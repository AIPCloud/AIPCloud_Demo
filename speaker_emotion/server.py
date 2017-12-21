from concurrent import futures
import grpc
import time
import os

import speaker_emotion_pb2
import speaker_emotion_pb2_grpc

import numpy as np
import librosa
from keras import backend as K
import tensorflow as tf
from utils import load_model

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50052

config=tf.ConfigProto(log_device_placement=False,allow_soft_placement=True)
sess = tf.Session(config=config)
K.set_session(sess) # K is keras backend
model = load_model()

class SpeakerEmotion(speaker_emotion_pb2_grpc.SpeakerEmotionServicer):
    def __init__(self):
        self.FRAME_LENGTH = 1000
        self.NUMBER_MELS = 128
        self.CLASSES = [ "neutral", "calm", "happy", "sad", "angry", "fearful", "surprise", "disgust" ]


    def refFun(self, S):
    	return np.log10(1 + 10000 * S)

    def Analyze(self, request_iterator, context):
        global model, sess
        execTime = time.time()

        for req in request_iterator:
            signal = req.signal
            sampleRate = req.sample_rate

            dataset_shape = (self.FRAME_LENGTH / 10) * self.NUMBER_MELS
            X_test_vectors = [ np.repeat(0, dataset_shape) ]
            signal = librosa.to_mono(np.transpose(signal))
            trimmedSignal, _ = librosa.effects.trim(signal, top_db=50)
            spectrogram = librosa.feature.melspectrogram(trimmedSignal, sr=sampleRate, n_fft=1024, hop_length=160)
            logSpectrogram = self.refFun(spectrogram)

            signalLength = float(len(trimmedSignal) / sampleRate) * 1000
            indexPosition = 0
            while indexPosition < signalLength - self.FRAME_LENGTH:
            	row = np.asarray(logSpectrogram[:, int(indexPosition / 10):int((indexPosition + self.FRAME_LENGTH) / 10)]).ravel()
            	X_test_vectors.append(row)
            	indexPosition += self.FRAME_LENGTH

            X_test_vectors = X_test_vectors[1:]
            X_test = []
            for i in range(len(X_test_vectors)):
            	matrix = np.zeros((self.NUMBER_MELS, int(self.FRAME_LENGTH / 10)))
            	for l in range(self.NUMBER_MELS):
            		for m in range(int(self.FRAME_LENGTH / 10)):
            			matrix[l, m] = X_test_vectors[i][l * int(self.FRAME_LENGTH / 10) + m]
            	X_test.append([matrix])

            with sess.graph.as_default():
                predict = model.predict(X_test)
            print(predict)

            # yield speaker_emotion_pb2.Response(
            # neutral=predict[-1][0],
            # calm=predict[-1][1],
            # happy=predict[-1][2],
            # sad=predict[-1][3],
            # angry=predict[-1][4],
            # fearful=predict[-1][5],
            # surprise=predict[-1][6],
            # disgust=predict[-1][7],
            # exec_time=execTime)
            execTime = time.time() - execTime
            yield speaker_emotion_pb2.Response(
            neutral=len(req.signal),
            calm=0.2,
            happy=0.3,
            sad=0.4,
            angry=0.5,
            fearful=0.6,
            surprise=0.7,
            disgust=0.8,
            exec_time=execTime
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    speaker_emotion_pb2_grpc.add_SpeakerEmotionServicer_to_server(SpeakerEmotion(), server)
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
