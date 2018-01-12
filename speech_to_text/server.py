from concurrent import futures
import grpc
import time
import os
from uuid import uuid4

import speech_to_text_pb2
import speech_to_text_pb2_grpc

import soundfile as sf
# Imports the Google Cloud client library
from google.oauth2 import service_account
from google.cloud import speech, storage, exceptions
from google.cloud.speech import enums, types

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50053


class SpeechToText(speech_to_text_pb2_grpc.SpeechToTextServicer):
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            '../aipcloud-212946bdf7b7.json')
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/devstorage.full_control'])
        storageClient = storage.Client(
            project="aipcloud-179518", credentials=scoped_credentials)
        self.bucketName = "aipcloud-bucket"
        # Get bucket:
        try:
            self.bucket = storageClient.get_bucket(self.bucketName)
        except exceptions.NotFound:
            raise Exception('Sorry, that bucket does not exist!')
        # Instantiates a client
        self.speechClient = speech.SpeechClient(credentials=scoped_credentials)

    def Recognition(self, request, context):
        execTime = time.time()
        try:
            # Set speech recognition config
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=request.sample_rate,
                language_code=request.language_code)

            # Write an audio file based on request signal
            print("Writing audio file based on signal.")
            fileName = str(uuid4()) + '.wav'
            sf.write(fileName, request.signal, request.sample_rate)
            # UPLOAD THE FILE TO GCS
            blob = self.bucket.blob(fileName)
            print("Uploading audio file.")
            blob.upload_from_filename(fileName)
            print("Upload done.")
            # Delete the local version
            os.remove(fileName)
            # Make sure the file has a unique name
            # Then feed the analyzer with the URI provided by GCS
            uri = 'gs://' + self.bucketName + '/' + fileName
            audio = types.RecognitionAudio(uri=uri)

            # Detects speech in the audio file
            print("Speech Recognition started.")
            operation = self.speechClient.long_running_recognize(
                config=config, audio=audio)

            operationResults = operation.result()
            operationResults = operationResults.results
            print("Speech Recognition is done.")
            if len(operationResults) == 0:
                raise Exception(
                    'The server did not send any recognition results.')

            results = []
            for res in operationResults:
                results.append(speech_to_text_pb2.Speech(transcript=res.alternatives[0].transcript))
            blob.delete()
        except:
            # Delete file from GCS and locally
            if os.path.isfile(fileName):
                os.remove(fileName)
            if blob:
                blob.delete()
            execTime = time.time() - execTime
            return speech_to_text_pb2.Response(
                speeches=[speech_to_text_pb2.Speech(
                    transcript="Error while converting speech to text.")],
                exec_time=execTime)

        execTime = time.time() - execTime
        return speech_to_text_pb2.Response(
            speeches=results,
            exec_time=execTime)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    speech_to_text_pb2_grpc.add_SpeechToTextServicer_to_server(
        SpeechToText(), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting SpeechToText Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
