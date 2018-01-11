import grpc

import speech_to_text_pb2
import speech_to_text_pb2_grpc

import soundfile as sf

_SPEECH_TO_TEXT_PORT = 50053

def run():
    channel = grpc.insecure_channel('localhost:{}'.format(_SPEECH_TO_TEXT_PORT))
    stub = speech_to_text_pb2_grpc.SpeechToTextStub(channel)

    # Reading file (test purposes)
    (signal, sampleRate) = sf.read("./sample_1.wav")

    res = stub.Recognition(speech_to_text_pb2.Request(signal=signal, sample_rate=sampleRate, language_code='en-US'))

    print("Transcipt: {}".format(res))


if __name__ == "__main__":
    run()
