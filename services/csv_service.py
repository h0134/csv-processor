import csv,io
import asyncio
from services.image_processing_service import process_images_async
from utils.file_utils import store_output_urls
from utils.image_utils import compress_image
from io import StringIO
from db_layer import *

async def process_csv_upload(file, request_id):
 
    file_stream = io.StringIO(file.stream.read().decode('utf-8'))
    insert_request_status(request_id, "processing")
    reader = csv.reader(file_stream)
    headers = next(reader)     

    data = []
    for row in reader:
        data.append(row) 

    

    processed_data = []
    print(data)
   
    for  row in data:
        if len(row) != 3:
            continue 
        
        serial_number, product_name, image_urls = row
        image_urls = image_urls.split(',')
        output_urls=process_images_async(image_urls)
        insert_product_details(serial_number,product_name, ",".join(image_urls),request_id,",".join(output_urls))
    update_request_status(request_id, "completed")
    return ""
