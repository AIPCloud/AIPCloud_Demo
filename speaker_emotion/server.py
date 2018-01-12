from concurrent import futures
import grpc
import time
import os

from speaker_emotion import speaker_emotion_pb2
from speaker_emotion import speaker_emotion_pb2_grpc

import numpy as np
import librosa
from keras import backend as K
import tensorflow as tf
from .utils import load_model
import configparser

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50054

model = load_model()
graph = tf.get_default_graph()

class SpeakerEmotion(speaker_emotion_pb2_grpc.SpeakerEmotionServicer):
    def __init__(self, graph, model):
        self.graph = graph
        self.model = model
        # Setting parameters

        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))

        self.FRAME_LENGTH = int(cfg.get("MEL", "frame_length"))
        self.FRAME_HOP = int(cfg.get("MEL", "frame_hop"))
        self.NUMBER_MELS = int(cfg.get("MEL", "n_mels"))

        self.CLASSES = [ "neutral", "depleased", "angry", "surprised" ]

    def refFun(self, S):
        return np.log10(1 + 10000 * S)

    def Analyze(self, request_iterator, context):
        execTime = time.time()
        Signal = []
        sampleRate = None
        for req in request_iterator:
            Signal += req.signal
            if not sampleRate:
                sampleRate = req.sample_rate
        if len(Signal) > 2 * sampleRate:
            with self.graph.as_default():
                emotion = self.detect(Signal, sampleRate, model=self.model)
            emotionResponse = []
            for e in emotion:
                emotionResponse.append(speaker_emotion_pb2.Emotion(neutral=e[0], depleased=e[1], angry=e[2], surprised=e[3]))

            execTime = time.time() - execTime
            return speaker_emotion_pb2.Response(
                emotions=emotionResponse,
                exec_time=execTime,
                empty=False
            )
        else:
            execTime = time.time() - execTime
            return speaker_emotion_pb2.Response(exec_time=execTime, empty=True)

    def detect(self, signal, sampleRate, model=False, debug=False):
        dataset_shape = (self.FRAME_LENGTH / 10) * self.NUMBER_MELS
        X_test_vectors = [np.repeat(0, dataset_shape)]

        signal = librosa.to_mono(np.transpose(signal))
        signal /= max(signal)

        spectrogram = librosa.feature.melspectrogram(
            signal, sr=sampleRate, n_fft=1024, hop_length=160)

        def refFun(S):
            return np.log10(1 + 10000 * S)

        logSpectrogram = refFun(spectrogram)

        signalLength = float(len(signal) / sampleRate) * 1000
        indexPosition = 0
        while indexPosition < signalLength - self.FRAME_LENGTH:
            row = np.asarray(logSpectrogram[:, int(
                indexPosition / 10):int((indexPosition + self.FRAME_LENGTH) / 10)]).ravel()
            X_test_vectors.append(row)
            indexPosition += self.FRAME_HOP

        X_test_vectors = X_test_vectors[1:]
        X_test = []
        for i in range(len(X_test_vectors)):
            matrix = np.zeros((self.NUMBER_MELS, int(self.FRAME_LENGTH / 10)))
            for l in range(self.NUMBER_MELS):
                for m in range(int(self.FRAME_LENGTH / 10)):
                    matrix[l, m] = X_test_vectors[i][l *
                                                     int(self.FRAME_LENGTH / 10) + m]
            X_test.append([matrix])
        X_test = np.asarray(X_test)
        predict = model.predict(X_test)

        return predict


def serve():
    global model, graph
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    speaker_emotion_pb2_grpc.add_SpeakerEmotionServicer_to_server(
        SpeakerEmotion(graph, model), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting SpeakerEmotion Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
