import grpc

import sentence_intent_pb2
import sentence_intent_pb2_grpc

_SENTENCE_SENTIMENT_PORT = 50055

def run():
    channel = grpc.insecure_channel('localhost:{}'.format(_SENTENCE_SENTIMENT_PORT))
    stub = sentence_intent_pb2_grpc.SentenceIntentStub(channel)
    res = stub.Analyze(sentence_intent_pb2.Request(sentence="Rendez-moi mon paravent tout de suite!"))
    print(res)


if __name__ == "__main__":
    run()
