from flask import Flask, request
from flask_cors import CORS as flask_cors

import logic

app = Flask(__name__)
app.logger.info = app.logger.info or print
flask_cors(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/upload", methods=["GET", "POST"])
def upload():
    app.logger.info(request.form)
    app.logger.info(request.files)
    file = request.files["file"]
    uploaded_file_id = logic.save_file(file)
    return {"uploaded_file_id": uploaded_file_id}
