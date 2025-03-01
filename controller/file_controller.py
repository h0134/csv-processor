from flask import Blueprint, request, jsonify,send_file
from services.csv_service import process_csv_upload
from uuid import uuid4
import asyncio,io,csv
from db_layer import *


file_controller = Blueprint('file_controller', __name__)

@file_controller.route('/upload_csv', methods=['POST'])
async def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    request_id = str(uuid4()) 
    asyncio.create_task(process_csv_upload(file, request_id))
    
    return jsonify({"request_id": request_id}), 200

@file_controller.route('/status/<request_id>', methods=['GET'])
def status(request_id):
    return jsonify(get_request_status(request_id)), 200



@file_controller.route('/download_csv/<request_id>', methods=['GET'])
def download_csv(request_id):
    rows = get_product_by_requestId(request_id)

    if not rows:
        return jsonify({"error": f"No data found for request_id: {request_id}"}), 404
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["serial_number", "request_id", "product_name", "input_image_urls", "output_image_urls"])
    for row in rows:
        writer.writerow(row)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name=f"request_details_{request_id}.csv")
