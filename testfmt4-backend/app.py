import time
from flask import Flask, request, send_from_directory
from flask_cors import CORS as flask_cors

import logic
import storage

app = Flask(__name__)
app.logger.info = app.logger.info or print
flask_cors(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_id = logic.save_file(file)
    return {"file_id": file_id}


@app.route("/preview", methods=["POST"])
def preview():
    result = logic.preview(request.form.to_dict())
    return result


@app.route("/convert", methods=["POST"])
def convert():
    result = logic.convert(request.form.to_dict())
    return result


@app.route("/prefill", methods=["POST"])
def prefill():
    result = logic.prefill(request.form.to_dict())
    return result


@app.route("/download/<string:file_id>", methods=["GET"])
def download(file_id):
    file_name = request.args.get("file_name") or logic.get_file_name(file_id)
    return send_from_directory(
        storage.FOLDER, file_id, as_attachment=True, attachment_filename=file_name
    )
