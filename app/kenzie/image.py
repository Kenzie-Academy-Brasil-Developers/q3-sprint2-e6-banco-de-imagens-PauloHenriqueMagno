from flask import jsonify, send_from_directory
import os

files_directory = os.getenv('FILES_DIRECTORY')
allowed_extensions = os.getenv('ALLOWED_EXTENSIONS').split(',')

def check_and_create_directory():
    if "images" not in os.listdir("./app"):
        os.mkdir(files_directory)
        for extension in allowed_extensions:
            os.mkdir(f"{files_directory}/{extension}")

check_and_create_directory()

def upload_image(files):
    if 'file' not in files:
        return jsonify({'message': 'File is missing'}), 404

    file = files["file"]
    file_name = file.filename.lower()

    file_extension = file_name.split('.')
    file_extension = file_extension[len(file_extension)-1]

    if file_extension not in allowed_extensions:
        return jsonify({'message': 'File extension not supported'}), 415   

    if file_name in os.listdir(f"{files_directory}/{file_extension}"):
        return jsonify({'message': 'File already exist'}), 409
    
    file.save(f"{files_directory}/{file_extension}/{file_name}")

    return jsonify(os.listdir(f"{files_directory}/{file_extension}")), 201

def zip_files(args):
    file_extension = str(args.get('file_extension'))
    compression_ratio = int(args.get('compression_ratio', 6))

    if not file_extension:
        return jsonify({'message': 'File extension is necessary'}), 404

    if file_extension not in allowed_extensions:
        return jsonify({'message': 'File extension do not exist'}), 404

    os.system(f"cd app/images/{file_extension} && zip -{compression_ratio} -r files * && mv {file_extension}.zip /tmp")

    return send_from_directory(
        directory = "/tmp",
        path=f"{file_extension}.zip",
        as_attachment=True
    )