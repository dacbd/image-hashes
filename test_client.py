import sys
from loguru import logger
import grpc
import image_hasher_pb2 as ServiceTypes
import image_hasher_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:8000") as channel:
        stub = image_hasher_pb2_grpc.ImageHasherStub(channel)
        with open("./assets/img80x80.jpg", "rb") as small_image:
            small_bytes = small_image.read()
        with open("./assets/img1000x1000.jpg", "rb") as large_image:
            large_bytes = large_image.read()
        small_res = stub.Hash(ServiceTypes.HashRequest(image=small_bytes))
        print(small_res)
        large_res = stub.Hash(ServiceTypes.HashRequest(image=large_bytes))
        print(large_res)
        print(stub.Compare(ServiceTypes.CompareRequest(base=large_bytes, comparator=small_bytes)))
        print(stub.SingleDistance(ServiceTypes.DistanceRequest(base="8cc5d1a1b47a78c7", comparator="8cc5d1a1c47a78c7")))


if __name__ == "__main__":
    run()