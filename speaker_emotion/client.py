import grpc

import speaker_emotion_pb2
import speaker_emotion_pb2_grpc

import soundfile as sf

_SPEAKER_EMOTION_PORT = 50052


def gen(array, chunkSize):
    i = 0
    length = len(array)
    while i < length:
        chunk = []
        for j in range(i, i + chunkSize):
            if j < length:
                chunk.append(array[j])

        i += chunkSize
        yield speaker_emotion_pb2.Request(signal=chunk, sample_rate=chunkSize)

def run():
    channel = grpc.insecure_channel('localhost:{}'.format(_SPEAKER_EMOTION_PORT))
    stub = speaker_emotion_pb2_grpc.SpeakerEmotionStub(channel)

    # Reading file (test purposes)
    (signal, sampleRate) = sf.read("./sample_1.wav")

    it = stub.Analyze(gen(signal, sampleRate))
    try:
        for r in it:
            print(f"Neutralite = {r.emotion.neutral}")
    except grpc._channel._Rendezvous as err:
        print(err)


if __name__ == "__main__":
    run()
