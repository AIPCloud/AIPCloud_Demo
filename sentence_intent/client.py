import grpc

from sentence_intent import sentence_intent_pb2
from sentence_intent import sentence_intent_pb2_grpc

_SENTENCE_INTENT_PORT = 50051

def run(sentence):
    channel = grpc.insecure_channel('localhost:{}'.format(_SENTENCE_INTENT_PORT))
    stub = sentence_intent_pb2_grpc.SentenceIntentStub(channel)
    res = stub.Analyze(sentence_intent_pb2.Request(sentence=sentence))
    return res
