import grpc

import speaker_change_detection_pb2
import speaker_change_detection_pb2_grpc

import librosa

_SPEAKER_CHANGE_DETECTION_PORT = 50054


def gen(array, chunkSize, sr):
    i = 0
    length = len(array)
    while i < length:
        chunk = []
        for j in range(i, i + chunkSize):
            if j < length:
                chunk.append(array[j])

        i += chunkSize
        yield speaker_change_detection_pb2.Request(signal=chunk, sample_rate=sr)

def run():
    channel = grpc.insecure_channel('localhost:{}'.format(_SPEAKER_CHANGE_DETECTION_PORT))
    stub = speaker_change_detection_pb2_grpc.SpeakerChangeDetectionStub(channel)

    # Reading file (test purposes)
    (signal, sampleRate) = librosa.load("./sample_3.wav", sr=44100)
    it = stub.Analyze(gen(signal, 1024, sampleRate))
    try:
        for r in it:
            print("Resultat = {response}".format(response=r))
    except grpc._channel._Rendezvous as err:
        print(err)


if __name__ == "__main__":
    run()
