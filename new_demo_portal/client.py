import grpc

import new_demo_portal_pb2
import new_demo_portal_pb2_grpc

import soundfile as sf

_NEW_DEMO_PORTAL_PORT = 50050


def gen(array, chunkSize):
    i = 0
    length = len(array)
    while i < length:
        chunk = []
        for j in range(i, i + chunkSize):
            if j < length:
                chunk.append(array[j])

        i += chunkSize
        yield new_demo_portal_pb2.Request(signal=chunk, sample_rate=chunkSize)

def run():
    channel = grpc.insecure_channel('localhost:{}'.format(_NEW_DEMO_PORTAL_PORT))
    stub = new_demo_portal_pb2_grpc.NewDemoPortalStub(channel)

    # Reading file (test purposes)
    (signal, sampleRate) = sf.read("./sample_1.wav")

    generator = gen(signal, sampleRate)
    it = stub.Analyze(generator)
    try:
        for r in it:
            print(r)
    except grpc._channel._Rendezvous as err:
        print(err)


if __name__ == "__main__":
    run()
