import grpc

from speaker_emotion import speaker_emotion_pb2
from speaker_emotion import speaker_emotion_pb2_grpc

import librosa

_SPEAKER_EMOTION_PORT = 50054


def gen(array, chunkSize, sr):
    i = 0
    length = len(array)
    while i < length:
        chunk = []
        for j in range(i, i + chunkSize):
            if j < length:
                chunk.append(array[j])

        i += chunkSize
        yield speaker_emotion_pb2.Request(signal=chunk, sample_rate=sr)

def run(signal, sampleRate):
    channel = grpc.insecure_channel('localhost:{}'.format(_SPEAKER_EMOTION_PORT))
    stub = speaker_emotion_pb2_grpc.SpeakerEmotionStub(channel)

    res = stub.Analyze(gen(signal, int(sampleRate), sampleRate))
    return res

if __name__ == "__main__":
    run()
