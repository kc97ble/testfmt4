import uuid

import storage


def save_file(file):
    uploaded_file_id = str(uuid.uuid4())
    path = storage.id_to_path(uploaded_file_id)
    file.save(path)
    return uploaded_file_id
