from io import BytesIO
from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, Field, constr
from src.hashes import image_hashes, standard_hashes

SHA1 = Annotated[
    constr(
        to_lower=True,
        strip_whitespace=True,
        regex="^[a-f0-9]+$",
        min_length=40,
        max_length=40
    ),
    Field(
        title="SHA1 Hash"
    )
]
SHA256 = Annotated[
    constr(
        to_lower=True,
        strip_whitespace=True,
        regex="^[a-f0-9]+$",
        min_length=64,
        max_length=64
    ),
    Field(
        title="SHA256 Hash"
    )
]
MD5 = Annotated[
    constr(
        to_lower=True,
        strip_whitespace=True,
        regex="^[a-f0-9]+$",
        min_length=32,
        max_length=32
    ),
    Field(
        title="MD5 Hash"
    )
]
IMGHASH = Annotated[
    constr(
        to_lower=True,
        strip_whitespace=True,
        regex="^[a-f0-9]+$",
        min_length=10,
        max_length=16
    ),
    Field(
        title="Image Hash"
    )
]

class HashesResponse(BaseModel):
    sha1: SHA1
    sha256: SHA256
    md5: MD5
    average_hash: IMGHASH
    color_hash: IMGHASH
    dhash: IMGHASH
    phash: IMGHASH
    whash: IMGHASH
    crop_hash: List[IMGHASH]

    def __init__(__pydantic_self__, data: BytesIO) -> None:
        ref_dict = { 
            **image_hashes(data),
            **standard_hashes(data)
        }
        super().__init__(**ref_dict)