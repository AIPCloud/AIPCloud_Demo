import os
from gensim.models import word2vec

from google.cloud import storage, exceptions
from keras.models import model_from_json

def check_or_download(fileName):
    if(not os.path.isfile("./data/{}".format(fileName))):
        print("Downloading {} from the cloud storage.".format(fileName))
        storageClient = storage.Client()
        bucketName = "aipcloud-bucket"
        # Get bucket:
        try:
            bucket = storageClient.get_bucket(bucketName)
        except exceptions.NotFound:
            raise Exception('Sorry, that bucket does not exist!')
        blob = bucket.blob("data/{}".format(fileName))
        blob.download_to_filename("./data/{}".format(fileName))


def load_model():
    print("Checking if model is on server.")
    check_or_download("FR_LSTM_model.json")
    check_or_download("FR_LSTM_weights.h5")
    check_or_download("FR.vocab")
    print("Model downloaded.")
    print("Loading sentiment model.")
    json_file = open(os.path.join("./data/FR_LSTM_model.json"), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("./data/FR_LSTM_weights.h5")
    W2V = word2vec.Word2Vec.load("./data/FR.vocab")
    print("Sentiment model succesfully loaded.")
    return W2V, model
