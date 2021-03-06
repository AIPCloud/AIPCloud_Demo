import os
import time
import grpc
from concurrent import futures
from keras import backend as K
import tensorflow as tf

from sentence_sentiment import sentence_sentiment_pb2
from sentence_sentiment import sentence_sentiment_pb2_grpc

import numpy as np
import nltk

from .utils import word2vec, load_model

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50052

W2V, model = load_model()
graph = tf.get_default_graph()


class SentenceSentiment(sentence_sentiment_pb2_grpc.SentenceSentimentServicer):
    def __init__(self, graph, model, W2V):
        self.graph = graph
        self.model = model
        self.W2V = W2V
        self.MAX_LENGTH = 300
        self.TOP_WORDS = 40000

    def Analyze(self, request, context):
        execTime = time.time()

        text = request.sentence
        text = text.lower()
        print(text)
        # We transform our sentence into word tokens
        tokens = nltk.word_tokenize(text)

        # Our input is a MAX_LENGTH integer vector
        vector = np.repeat(0, self.MAX_LENGTH)
        for i in range(min(self.MAX_LENGTH, len(tokens))):
            # If the word is in vocabulary
            if tokens[i] in self.W2V.wv.vocab:
                indexVal = self.W2V.wv.vocab[tokens[i]].index
                # If the word index was in the vocabulary during training phase
                if indexVal < self.TOP_WORDS:
                    vector[i] = indexVal
        with self.graph.as_default():
            predict = self.model.predict(np.asarray([vector]))
        execTime = time.time() - execTime
        return sentence_sentiment_pb2.Response(
            sentiment=sentence_sentiment_pb2.Sentiment(
                positivity=predict[0][2],
                neutrality=predict[0][1],
                negativity=predict[0][0]),
            exec_time=execTime)


def serve():
    global W2V, model, graph
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentence_sentiment_pb2_grpc.add_SentenceSentimentServicer_to_server(
        SentenceSentiment(graph, model, W2V), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting SentenceSentiment Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
