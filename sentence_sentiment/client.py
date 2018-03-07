import grpc

from sentence_sentiment import sentence_sentiment_pb2
from sentence_sentiment import sentence_sentiment_pb2_grpc

_SENTENCE_SENTIMENT_PORT = 50052

def run(sentence):
    channel = grpc.insecure_channel('localhost:{}'.format(_SENTENCE_SENTIMENT_PORT))
    stub = sentence_sentiment_pb2_grpc.SentenceSentimentStub(channel)
    res = stub.Analyze(sentence_sentiment_pb2.Request(sentence=sentence))
    return res
