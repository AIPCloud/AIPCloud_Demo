from concurrent import futures
import grpc
import time
import os

import soundfile as sf

import new_demo_portal_pb2
import new_demo_portal_pb2_grpc

import speech_to_text_pb2
import speaker_emotion_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50050


class NewDemoPortal(new_demo_portal_pb2_grpc.NewDemoPortalServicer):
    def Analyze(self, request_iterator, context):
        Signal = []
        execTime = time.time()
        print("Connection with client established.")
        for req in request_iterator:
            # print("Successful request.")
            Signal += req.signal
            if len(Signal) > 15 * req.sample_rate:
                print("Writing audio file.")
                sf.write("new_file.wav", Signal, req.sample_rate)

                yield new_demo_portal_pb2.Response(
                    speech=speech_to_text_pb2.Speech(
                        transcript="test"),
                    emotion=speaker_emotion_pb2.Emotion(
                        neutral=0.1,
                        calm=0.2,
                        happy=0.3,
                        sad=0.4,
                        angry=0.5,
                        fearful=0.6,
                        surprise=0.7,
                        disgust=0.8),
                    exec_time=execTime)
                raise StopIteration
            execTime = time.time() - execTime


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    new_demo_portal_pb2_grpc.add_NewDemoPortalServicer_to_server(
        NewDemoPortal(), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting NewDemoPortal Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
