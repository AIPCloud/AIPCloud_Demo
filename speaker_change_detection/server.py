from concurrent import futures
import grpc
import time
import os
import random
import tensorflow as tf

from .utils import load_model
from .detect import detect

from speaker_change_detection import speaker_change_detection_pb2
from speaker_change_detection import speaker_change_detection_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50053

model = load_model()
graph = tf.get_default_graph()


class SpeakerChangeDetection(speaker_change_detection_pb2_grpc.SpeakerChangeDetectionServicer):
    def __init__(self, graph, model):
        self.graph = graph
        self.model = model

    def Analyze(self, request_iterator, context):
        sampleRate = False
        Signal = []
        signalChunk = []
        for req in request_iterator:
            if sampleRate and sampleRate != req.sample_rate:
                raise Exception("Sample rate changed during streaming.")
            sampleRate = req.sample_rate
            signalChunk += req.signal
            if len(signalChunk) > 5 * sampleRate:
                with self.graph.as_default():
                    execTime = time.time()
                    t_0 = len(Signal) / sampleRate
                    changes = detect(signalChunk, sampleRate, model=self.model)
                    changes = [4]
                for change in changes:
                    change += t_0
                    yield speaker_change_detection_pb2.Response(change=speaker_change_detection_pb2.Change(time=change), exec_time=time.time() - execTime)
                signalChunk = []
            Signal += req.signal

def serve():
    global graph, model
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    speaker_change_detection_pb2_grpc.add_SpeakerChangeDetectionServicer_to_server(
        SpeakerChangeDetection(graph, model), server)
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
