import logging
from io import BytesIO
import sys
import uvicorn
from loguru import logger
from fastapi import FastAPI, UploadFile
from src.types import HashesResponse
from src.logger import InterceptHandler


app = FastAPI()

@app.on_event("startup")
async def startup():
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logging.root.handlers = [InterceptHandler()]
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": not sys.stdout.isatty()}])

@app.post("/image", response_model=HashesResponse)
async def generate_hashes(file: UploadFile):
    buf = BytesIO(file.file.read())
    logger.debug(f"image size: {buf.__sizeof__()}")
    return {"data": buf}

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)