import os
import uuid
from zipfile import ZipFile, ZIP_DEFLATED

import database
import settings
import utils


def id_to_path(id):
    return os.path.join(settings.UPLOAD_FOLDER, id)


def get_names_in_archive(file_id):
    path = id_to_path(file_id)
    with ZipFile(path) as f:
        result = [x for x in f.namelist() if not x.endswith("/")]
        return list(sorted(result, key=utils.natural_sorting_key))


def save_file(file, file_id, file_name):
    path = id_to_path(file_id)
    database.add_upload_info(file_id, file_name)
    file.save(path)


# TODO: read() extracts the file, therefore, it might cause performance issues
def get_renamed_archive(source_file_id, bef, aft, file_name):
    target_file_id = str(uuid.uuid4())
    source = ZipFile(id_to_path(source_file_id), "r")
    target = ZipFile(id_to_path(target_file_id), "w", ZIP_DEFLATED)
    for bef_name, aft_name in zip(bef, aft):
        target.writestr(aft_name, source.read(bef_name))
    target.close()
    source.close()
    database.add_upload_info(target_file_id, file_name)
    return {"file_id": target_file_id}


def get_upload_folder():
    return settings.UPLOAD_FOLDER


def get_file_size(file_id):
    path = id_to_path(file_id)
    return os.path.getsize(path)
