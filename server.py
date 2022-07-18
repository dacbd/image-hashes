import asyncio
import sys
from io import BytesIO

from loguru import logger
import grpc
import image_hasher_pb2 as ServiceTypes
import image_hasher_pb2_grpc
from src import utils

_cleanup_coroutines = []

class ImageHasher(image_hasher_pb2_grpc.ImageHasherServicer):
    
    async def Hash(
        self,
        request: ServiceTypes.HashRequest,
        context: grpc.aio.ServicerContext
    ) -> ServiceTypes.HashResponse:
        crypt_hashes = utils.standard_hashes(BytesIO(initial_bytes=request.image))
        image_hashes = utils.image_hashes(BytesIO(initial_bytes=request.image))
        return ServiceTypes.HashResponse(
            std_hashes = ServiceTypes.CryptoHashes(**crypt_hashes),
            image_hashes = ServiceTypes.ImageHashes(**image_hashes)
        )

    async def Compare(
        self,
        request: ServiceTypes.CompareRequest,
        context: grpc.aio.ServicerContext
    ) -> ServiceTypes.CompareResponse:
        c_dict = utils.compare(BytesIO(initial_bytes=request.base), BytesIO(initial_bytes=request.comparator))
        return ServiceTypes.CompareResponse(
            base = ServiceTypes.CryptoHashes(**c_dict["base"]),
            comparator = ServiceTypes.CryptoHashes(**c_dict["other"]),
            distance = ServiceTypes.Distance(
                dhash = c_dict["distance"]["dhash"],
                phash = c_dict["distance"]["phash"],
                whash = c_dict["distance"]["whash"],
                average_hash = c_dict["distance"]["average_hash"],
                color_hash = c_dict["distance"]["color_hash"],
                crop_hash = ServiceTypes.CropHashDistance(**c_dict["distance"]["crop_hash"])
            )
        )

    async def SingleDistance(
        self,
        request: ServiceTypes.DistanceRequest,
        context: grpc.aio.ServicerContext
    ) -> ServiceTypes.DistanceResponse:
        return ServiceTypes.DistanceResponse(
            distance = utils.distance(request.base, request.comparator)
        )

async def serve() -> None:
    server = grpc.aio.server()
    image_hasher_pb2_grpc.add_ImageHasherServicer_to_server(ImageHasher(), server)
    listen_addr = "127.0.0.1:8000"
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting server of {listen_addr}")
    await server.start()

    async def shutdown():
        logger.info("Starting graceful shutdown")
        await server.stop(5)

    _cleanup_coroutines.append(shutdown())
    await server.wait_for_termination()

if __name__ == "__main__":
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": not sys.stdout.isatty()}])
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()