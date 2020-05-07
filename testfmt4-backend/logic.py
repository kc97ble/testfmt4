import uuid
from operator import itemgetter

import storage


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
    def __init__(self, uploaded_file_id, test_suite_format, test_list, extra_files):
        self.uploaded_file_id = uploaded_file_id
        self.test_suite_format = test_suite_format
        self.test_list = test_list
        self.extra_files = extra_files

    @classmethod
    def analyze_raw_test_suite(cls, uploaded_file_id, test_suite_format):
        paths = storage.get_file_list_in_archive(uploaded_file_id)
        test_list = []
        extra_files = set(paths)

        # this stupid nested loop can be optimized
        for item in paths:
            for jtem in paths:
                test_id = test_suite_format.get_test_id(item, jtem)
                if test_id is not None:
                    test_list.append((test_id, item, jtem))
                    extra_files.remove(item)
                    extra_files.remove(jtem)

        return test_list, list(extra_files)

    @classmethod
    def get_test_suite(cls, uploaded_file_id, inp_format, out_format):
        test_suite_format = TestSuiteFormat(inp_format, out_format)
        test_list, extra_files = TestSuite.analyze_raw_test_suite(
            uploaded_file_id, test_suite_format
        )
        return TestSuite(uploaded_file_id, test_suite_format, test_list, extra_files)

    def get_name_list(self):
        result = []
        for test in self.test_list:
            test_id, _, _ = test
            result.append(self.test_suite_format.get_inp_name(test_id))
            result.append(self.test_suite_format.get_out_name(test_id))
        result.extend(self.extra_files)
        return result


def save_file(file):
    uploaded_file_id = str(uuid.uuid4())
    path = storage.id_to_path(uploaded_file_id)
    file.save(path)
    return uploaded_file_id


def preview(params):

    uploaded_file_id = params["uploaded_file_id"]
    bef_inp_format = params["bef_inp_format"]
    bef_out_format = params["bef_out_format"]
    aft_inp_format = params["aft_inp_format"]
    aft_out_format = params["aft_out_format"]

    try:
        test_suite = TestSuite.get_test_suite(
            uploaded_file_id, bef_inp_format, bef_out_format
        )
        bef_preview = test_suite.get_name_list()
        try:
            test_suite.test_suite_format = TestSuiteFormat(
                aft_inp_format, aft_out_format
            )
            aft_preview = test_suite.get_name_list()
            return {"bef_preview": bef_preview, "aft_preview": aft_preview}
        except:
            return {"bef_preview": bef_preview, "aft_preview": []}
    except:
        return {"bef_preview": [], "aft_preview": []}


def convert(params):
    uploaded_file_id = params["uploaded_file_id"]
    bef, aft = itemgetter("bef_preview", "aft_preview")(preview(params))
    result = storage.get_renamed_archive(uploaded_file_id, bef, aft)
    return result
