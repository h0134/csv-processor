from PIL import Image
import io

def compress_image(img: Image) -> Image:
    # Compress image by 50%
    width, height = img.size
    img = img.resize((width // 2, height // 2))
    print("Image compressed.")
    print(img)
    return img
