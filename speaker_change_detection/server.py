from concurrent import futures
import grpc
import time
import os
import random
import tensorflow as tf
from keras import backend as K

from utils import load_model
from detect import detect

import speaker_change_detection_pb2
import speaker_change_detection_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50054

config = tf.ConfigProto(log_device_placement=False, allow_soft_placement=True)
sess = tf.Session(config=config)
K.set_session(sess)  # K is keras backend
model = load_model()

class SpeakerChangeDetection(speaker_change_detection_pb2_grpc.SpeakerChangeDetectionServicer):
    def __init__(self):
        self.sampleRate = 0

    def Analyze(self, request, context):
        global model, sess
        execTime = time.time()
        Signal = []

        with sess.graph.as_default():
            changes = detect(request.signal, request.sample_rate, model=model)

        execTime = time.time() - execTime
        return speaker_change_detection_pb2.Response(changes=speaker_change_detection_pb2.Changes(time=changes), exec_time=execTime)

        # lastAnalysis = 0
        # for r in request_iterator:
        # 	self.sampleRate = r.sample_rate
        # 	Signal += r.signal
        # 	analysisSize = 3 * self.sampleRate
            # if len(Signal) - analysisSize > lastAnalysis:
        # 		print("We have enough data to run an analysis.")
        # 		# res = detect(lastAnalysis, lastAnalysis + analysisSize)
        # 		res = detect(Signal, self.sampleRate, framing=False)
        # 		lastAnalysis += 0.5 * analysisSize
        # 		yield speaker_change_detection_pb2.Response(
        # 		change=speaker_change_detection_pb2.Change(time=res),
        # 		exec_time=execTime)
        # res = detect(Signal, len(Signal) - analysisSize, len(Signal))
        # yield speaker_change_detection_pb2.Response(
        # change=speaker_change_detection_pb2.Change(time=res),
        # exec_time=execTime)




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
