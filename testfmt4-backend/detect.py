# import random

# SAMPLE_SIZE = 16


# class Pattern:
#     def __init__(self, ll, mm, rr):
#         assert mm in ["*", "0", "1", "00", "01", "000", "001", "0000", "0001"]
#         self.ll = ll
#         self.mm = mm
#         self.rr = rr


# def get_all_star_patterns(name):
#     for j in range(len(name) + 1):
#         for i in range(i + 1):
#             Pattern(name[:i], "*", name[j:])
#     return [("", "")]


# def score(x):
#     return 0


def find_best_format(names):
    # sample = random.sample(names, min(len(names), SAMPLE_SIZE))

    # all_potential_format = [
    #     (score(x), x) for name in sample for x in get_all_star_formats(name)
    # ]

    # max_score, best_format = max(all_potential_format)

    # # TODO
    # print("873458346876345843")
    # print(max_score)

    # return best_format
    return ("", "")
