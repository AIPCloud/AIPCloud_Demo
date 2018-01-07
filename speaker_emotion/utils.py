import os

from google.oauth2 import service_account
from google.cloud import storage, exceptions
from keras.models import model_from_json

def check_or_download(path, fileName):
    if(not os.path.exists("./data/{fileName}".format(fileName=fileName))):
        print("Downloading {fileName} from the cloud storage.".format(fileName=fileName))
        credentials = service_account.Credentials.from_service_account_file('./aipcloud-987fc3f00757.json')
        storageClient = storage.Client(project="aipcloud-179518", credentials=credentials)
        bucketName = "aipcloud-bucket"
        # Get bucket:
        try:
            bucket = storageClient.get_bucket(bucketName)
        except exceptions.NotFound:
            raise Exception('Sorry, that bucket does not exist!')
        blob = bucket.blob("data{path}/{fileName}".format(path=path, fileName=fileName))
        blob.download_to_filename("./data/{fileName}".format(fileName=fileName))


def load_model():
    print("Checking if model is on server.")
    check_or_download("/sound/emotion", "model.json")
    check_or_download("/sound/emotion", "weights.h5")
    print("Model downloaded.")
    print("Loading speaker emotion model.")
    json_file = open(os.path.join("./data/model.json"), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("./data/weights.h5")
    print("Speaker emotion model succesfully loaded.")
    return model
