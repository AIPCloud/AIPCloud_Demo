import grpc

import sentence_sentiment_pb2
import sentence_sentiment_pb2_grpc

_SENTENCE_SENTIMENT_PORT = 50051

def run():
    channel = grpc.insecure_channel('localhost:{}'.format(_SENTENCE_SENTIMENT_PORT))
    stub = sentence_sentiment_pb2_grpc.SentenceSentimentStub(channel)
    res = stub.Analyze(sentence_sentiment_pb2.Request(sentence="Je teste cette phrase maintenant tout de suite, je suis très content!"))
    print(res)


if __name__ == "__main__":
    run()
