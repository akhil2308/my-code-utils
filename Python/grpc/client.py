"""Minimal gRPC client. Generate stubs first — see README.md."""
import grpc

import greeter_pb2
import greeter_pb2_grpc


def main(name="akhil", target="localhost:50051"):
    with grpc.insecure_channel(target) as channel:
        stub = greeter_pb2_grpc.GreeterStub(channel)
        reply = stub.SayHello(greeter_pb2.HelloRequest(name=name))
        print("server said:", reply.message)


if __name__ == "__main__":
    main()
