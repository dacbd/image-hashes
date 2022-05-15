import hashlib
import imagehash as ImgHash
from io import BytesIO
from PIL import Image

def compare(base: BytesIO, other: BytesIO) -> dict:
    base_img = Image.open(base)
    other_img = Image.open(other)
    crop_res = ImgHash.crop_resistant_hash(base_img).hash_diff(ImgHash.crop_resistant_hash(other_img))
    return {
        "base": standard_hashes(base),
        "other": standard_hashes(other),
        "distance":{
            "average_hash": ImgHash.average_hash(base_img) - ImgHash.average_hash(other_img),
            "color_hash": ImgHash.colorhash(base_img) - ImgHash.colorhash(other_img),
            "crop_hash": {
                "matching_segments": crop_res[0],
                "hamming_distance": crop_res[1]
            },
            "dhash": ImgHash.dhash(base_img) - ImgHash.dhash(other_img),
            "phash": ImgHash.phash(base_img) - ImgHash.phash(other_img),
            "whash": ImgHash.whash(base_img) - ImgHash.whash(other_img),
        }
    }

def distance(base: str, other: str) -> int:
    base_img = ImgHash.ImageHash(base)
    other_img = ImgHash.ImageHash(other)
    return base_img - other_img

def image_hashes(image: BytesIO) -> dict:
    img = Image.open(image)
    return {
        "average_hash": ImgHash.average_hash(img).__str__(),
        "color_hash": ImgHash.colorhash(img).__str__(),
        "crop_hash": ImgHash.crop_resistant_hash(img).__str__().split(","),
        "dhash": ImgHash.dhash(img).__str__(),
        "phash": ImgHash.phash(img).__str__(),
        "whash": ImgHash.whash(img).__str__(),
    }

def standard_hashes(image: BytesIO) -> dict:
    std_hashes = {
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
        "md5": hashlib.md5()
    }
    for _, hash in std_hashes.items():
        hash.update(image.getbuffer())

    return {
        "sha1": std_hashes["sha1"].hexdigest(),
        "sha256": std_hashes["sha256"].hexdigest(),
        "md5": std_hashes["md5"].hexdigest()
    }
