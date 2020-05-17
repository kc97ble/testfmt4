import os
import uuid
from operator import itemgetter

import storage
import database
import pattern


class TestSuite:
    def __init__(
        self,
        file_id: str,
        pattern_pair: pattern.PatternPair,
        test_id_list: list,
        extra_files: list,
    ):
        self.file_id = file_id
        self.pattern_pair = pattern_pair
        self.test_id_list = test_id_list
        self.extra_files = extra_files

    @classmethod
    def get_test_suite(cls, file_id: str, inp_format: str, out_format: str):
        pattern_pair = pattern.PatternPair.from_string_pair(inp_format, out_format)
        names = storage.get_names_in_archive(file_id)
        test_id_list, extra_files = pattern_pair.matches(
            names, returns="test_id_with_extra_files"
        )
        return cls(file_id, pattern_pair, test_id_list, extra_files)

    def get_name_list(self, add_extra_info=False):
        important_files = []

        for index, t in enumerate(self.test_id_list):
            inp_name = self.pattern_pair.x.get_name(t, index=index, use_index=True)
            out_name = self.pattern_pair.y.get_name(t, index=index, use_index=True)
            important_files.extend([inp_name, out_name])

        result = []

        for name in important_files:
            if add_extra_info:
                result.append({"value": name, "is_extra_file": False})
            else:
                result.append(name)

        for name in self.extra_files:
            if add_extra_info:
                result.append({"value": name, "is_extra_file": True})
            else:
                result.append(name)

        return result


def is_valid_file_type(file_name):
    _, ext = os.path.splitext(file_name)
    return ext in [".zip", ".ZIP"]


def save_file(file):
    file_id = str(uuid.uuid4())
    file_name = file.filename
    if not is_valid_file_type(file_name):
        raise Exception("400: Only ZIP files are supported")
    storage.save_file(file, file_id, file_name)
    return file_id


def preview(params):
    file_id = params["file_id"]
    bif = params["bef_inp_format"]
    bof = params["bef_out_format"]
    aif = params["aft_inp_format"]
    aof = params["aft_out_format"]

    try:
        test_suite = TestSuite.get_test_suite(file_id, bif, bof)
        bef_preview = test_suite.get_name_list(add_extra_info=True)
        try:
            test_suite.pattern_pair = pattern.PatternPair.from_string_pair(aif, aof)
            aft_preview = test_suite.get_name_list(add_extra_info=True)
            return {"bef_preview": bef_preview, "aft_preview": aft_preview}
        except:
            return {"bef_preview": bef_preview, "aft_preview": []}
    except:
        test_suite = TestSuite.get_test_suite(file_id, "*", "*")
        preview = test_suite.get_name_list(add_extra_info=True)
        return {"bef_preview": preview, "aft_preview": []}


def convert(params):
    file_id = params["file_id"]
    bif = params["bef_inp_format"]
    bof = params["bef_out_format"]
    aif = params["aft_inp_format"]
    aof = params["aft_out_format"]
    file_name = params["file_name"]

    if not file_name:
        info = database.get_upload_info(file_id)
        file_name = info["file_name"]

    test_suite = TestSuite.get_test_suite(file_id, bif, bof)
    bef_preview = test_suite.get_name_list()
    test_suite.pattern_pair = pattern.PatternPair.from_string_pair(aif, aof)
    aft_preview = test_suite.get_name_list()

    result = storage.get_renamed_archive(file_id, bef_preview, aft_preview, file_name)
    return result


def prefill(params):
    file_id = params["file_id"]
    info = database.get_upload_info(file_id)

    file_name = info["file_name"]
    names = storage.get_names_in_archive(file_id)
    pattern_pair = pattern.find_best_pattern_pair(names)

    return {
        "file_name": file_name,
        "inp_format": pattern_pair.x.to_string(),
        "out_format": pattern_pair.y.to_string(),
    }


def get_file_name(file_id):
    info = database.get_upload_info(file_id)
    return info["file_name"]


def preview_file(file_id):
    file_name = get_file_name(file_id)
    file_size = storage.get_file_size(file_id)
    names = storage.get_names_in_archive(file_id)
    return {"file_name": file_name, "file_size": file_size, "content": names}
