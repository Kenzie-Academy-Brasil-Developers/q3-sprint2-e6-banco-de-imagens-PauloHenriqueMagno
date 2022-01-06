import os
from flask import Flask, request, jsonify, send_file
from .kenzie.image import upload_image, zip_files

files_directory = os.getenv('FILES_DIRECTORY')
allowed_extensions = os.getenv('ALLOWED_EXTENSIONS').split(',')

app = Flask(__name__)

@app.get("/files")
def get_files_list():
    files = []
    for extension in allowed_extensions:
        files += os.listdir(f"{files_directory}/{extension}")

    return jsonify(files), 200

@app.get("/files/<extension>")
def get_files_by_extension(extension: str):
    extension = str(extension)

    if extension not in allowed_extensions:
        return jsonify({'message': 'extension not found'}), 400

    files_list = os.listdir(f"{files_directory}/{extension}")

    return jsonify(files_list), 200

@app.get("/download/<file_name>")
def get_file(file_name: str):
    file_name = str(file_name).lower()
    file_extension = file_name.split('.')
    file_extension = str(file_extension[len(file_extension)-1])

    if file_name not in os.listdir(f"{files_directory}/{file_extension}"):
        return jsonify({'message': 'File not found'}), 404

    return send_file(
        f"images/{file_extension}/{file_name}",
        as_attachment = True
    ), 200

@app.get("/download-zip")
def get_zip_files():
    return zip_files(request.args)

@app.post("/upload")
def post_files():
    return upload_image(request.files)