from concurrent import futures
import grpc
import time
import os

import new_demo_portal_pb2
import new_demo_portal_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 50054

class NewDemoPortal(new_demo_portal_pb2_grpc.NewDemoPortalServicer):
    def Analyze(self, request, context)
        return Response(exec_time=2)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    new_demo_portal_pb2_grpc.add_NewDemoPortalServicer_to_server(NewDemoPortal(), server)
    server.add_insecure_port('[::]:{}'.format(_PORT))
    server.start()
    print("Starting NewDemoPortal Server on port {}...".format(_PORT))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
