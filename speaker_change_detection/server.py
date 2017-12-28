from concurrent import futures
import grpc
import time
import os
import random

import speaker_change_detection_pb2
import speaker_change_detection_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50054


class SpeakerChangeDetection(speaker_change_detection_pb2_grpc.SpeakerChangeDetectionServicer):
    def __init__(self):
        self.Signal = []
        self.sampleRate = 0

    def SCD(self, start, stop):
        startS = start / self.sampleRate
        stopS = stop / self.sampleRate
        print(
            f"Starting change detection algorithm from {startS}s to {stopS}s.")
        time.sleep(0.4)
        print("Ending change detection algorithm.")
        return (start + random.random() * (stop - start)) / self.sampleRate

    def Analyze(self, request_iterator, context):
        execTime = time.time()

        lastAnalysis = 0

        for r in request_iterator:
            self.sampleRate = r.sample_rate
            self.Signal += r.signal
            analysisSize = 3 * self.sampleRate
            if len(self.Signal) - analysisSize > lastAnalysis:
                print("We have enough data to run an analysis.")
                res = self.SCD(lastAnalysis, lastAnalysis + analysisSize)
                lastAnalysis += 0.5 * analysisSize
                yield speaker_change_detection_pb2.Response(
                change=speaker_change_detection_pb2.Change(time=res),
                exec_time=execTime)
        res = self.SCD(len(self.Signal) - analysisSize, len(self.Signal))
        yield speaker_change_detection_pb2.Response(
        change=speaker_change_detection_pb2.Change(time=res),
        exec_time=execTime)


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
