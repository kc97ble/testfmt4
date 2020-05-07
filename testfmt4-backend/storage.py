import os
import uuid
from zipfile import ZipFile, ZIP_DEFLATED

FOLDER = "/tmp"


def id_to_path(id):
    return os.path.join(FOLDER, id)


def get_file_list_in_archive(uploaded_file_id):
    path = id_to_path(uploaded_file_id)
    with ZipFile(path) as f:
        return f.namelist()


def get_renamed_archive(uploaded_file_id, bef, aft):
    renamed_file_id = str(uuid.uuid4())
    source = ZipFile(id_to_path(uploaded_file_id), "r")
    target = ZipFile(id_to_path(renamed_file_id), "w", ZIP_DEFLATED)
    for bef_name, aft_name in zip(bef, aft):
        target.writestr(aft_name, source.read(bef_name))
    target.close()
    source.close()
    return {"file_id": renamed_file_id}
