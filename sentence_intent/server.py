from concurrent import futures
import grpc
import time
import os

from sentence_intent import sentence_intent_pb2
from sentence_intent import sentence_intent_pb2_grpc

import numpy as np
import nltk
from keras import backend as K
import tensorflow as tf

from .utils import word2vec, load_model

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50051

W2V, model = load_model()
graph = tf.get_default_graph()


class SentenceIntent(sentence_intent_pb2_grpc.SentenceIntentServicer):
    def __init__(self, graph, model, W2V):
        self.graph = graph
        self.model = model
        self.W2V = W2V
        self.MAX_LENGTH = 24
        self.TOP_WORDS = 40000

    def Analyze(self, request, context):
        execTime = time.time()

        text = request.sentence.lower()
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
            predict = self.model.predict(np.asarray([vector]))[0]
        execTime = time.time() - execTime
        return sentence_intent_pb2.Response(
            intent=sentence_intent_pb2.Intent(
                request=predict[0],
                threat=predict[1],
                opinion=predict[2]),
            exec_time=execTime)


def serve():
    global model, W2V, graph

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentence_intent_pb2_grpc.add_SentenceIntentServicer_to_server(
        SentenceIntent(graph, model, W2V), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting SentenceIntent Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
