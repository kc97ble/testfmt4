import uuid
from operator import itemgetter

import storage
import database
import detect


class TestSuiteFormat:
    def __init__(self, inp_format, out_format):
        assert inp_format.count("*") == 1
        assert out_format.count("*") == 1
        self.inp_format = inp_format
        self.out_format = out_format

    def extract_test_id_with_pattern(self, pattern, name):
        prefix_length = pattern.index("*")
        postfix_length = len(pattern) - 1 - prefix_length
        if not name.startswith(pattern[:prefix_length]):
            return None
        if not name.endswith(pattern[-postfix_length:]):
            return None
        return name[prefix_length : len(name) - postfix_length]

    def get_test_id(self, inp_file, out_file):
        inp_id = self.extract_test_id_with_pattern(self.inp_format, inp_file)
        out_id = self.extract_test_id_with_pattern(self.out_format, out_file)
        return inp_id if inp_id is not None and inp_id == out_id else None

    def get_inp_name(self, test_id):
        i = self.inp_format.index("*")
        return self.inp_format[:i] + test_id + self.inp_format[i + 1 :]

    def get_out_name(self, test_id):
        i = self.out_format.index("*")
        return self.out_format[:i] + test_id + self.out_format[i + 1 :]


class TestSuite:
    def __init__(self, file_id, test_suite_format, test_list, extra_files):
        self.file_id = file_id
        self.test_suite_format = test_suite_format
        self.test_list = test_list
        self.extra_files = extra_files

    @classmethod
    def analyze_raw_test_suite(cls, file_id, test_suite_format):
        paths = storage.get_file_list_in_archive(file_id)
        test_list = []
        extra_files = list(paths)

        # this stupid nested loop can be optimized
        for item in paths:
            for jtem in paths:
                if item != jtem:
                    test_id = test_suite_format.get_test_id(item, jtem)
                    if test_id is not None:
                        test_list.append((test_id, item, jtem))
                        extra_files.remove(item)
                        extra_files.remove(jtem)

        return test_list, list(extra_files)

    @classmethod
    def get_test_suite(cls, file_id, inp_format, out_format):
        test_suite_format = TestSuiteFormat(inp_format, out_format)
        test_list, extra_files = TestSuite.analyze_raw_test_suite(
            file_id, test_suite_format
        )
        return TestSuite(file_id, test_suite_format, test_list, extra_files)

    def get_name_list(self, add_extra_info=False):
        important_files = []

        for test in self.test_list:
            test_id, _, _ = test
            inp_name = self.test_suite_format.get_inp_name(test_id)
            out_name = self.test_suite_format.get_out_name(test_id)
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


def save_file(file):
    file_id = str(uuid.uuid4())
    file_name = file.filename
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
            test_suite.test_suite_format = TestSuiteFormat(aif, aof)
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
    test_suite.test_suite_format = TestSuiteFormat(aif, aof)
    aft_preview = test_suite.get_name_list()

    result = storage.get_renamed_archive(file_id, bef_preview, aft_preview, file_name)
    return result


def prefill(params):
    file_id = params["file_id"]
    info = database.get_upload_info(file_id)

    file_name = info["file_name"]
    names = storage.get_file_list_in_archive(file_id)
    inp_format, out_format = detect.find_best_format(names)

    return {
        "file_name": file_name,
        "inp_format": inp_format,
        "out_format": out_format,
    }


def get_file_name(file_id):
    info = database.get_upload_info(file_id)
    return info["file_name"]
