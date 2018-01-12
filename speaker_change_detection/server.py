from concurrent import futures
import grpc
import time
import os
import random
import tensorflow as tf
from keras import backend as K

from .utils import load_model
from .detect import detect

from speaker_change_detection import speaker_change_detection_pb2
from speaker_change_detection import speaker_change_detection_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50053


class SpeakerChangeDetection(speaker_change_detection_pb2_grpc.SpeakerChangeDetectionServicer):
    def __init__(self):
        config = tf.ConfigProto(log_device_placement=False, allow_soft_placement=True)
        self.sess = tf.Session(config=config)
        K.set_session(self.sess)  # K is keras backend
        self.model = load_model()

    def Analyze(self, request_iterator, context):
        sampleRate = False
        Signal = []
        signalChunk = []
        for req in request_iterator:
            if sampleRate and sampleRate != req.sample_rate:
                raise Exception("Sample rate changed during streaming.")
            sampleRate = req.sample_rate
            signalChunk += req.signal
            if len(signalChunk) > 3 * sampleRate:
                with self.sess.graph.as_default():
                    execTime = time.time()
                    t_0 = len(Signal) / sampleRate
                    changes = detect(signalChunk, sampleRate, model=self.model)
                for change in changes:
                    change += t_0
                    yield speaker_change_detection_pb2.Response(change=speaker_change_detection_pb2.Change(time=change), exec_time=time.time() - execTime)
                signalChunk = []
            Signal += req.signal

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    speaker_change_detection_pb2_grpc.add_SpeakerChangeDetectionServicer_to_server(
        SpeakerChangeDetection(), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting SpeakerChangeDetection Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
