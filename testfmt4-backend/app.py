import time
import flask

from flask import Flask, request, send_from_directory
from flask_cors import CORS as flask_cors

import logic
import storage

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024
app.logger.info = app.logger.info or print
flask_cors(app)


@app.route("/")
def intro():
    return "testfmt4-backend"


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
        storage.get_upload_folder(),
        file_id,
        as_attachment=True,
        attachment_filename=file_name,
    )


@app.route("/preview_file/<string:file_id>", methods=["GET"])
def preview_file(file_id):
    result = logic.preview_file(file_id)
    return result


@app.errorhandler(Exception)
def handle_exception(e):
    message = e.message if hasattr(e, "message") else str(e)
    code = 500
    if len(message) >= 4 and message[3] == ":" and message[:3].isdigit():
        code = int(message[:3])
        message = message[4:].lstrip()
    if not message:
        message = str(type(e))
    return flask.jsonify(error_msg="Error: " + message), code
