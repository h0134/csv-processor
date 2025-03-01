import requests
from PIL import Image
from io import BytesIO
from utils.minio_utils import MinioUtil
import asyncio
from utils.image_utils import compress_image
import random
import string
from config import Config

def process_images_async(image_urls):
    output_image_urls = []

    for image_url in image_urls:
        response = requests.get(image_url.strip())
        img = Image.open(BytesIO(response.content))
        compressed_img = compress_image(img)
        minio_util = MinioUtil(Config.minio_host, Config.minio_secret, Config.minio_key, Config.minio_bucket)
        output_image_url =  minio_util.upload_image(compressed_img, generate_random_string(10) + ".png")
        output_image_urls.append(output_image_url)

    return output_image_urls

def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))