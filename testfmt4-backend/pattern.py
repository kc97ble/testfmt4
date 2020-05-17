import os
import random
import utils

SAMPLE_SIZE = 16
NUMBERED_MM = ["0", "1", "00", "01", "000", "001", "0000", "0001"]
VALID_MM = ["*"] + NUMBERED_MM

MSG_TOO_MANY_OCCURRENCES = "Invalid pattern: Pattern cannot have more than one '{}'"
MSG_MM_NOT_FOUND = "Invalid pattern: Wildcard not found. Wildcard list: {}"


class Pattern:
    def __init__(self, ll, mm, rr):
        assert mm in VALID_MM
        self.ll = ll
        self.mm = mm
        self.rr = rr

    def __repr__(self):
        return "Pattern('{}', '{}', '{}')".format(self.ll, self.mm, self.rr)

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return self.__repr__().__hash__()

    @classmethod
    def from_string(cls, text):
        for mm in ["*"] + sorted(NUMBERED_MM, key=len, reverse=True):
            if mm in text:
                if text.count(mm) > 1:
                    raise Exception(MSG_TOO_MANY_OCCURRENCES.format(mm))
                i = text.index(mm)
                return cls(text[:i], mm, text[i + len(mm) :])
        raise Exception(MSG_MM_NOT_FOUND, ",".join(VALID_MM))

    def to_string(self):
        return self.ll + self.mm + self.rr

    def is_valid_test_id(self, test_id):
        if self.mm == "*":
            return True
        if self.mm in NUMBERED_MM:
            return test_id.isdigit() and len(test_id) >= len(self.mm)
        raise NotImplementedError

    def matched(self, name):
        return (
            name.startswith(self.ll)
            and name.endswith(self.rr)
            and len(name) >= len(self.ll) + len(self.rr)
            and self.is_valid_test_id(self.get_test_id(name))
        )

    def get_test_id(self, name):
        return name[len(self.ll) : len(name) - len(self.rr)]

    def get_test_id_from_index(self, index):
        assert self.mm in NUMBERED_MM
        return str(int(self.mm) + index).zfill(len(self.mm))

    def get_name(self, test_id, index=None, use_index=False):
        if use_index and self.mm in NUMBERED_MM:
            return self.ll + self.get_test_id_from_index(index) + self.rr
        return self.ll + test_id + self.rr

    def matches(self, names, returns):
        if returns == "test_id":
            result = [n for n in names]
            result = [n for n in result if self.matched(n)]
            result = [self.get_test_id(n) for n in result]
            return result
        else:
            raise NotImplementedError


class PatternPair:
    def __init__(self, x: Pattern, y: Pattern):
        assert x.mm == y.mm
        self.x = x
        self.y = y

    def __repr__(self):
        return "PatternPair({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return self.__repr__().__hash__()

    @classmethod
    def from_string_pair(cls, inp_format, out_format):
        return cls(Pattern.from_string(inp_format), Pattern.from_string(out_format))

    def matches(self, names, returns):
        x_test_ids = self.x.matches(names, returns="test_id")
        y_test_ids = self.y.matches(names, returns="test_id")

        test_ids = set(x_test_ids) & set(y_test_ids)
        test_ids = list(sorted(test_ids, key=utils.natural_sorting_key))

        if returns == "fast_count":
            if self.x.mm == "*":
                return len(test_ids)
            elif self.x.mm in NUMBERED_MM:
                count_valid = 0
                for t in test_ids:
                    if t == self.x.get_test_id_from_index(count_valid):
                        count_valid += 1

                return count_valid

        extra_files = list(names)
        valid_test_ids = []
        for t in test_ids:
            if self.x.mm in NUMBERED_MM:
                if t != self.x.get_test_id_from_index(len(valid_test_ids)):
                    continue

            inp_name = self.x.get_name(t)
            out_name = self.y.get_name(t)

            if inp_name == out_name:
                continue
            if inp_name not in extra_files:
                continue
            if out_name not in extra_files:
                continue

            valid_test_ids.append(t)
            extra_files.remove(inp_name)
            extra_files.remove(out_name)

        if returns == "count":
            return len(valid_test_ids)
        elif returns == "test_id":
            return valid_test_ids
        elif returns == "test_id_with_extra_files":
            return valid_test_ids, extra_files
        else:
            raise NotImplementedError

    def score(self, names):
        def ls(s):
            return len(s) - s.count("0")

        def zs(s):
            return -s.count("0")

        def vs(s):
            return sum(
                s.lower().count(c) * w
                for c, w in [("a", -1), ("e", -1), ("i", +1), ("o", -1), ("u", -1)]
            )

        count_score = self.matches(names, returns="fast_count")

        len_score = ls(self.x.ll + self.x.rr + self.y.ll + self.y.rr)
        zero_score = zs(self.x.ll + self.x.rr + self.y.ll + self.y.rr)

        assert self.x.mm in ["*"] + NUMBERED_MM
        specific_score = 0 if self.x.mm == "*" else len(self.x.mm)

        vowel_score = vs(self.x.ll + self.x.rr) - vs(self.y.ll + self.y.rr)

        return count_score, specific_score, len_score, zero_score, vowel_score

    def is_string_safe(self):
        try:
            x = Pattern.from_string(self.x.to_string())
            y = Pattern.from_string(self.y.to_string())
            return self == PatternPair(x, y)
        except:
            return False


def maximal(a, key):
    max_score = max(map(key, a))
    result = [x for x in a if key(x) == max_score]
    if len(result) == 1:
        return result[0]
    else:
        print(result)
        raise Exception("More than one maximum values")


def get_all_star_pattern_pairs(names):
    sample = random.sample(names, min(len(names), SAMPLE_SIZE))

    star_pattern_pairs = []

    all_prefixes = [n[:i] for n in sample for i in range(len(n) + 1)]
    all_prefixes = list(sorted(set(all_prefixes)))
    all_suffixes = [n[i:] for n in sample for i in range(len(n) + 1)]
    all_suffixes = list(sorted(set(all_suffixes)))

    for prefix in all_prefixes:
        matched_names = [n for n in names if n.startswith(prefix)]
        if len(matched_names) == 2:
            mn0, mn1 = matched_names
            for i in range(len(prefix) + 1):
                x = Pattern(prefix[:i], "*", mn0[len(prefix) :])
                y = Pattern(prefix[:i], "*", mn1[len(prefix) :])
                star_pattern_pairs.append(PatternPair(x, y))

    for suffix in all_suffixes:
        matched_names = [n for n in names if n.endswith(suffix)]
        if len(matched_names) == 2:
            mn0, mn1 = matched_names
            for i in range(len(suffix) + 1):
                x = Pattern(mn0[: len(mn0) - len(suffix)], "*", suffix[i:])
                y = Pattern(mn1[: len(mn1) - len(suffix)], "*", suffix[i:])
                star_pattern_pairs.append(PatternPair(x, y))

    star_pattern_pairs = list(set(star_pattern_pairs))
    return star_pattern_pairs


def get_variant_pattern_pairs(pp):
    return [
        PatternPair(Pattern(pp.x.ll, mm, pp.x.rr), Pattern(pp.y.ll, mm, pp.y.rr))
        for mm in VALID_MM
    ] + [
        PatternPair(Pattern(pp.y.ll, mm, pp.y.rr), Pattern(pp.x.ll, mm, pp.x.rr))
        for mm in VALID_MM
    ]


def find_best_pattern_pair(names):
    star_pattern_pairs = get_all_star_pattern_pairs(names)
    star_pattern_pairs = [
        pp for pp in star_pattern_pairs if pp.matches(names, returns="fast_count") >= 2
    ]
    # for pp in star_pattern_pairs:
    #     print(pp, pp.is_string_safe(), pp.score(names))

    if len(star_pattern_pairs) == 0:
        return PatternPair(Pattern("", "*", ""), Pattern("", "*", ""))
    best_star_pattern_pair = maximal(star_pattern_pairs, key=lambda pp: pp.score(names))

    pattern_pairs = get_variant_pattern_pairs(best_star_pattern_pair)
    # for pp in pattern_pairs:
    #     print(pp, pp.is_string_safe(), pp.score(names))
    pattern_pairs = [pp for pp in pattern_pairs if pp.is_string_safe()]
    best_pattern_pair = maximal(pattern_pairs, key=lambda pp: pp.score(names))

    return best_pattern_pair


def list_dir_recursively(folder):
    old_cwd = os.getcwd()
    os.chdir(folder)
    result = []
    for root, _, filenames in os.walk("."):
        for filename in filenames:
            result.append(os.path.join(root, filename))
    os.chdir(old_cwd)
    return result


def test_with_dir(folder):
    names = list_dir_recursively(folder)
    print(folder, find_best_pattern_pair(names))


if __name__ == "__main__":
    # test_with_dir("/mnt/NTFS/Problems 2016/3circles")
    # test_with_dir("/mnt/NTFS/Problems 2016/511")
    # test_with_dir("/mnt/NTFS/Problems 2016/A007")
    test_with_dir("/mnt/NTFS/Problems 2016/abc")
    test_with_dir("/mnt/NTFS/Problems 2016/accepted")
    test_with_dir("/mnt/NTFS/Problems 2016/acquire")
    test_with_dir("/mnt/NTFS/Problems 2016/adict")
    test_with_dir("/mnt/NTFS/Problems 2016/adn")
    test_with_dir("/mnt/NTFS/Problems 2016/afarm")
    test_with_dir("/mnt/NTFS/Problems 2016/aggressivecows")
    test_with_dir("/mnt/NTFS/Problems 2016/airline")
    test_with_dir("/mnt/NTFS/Problems 2016/aiwar")
    test_with_dir("/mnt/NTFS/Problems 2016/albinuta")
    test_with_dir("/mnt/NTFS/Problems 2016/alley")
    test_with_dir("/mnt/NTFS/Problems 2016/alliances")
    test_with_dir("/mnt/NTFS/Problems 2016/amusing")
    test_with_dir("/mnt/NTFS/Problems 2016/anbinh")
    test_with_dir("/mnt/NTFS/Problems 2016/apple")
    test_with_dir("/mnt/NTFS/Problems 2016/arbore")
    test_with_dir("/mnt/NTFS/Problems 2016/ascii")
    test_with_dir("/mnt/NTFS/Problems 2016/atm")
    test_with_dir("/mnt/NTFS/Problems 2016/attract")
    test_with_dir("/mnt/NTFS/Problems 2016/authen")
    test_with_dir("/mnt/NTFS/Problems 2016/automaton")
    test_with_dir("/mnt/NTFS/Problems 2016/avatar")
    test_with_dir("/mnt/NTFS/Problems 2016/babylontower")
    test_with_dir("/mnt/NTFS/Problems 2016/ball")
    test_with_dir("/mnt/NTFS/Problems 2016/balstring")
    test_with_dir("/mnt/NTFS/Problems 2016/bamboos")
    test_with_dir("/mnt/NTFS/Problems 2016/bandyta")
    test_with_dir("/mnt/NTFS/Problems 2016/barons")
    test_with_dir("/mnt/NTFS/Problems 2016/bcl")
    test_with_dir("/mnt/NTFS/Problems 2016/beads")
    test_with_dir("/mnt/NTFS/Problems 2016/bfs1")
    test_with_dir("/mnt/NTFS/Problems 2016/bfs2")
    test_with_dir("/mnt/NTFS/Problems 2016/bgame")
    test_with_dir("/mnt/NTFS/Problems 2016/bgame1")
    test_with_dir("/mnt/NTFS/Problems 2016/bgame2")
    test_with_dir("/mnt/NTFS/Problems 2016/bila")
    test_with_dir("/mnt/NTFS/Problems 2016/bill")
    test_with_dir("/mnt/NTFS/Problems 2016/billboard8")
    test_with_dir("/mnt/NTFS/Problems 2016/binary")
    test_with_dir("/mnt/NTFS/Problems 2016/bit1")
    test_with_dir("/mnt/NTFS/Problems 2016/bitstr")
    test_with_dir("/mnt/NTFS/Problems 2016/block")
    test_with_dir("/mnt/NTFS/Problems 2016/BLUZIIUM")
    test_with_dir("/mnt/NTFS/Problems 2016/bnwnim")
    test_with_dir("/mnt/NTFS/Problems 2016/board")
    test_with_dir("/mnt/NTFS/Problems 2016/bookcase")
    test_with_dir("/mnt/NTFS/Problems 2016/boundary")
    test_with_dir("/mnt/NTFS/Problems 2016/bowling")
    test_with_dir("/mnt/NTFS/Problems 2016/brackets")
    test_with_dir("/mnt/NTFS/Problems 2016/bseq")
    test_with_dir("/mnt/NTFS/Problems 2016/bsf")
    test_with_dir("/mnt/NTFS/Problems 2016/btn")
    test_with_dir("/mnt/NTFS/Problems 2016/btn2")
    test_with_dir("/mnt/NTFS/Problems 2016/btree")
    test_with_dir("/mnt/NTFS/Problems 2016/buffalo")
    test_with_dir("/mnt/NTFS/Problems 2016/bumeran")
    test_with_dir("/mnt/NTFS/Problems 2016/bus")
    test_with_dir("/mnt/NTFS/Problems 2016/cactus")
    test_with_dir("/mnt/NTFS/Problems 2016/cake")
    test_with_dir("/mnt/NTFS/Problems 2016/cakes (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/cakes (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/cakes (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/camp")
    test_with_dir("/mnt/NTFS/Problems 2016/candies")
    test_with_dir("/mnt/NTFS/Problems 2016/candy")
    test_with_dir("/mnt/NTFS/Problems 2016/cap")
    test_with_dir("/mnt/NTFS/Problems 2016/cardgame")
    test_with_dir("/mnt/NTFS/Problems 2016/cardrm")
    test_with_dir("/mnt/NTFS/Problems 2016/casino")
    test_with_dir("/mnt/NTFS/Problems 2016/cchange")
    test_with_dir("/mnt/NTFS/Problems 2016/cdc")
    test_with_dir("/mnt/NTFS/Problems 2016/cellphone")
    test_with_dir("/mnt/NTFS/Problems 2016/charm")
    test_with_dir("/mnt/NTFS/Problems 2016/cheat (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/cheat (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/cheat (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/chefduel")
    test_with_dir("/mnt/NTFS/Problems 2016/chess")
    test_with_dir("/mnt/NTFS/Problems 2016/chess (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/chips")
    test_with_dir("/mnt/NTFS/Problems 2016/chk")
    test_with_dir("/mnt/NTFS/Problems 2016/circles")
    test_with_dir("/mnt/NTFS/Problems 2016/clis")
    test_with_dir("/mnt/NTFS/Problems 2016/cmp")
    test_with_dir("/mnt/NTFS/Problems 2016/cng")
    test_with_dir("/mnt/NTFS/Problems 2016/cngame")
    test_with_dir("/mnt/NTFS/Problems 2016/cnt")
    test_with_dir("/mnt/NTFS/Problems 2016/coins (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/coins (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/color (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/color (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/color (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/coltri")
    test_with_dir("/mnt/NTFS/Problems 2016/combsort")
    test_with_dir("/mnt/NTFS/Problems 2016/commando")
    test_with_dir("/mnt/NTFS/Problems 2016/contest (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/contest (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/contest (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/convention")
    test_with_dir("/mnt/NTFS/Problems 2016/counttree")
    test_with_dir("/mnt/NTFS/Problems 2016/cowrun")
    test_with_dir("/mnt/NTFS/Problems 2016/cp")
    test_with_dir("/mnt/NTFS/Problems 2016/cr")
    test_with_dir("/mnt/NTFS/Problems 2016/crec01")
    test_with_dir("/mnt/NTFS/Problems 2016/cstr")
    test_with_dir("/mnt/NTFS/Problems 2016/ctravel")
    test_with_dir("/mnt/NTFS/Problems 2016/cuiburi")
    test_with_dir("/mnt/NTFS/Problems 2016/curent")
    test_with_dir("/mnt/NTFS/Problems 2016/cxy")
    test_with_dir("/mnt/NTFS/Problems 2016/cylinders")
    test_with_dir("/mnt/NTFS/Problems 2016/dartz")
    test_with_dir("/mnt/NTFS/Problems 2016/debug")
    test_with_dir("/mnt/NTFS/Problems 2016/dejavu")
    test_with_dir("/mnt/NTFS/Problems 2016/del")
    test_with_dir("/mnt/NTFS/Problems 2016/delivery")
    test_with_dir("/mnt/NTFS/Problems 2016/delivery (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/desert")
    test_with_dir("/mnt/NTFS/Problems 2016/diamond")
    test_with_dir("/mnt/NTFS/Problems 2016/dice")
    test_with_dir("/mnt/NTFS/Problems 2016/dictionary")
    test_with_dir("/mnt/NTFS/Problems 2016/difference")
    test_with_dir("/mnt/NTFS/Problems 2016/digits")
    test_with_dir("/mnt/NTFS/Problems 2016/digits (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/diningb")
    test_with_dir("/mnt/NTFS/Problems 2016/disjointset1")
    test_with_dir("/mnt/NTFS/Problems 2016/dispatching")
    # test_with_dir("/mnt/NTFS/Problems 2016/div") # INVALID
    test_with_dir("/mnt/NTFS/Problems 2016/divisors")
    test_with_dir("/mnt/NTFS/Problems 2016/dna")
    test_with_dir("/mnt/NTFS/Problems 2016/dominance")
    test_with_dir("/mnt/NTFS/Problems 2016/domino")
    test_with_dir("/mnt/NTFS/Problems 2016/dry")
    test_with_dir("/mnt/NTFS/Problems 2016/dseq")
    test_with_dir("/mnt/NTFS/Problems 2016/ecircle")
    test_with_dir("/mnt/NTFS/Problems 2016/egroup")
    test_with_dir("/mnt/NTFS/Problems 2016/electric")
    test_with_dir("/mnt/NTFS/Problems 2016/elephant")
    test_with_dir("/mnt/NTFS/Problems 2016/embroidery")
    test_with_dir("/mnt/NTFS/Problems 2016/encoding")
    test_with_dir("/mnt/NTFS/Problems 2016/encoding (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/equivalence")
    test_with_dir("/mnt/NTFS/Problems 2016/errant")
    test_with_dir("/mnt/NTFS/Problems 2016/ests")
    test_with_dir("/mnt/NTFS/Problems 2016/eulertour")
    test_with_dir("/mnt/NTFS/Problems 2016/eureka")
    test_with_dir("/mnt/NTFS/Problems 2016/exactone")
    test_with_dir("/mnt/NTFS/Problems 2016/exam")
    test_with_dir("/mnt/NTFS/Problems 2016/exam (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/exercise")
    test_with_dir("/mnt/NTFS/Problems 2016/expectedsum")
    test_with_dir("/mnt/NTFS/Problems 2016/explore")
    test_with_dir("/mnt/NTFS/Problems 2016/expstr")
    test_with_dir("/mnt/NTFS/Problems 2016/extreme")
    test_with_dir("/mnt/NTFS/Problems 2016/factor")
    test_with_dir("/mnt/NTFS/Problems 2016/fence")
    test_with_dir("/mnt/NTFS/Problems 2016/festival")
    test_with_dir("/mnt/NTFS/Problems 2016/fib2")
    test_with_dir("/mnt/NTFS/Problems 2016/fibonacci")
    test_with_dir("/mnt/NTFS/Problems 2016/fire")
    test_with_dir("/mnt/NTFS/Problems 2016/flies")
    test_with_dir("/mnt/NTFS/Problems 2016/flori")
    test_with_dir("/mnt/NTFS/Problems 2016/fontan")
    test_with_dir("/mnt/NTFS/Problems 2016/format1")
    test_with_dir("/mnt/NTFS/Problems 2016/fourblocks")
    test_with_dir("/mnt/NTFS/Problems 2016/fox")
    test_with_dir("/mnt/NTFS/Problems 2016/foxbomb")
    test_with_dir("/mnt/NTFS/Problems 2016/frac")
    test_with_dir("/mnt/NTFS/Problems 2016/free")
    test_with_dir("/mnt/NTFS/Problems 2016/freebus")
    test_with_dir("/mnt/NTFS/Problems 2016/function")
    test_with_dir("/mnt/NTFS/Problems 2016/FVZVBYUL")
    test_with_dir("/mnt/NTFS/Problems 2016/game (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/game (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/games")
    test_with_dir("/mnt/NTFS/Problems 2016/garden")
    test_with_dir("/mnt/NTFS/Problems 2016/garden (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/gather")
    test_with_dir("/mnt/NTFS/Problems 2016/gattaca")
    test_with_dir("/mnt/NTFS/Problems 2016/gcd50")
    test_with_dir("/mnt/NTFS/Problems 2016/gcdlcm")
    test_with_dir("/mnt/NTFS/Problems 2016/gcitp")
    test_with_dir("/mnt/NTFS/Problems 2016/gems")
    test_with_dir("/mnt/NTFS/Problems 2016/gift")
    test_with_dir("/mnt/NTFS/Problems 2016/grading")
    test_with_dir("/mnt/NTFS/Problems 2016/graph")
    test_with_dir("/mnt/NTFS/Problems 2016/graph1")
    test_with_dir("/mnt/NTFS/Problems 2016/growth")
    test_with_dir("/mnt/NTFS/Problems 2016/guard")
    test_with_dir("/mnt/NTFS/Problems 2016/guess")
    test_with_dir("/mnt/NTFS/Problems 2016/hack")
    test_with_dir("/mnt/NTFS/Problems 2016/hamilton")
    test_with_dir("/mnt/NTFS/Problems 2016/hanoi")
    test_with_dir("/mnt/NTFS/Problems 2016/hapmap")
    test_with_dir("/mnt/NTFS/Problems 2016/hapnum")
    test_with_dir("/mnt/NTFS/Problems 2016/hexanet")
    test_with_dir("/mnt/NTFS/Problems 2016/highway")
    test_with_dir("/mnt/NTFS/Problems 2016/highway (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/hon")
    test_with_dir("/mnt/NTFS/Problems 2016/horror")
    test_with_dir("/mnt/NTFS/Problems 2016/house")
    test_with_dir("/mnt/NTFS/Problems 2016/hrpa")
    test_with_dir("/mnt/NTFS/Problems 2016/hstr")
    test_with_dir("/mnt/NTFS/Problems 2016/htab")
    test_with_dir("/mnt/NTFS/Problems 2016/hurdles")
    test_with_dir("/mnt/NTFS/Problems 2016/ibs")
    test_with_dir("/mnt/NTFS/Problems 2016/imgame")
    test_with_dir("/mnt/NTFS/Problems 2016/invasion")
    test_with_dir("/mnt/NTFS/Problems 2016/irrev")
    test_with_dir("/mnt/NTFS/Problems 2016/its")
    test_with_dir("/mnt/NTFS/Problems 2016/izbori")
    test_with_dir("/mnt/NTFS/Problems 2016/jewel")
    test_with_dir("/mnt/NTFS/Problems 2016/job")
    test_with_dir("/mnt/NTFS/Problems 2016/jumper")
    test_with_dir("/mnt/NTFS/Problems 2016/justinbieber")
    test_with_dir("/mnt/NTFS/Problems 2016/kdigit")
    test_with_dir("/mnt/NTFS/Problems 2016/keyboard")
    test_with_dir("/mnt/NTFS/Problems 2016/kid")
    test_with_dir("/mnt/NTFS/Problems 2016/kingdomdefense")
    test_with_dir("/mnt/NTFS/Problems 2016/knapsack")
    test_with_dir("/mnt/NTFS/Problems 2016/knight")
    test_with_dir("/mnt/NTFS/Problems 2016/ksteps")
    test_with_dir("/mnt/NTFS/Problems 2016/kwadrat")
    test_with_dir("/mnt/NTFS/Problems 2016/L")
    test_with_dir("/mnt/NTFS/Problems 2016/lake")
    test_with_dir("/mnt/NTFS/Problems 2016/lamp")
    test_with_dir("/mnt/NTFS/Problems 2016/land")
    test_with_dir("/mnt/NTFS/Problems 2016/lane")
    test_with_dir("/mnt/NTFS/Problems 2016/lcm")
    test_with_dir("/mnt/NTFS/Problems 2016/lcmset")
    test_with_dir("/mnt/NTFS/Problems 2016/lcrle")
    test_with_dir("/mnt/NTFS/Problems 2016/lcs")
    test_with_dir("/mnt/NTFS/Problems 2016/leastturn")
    test_with_dir("/mnt/NTFS/Problems 2016/LGKZOBGA")
    test_with_dir("/mnt/NTFS/Problems 2016/light")
    test_with_dir("/mnt/NTFS/Problems 2016/light (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/lin")
    test_with_dir("/mnt/NTFS/Problems 2016/line")
    test_with_dir("/mnt/NTFS/Problems 2016/lines")
    test_with_dir("/mnt/NTFS/Problems 2016/lis3")
    test_with_dir("/mnt/NTFS/Problems 2016/lll")
    test_with_dir("/mnt/NTFS/Problems 2016/lock")
    test_with_dir("/mnt/NTFS/Problems 2016/loco")
    test_with_dir("/mnt/NTFS/Problems 2016/longqueue")
    test_with_dir("/mnt/NTFS/Problems 2016/lotarie")
    test_with_dir("/mnt/NTFS/Problems 2016/lpass")
    test_with_dir("/mnt/NTFS/Problems 2016/lrec")
    test_with_dir("/mnt/NTFS/Problems 2016/lthcards")
    test_with_dir("/mnt/NTFS/Problems 2016/lthcars")
    test_with_dir("/mnt/NTFS/Problems 2016/lthconnect")
    test_with_dir("/mnt/NTFS/Problems 2016/lthdna")
    test_with_dir("/mnt/NTFS/Problems 2016/lthmaterial")
    test_with_dir("/mnt/NTFS/Problems 2016/lthmax")
    test_with_dir("/mnt/NTFS/Problems 2016/lthnum")
    test_with_dir("/mnt/NTFS/Problems 2016/lthones")
    test_with_dir("/mnt/NTFS/Problems 2016/lthterror")
    test_with_dir("/mnt/NTFS/Problems 2016/lucky")
    test_with_dir("/mnt/NTFS/Problems 2016/lucky2")
    test_with_dir("/mnt/NTFS/Problems 2016/lucky3")
    test_with_dir("/mnt/NTFS/Problems 2016/M")
    test_with_dir("/mnt/NTFS/Problems 2016/matchup")
    test_with_dir("/mnt/NTFS/Problems 2016/matrice")
    test_with_dir("/mnt/NTFS/Problems 2016/matrix")
    test_with_dir("/mnt/NTFS/Problems 2016/maxgift")
    test_with_dir("/mnt/NTFS/Problems 2016/maze")
    test_with_dir("/mnt/NTFS/Problems 2016/mecho")
    test_with_dir("/mnt/NTFS/Problems 2016/meetingpoint")
    test_with_dir("/mnt/NTFS/Problems 2016/message")
    test_with_dir("/mnt/NTFS/Problems 2016/meteor")
    test_with_dir("/mnt/NTFS/Problems 2016/milkprod")
    test_with_dir("/mnt/NTFS/Problems 2016/miners")
    test_with_dir("/mnt/NTFS/Problems 2016/mines")
    test_with_dir("/mnt/NTFS/Problems 2016/minlex2")
    test_with_dir("/mnt/NTFS/Problems 2016/minroute")
    test_with_dir("/mnt/NTFS/Problems 2016/MNIAOCKW")
    test_with_dir("/mnt/NTFS/Problems 2016/move")
    test_with_dir("/mnt/NTFS/Problems 2016/mowlawn")
    test_with_dir("/mnt/NTFS/Problems 2016/mtime")
    test_with_dir("/mnt/NTFS/Problems 2016/mud")
    test_with_dir("/mnt/NTFS/Problems 2016/mutation")
    test_with_dir("/mnt/NTFS/Problems 2016/naming")
    test_with_dir("/mnt/NTFS/Problems 2016/naw")
    test_with_dir("/mnt/NTFS/Problems 2016/nbs")
    test_with_dir("/mnt/NTFS/Problems 2016/ndoku")
    test_with_dir("/mnt/NTFS/Problems 2016/ndoku (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/newabc")
    test_with_dir("/mnt/NTFS/Problems 2016/nightwatch")
    test_with_dir("/mnt/NTFS/Problems 2016/ninja")
    test_with_dir("/mnt/NTFS/Problems 2016/NKXCVYNV")
    test_with_dir("/mnt/NTFS/Problems 2016/nqueen")
    test_with_dir("/mnt/NTFS/Problems 2016/ntrees")
    test_with_dir("/mnt/NTFS/Problems 2016/number (1)")
    test_with_dir("/mnt/NTFS/Problems 2016/number (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/number (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/numere")
    test_with_dir("/mnt/NTFS/Problems 2016/numways")
    test_with_dir("/mnt/NTFS/Problems 2016/nzsum")
    test_with_dir("/mnt/NTFS/Problems 2016/odd")
    test_with_dir("/mnt/NTFS/Problems 2016/operation")
    test_with_dir("/mnt/NTFS/Problems 2016/order")
    test_with_dir("/mnt/NTFS/Problems 2016/order (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/P")
    test_with_dir("/mnt/NTFS/Problems 2016/paintab")
    test_with_dir("/mnt/NTFS/Problems 2016/palincut")
    test_with_dir("/mnt/NTFS/Problems 2016/palindrome")
    test_with_dir("/mnt/NTFS/Problems 2016/palindromes")
    test_with_dir("/mnt/NTFS/Problems 2016/palinez")
    test_with_dir("/mnt/NTFS/Problems 2016/palinn")
    test_with_dir("/mnt/NTFS/Problems 2016/parking")
    test_with_dir("/mnt/NTFS/Problems 2016/partition")
    test_with_dir("/mnt/NTFS/Problems 2016/password")
    test_with_dir("/mnt/NTFS/Problems 2016/path")
    test_with_dir("/mnt/NTFS/Problems 2016/path (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/patheads")
    test_with_dir("/mnt/NTFS/Problems 2016/patrol")
    test_with_dir("/mnt/NTFS/Problems 2016/patrol (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/penguins")
    test_with_dir("/mnt/NTFS/Problems 2016/penguins (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/perfect")
    test_with_dir("/mnt/NTFS/Problems 2016/perimeter")
    test_with_dir("/mnt/NTFS/Problems 2016/period")
    test_with_dir("/mnt/NTFS/Problems 2016/perm7")
    test_with_dir("/mnt/NTFS/Problems 2016/pets")
    test_with_dir("/mnt/NTFS/Problems 2016/phoneline")
    test_with_dir("/mnt/NTFS/Problems 2016/photo")
    test_with_dir("/mnt/NTFS/Problems 2016/pickup")
    test_with_dir("/mnt/NTFS/Problems 2016/pikachu")
    # test_with_dir("/mnt/NTFS/Problems 2016/pin") # SPECIAL
    test_with_dir("/mnt/NTFS/Problems 2016/pinetree")
    test_with_dir("/mnt/NTFS/Problems 2016/points")
    test_with_dir("/mnt/NTFS/Problems 2016/poly")
    test_with_dir("/mnt/NTFS/Problems 2016/portunol")
    test_with_dir("/mnt/NTFS/Problems 2016/poslozi")
    test_with_dir("/mnt/NTFS/Problems 2016/pour")
    test_with_dir("/mnt/NTFS/Problems 2016/power")
    test_with_dir("/mnt/NTFS/Problems 2016/problem")
    test_with_dir("/mnt/NTFS/Problems 2016/profit")
    test_with_dir("/mnt/NTFS/Problems 2016/protest")
    test_with_dir("/mnt/NTFS/Problems 2016/ptrang")
    test_with_dir("/mnt/NTFS/Problems 2016/pub1")
    test_with_dir("/mnt/NTFS/Problems 2016/pub2")
    test_with_dir("/mnt/NTFS/Problems 2016/pviz")
    test_with_dir("/mnt/NTFS/Problems 2016/pw")
    test_with_dir("/mnt/NTFS/Problems 2016/qbpizza")
    test_with_dir("/mnt/NTFS/Problems 2016/qlkho")
    test_with_dir("/mnt/NTFS/Problems 2016/race (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/racing")
    test_with_dir("/mnt/NTFS/Problems 2016/randl")
    test_with_dir("/mnt/NTFS/Problems 2016/ranking")
    test_with_dir("/mnt/NTFS/Problems 2016/read")
    test_with_dir("/mnt/NTFS/Problems 2016/recruit")
    test_with_dir("/mnt/NTFS/Problems 2016/reinvent")
    test_with_dir("/mnt/NTFS/Problems 2016/remsqr")
    test_with_dir("/mnt/NTFS/Problems 2016/review")
    test_with_dir("/mnt/NTFS/Problems 2016/revolutie")
    test_with_dir("/mnt/NTFS/Problems 2016/ricehub")
    test_with_dir("/mnt/NTFS/Problems 2016/river")
    test_with_dir("/mnt/NTFS/Problems 2016/rlestr")
    test_with_dir("/mnt/NTFS/Problems 2016/roads")
    test_with_dir("/mnt/NTFS/Problems 2016/roads (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/robot")
    test_with_dir("/mnt/NTFS/Problems 2016/robots")
    test_with_dir("/mnt/NTFS/Problems 2016/rocks")
    test_with_dir("/mnt/NTFS/Problems 2016/rook1")
    test_with_dir("/mnt/NTFS/Problems 2016/rook2")
    test_with_dir("/mnt/NTFS/Problems 2016/rooks")
    test_with_dir("/mnt/NTFS/Problems 2016/rotate")
    test_with_dir("/mnt/NTFS/Problems 2016/routing")
    test_with_dir("/mnt/NTFS/Problems 2016/rselect")
    test_with_dir("/mnt/NTFS/Problems 2016/run")
    test_with_dir("/mnt/NTFS/Problems 2016/salary")
    test_with_dir("/mnt/NTFS/Problems 2016/scanner")
    test_with_dir("/mnt/NTFS/Problems 2016/seat")
    test_with_dir("/mnt/NTFS/Problems 2016/seating")
    test_with_dir("/mnt/NTFS/Problems 2016/seed")
    test_with_dir("/mnt/NTFS/Problems 2016/seg1")
    test_with_dir("/mnt/NTFS/Problems 2016/seg2")
    test_with_dir("/mnt/NTFS/Problems 2016/segments")
    test_with_dir("/mnt/NTFS/Problems 2016/sellgold")
    test_with_dir("/mnt/NTFS/Problems 2016/seq")
    test_with_dir("/mnt/NTFS/Problems 2016/seq (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/seq (4)")
    test_with_dir("/mnt/NTFS/Problems 2016/seq5ic")
    test_with_dir("/mnt/NTFS/Problems 2016/seq6")
    test_with_dir("/mnt/NTFS/Problems 2016/sequence")
    test_with_dir("/mnt/NTFS/Problems 2016/service")
    test_with_dir("/mnt/NTFS/Problems 2016/shark")
    test_with_dir("/mnt/NTFS/Problems 2016/shelf2")
    test_with_dir("/mnt/NTFS/Problems 2016/sibice")
    test_with_dir("/mnt/NTFS/Problems 2016/sieuthi")
    test_with_dir("/mnt/NTFS/Problems 2016/sight")
    test_with_dir("/mnt/NTFS/Problems 2016/signaling")
    test_with_dir("/mnt/NTFS/Problems 2016/simplefactor")
    test_with_dir("/mnt/NTFS/Problems 2016/sirag")
    test_with_dir("/mnt/NTFS/Problems 2016/soi")
    test_with_dir("/mnt/NTFS/Problems 2016/sort")
    test_with_dir("/mnt/NTFS/Problems 2016/spec")
    test_with_dir("/mnt/NTFS/Problems 2016/speed")
    test_with_dir("/mnt/NTFS/Problems 2016/sqgame")
    test_with_dir("/mnt/NTFS/Problems 2016/sqgarden")
    test_with_dir("/mnt/NTFS/Problems 2016/square")
    test_with_dir("/mnt/NTFS/Problems 2016/ssort")
    test_with_dir("/mnt/NTFS/Problems 2016/stablenum")
    test_with_dir("/mnt/NTFS/Problems 2016/stair")
    test_with_dir("/mnt/NTFS/Problems 2016/step")
    test_with_dir("/mnt/NTFS/Problems 2016/stones")
    test_with_dir("/mnt/NTFS/Problems 2016/stop")
    test_with_dir("/mnt/NTFS/Problems 2016/strcomp")
    test_with_dir("/mnt/NTFS/Problems 2016/strgcut")
    test_with_dir("/mnt/NTFS/Problems 2016/string")
    test_with_dir("/mnt/NTFS/Problems 2016/string (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/submatrix")
    test_with_dir("/mnt/NTFS/Problems 2016/subseq1")
    test_with_dir("/mnt/NTFS/Problems 2016/subseq2")
    test_with_dir("/mnt/NTFS/Problems 2016/subtri")
    test_with_dir("/mnt/NTFS/Problems 2016/subway")
    test_with_dir("/mnt/NTFS/Problems 2016/sum")
    test_with_dir("/mnt/NTFS/Problems 2016/sum (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/sum2d")
    test_with_dir("/mnt/NTFS/Problems 2016/sum2n")
    test_with_dir("/mnt/NTFS/Problems 2016/sumez")
    test_with_dir("/mnt/NTFS/Problems 2016/sumsquare")
    test_with_dir("/mnt/NTFS/Problems 2016/sumxorez")
    test_with_dir("/mnt/NTFS/Problems 2016/table")
    test_with_dir("/mnt/NTFS/Problems 2016/tableletter")
    # test_with_dir("/mnt/NTFS/Problems 2016/taskauthor")  # SPECIAL
    test_with_dir("/mnt/NTFS/Problems 2016/tdepth")
    test_with_dir("/mnt/NTFS/Problems 2016/teams")
    test_with_dir("/mnt/NTFS/Problems 2016/tele")
    test_with_dir("/mnt/NTFS/Problems 2016/telefon")
    test_with_dir("/mnt/NTFS/Problems 2016/telewire")
    test_with_dir("/mnt/NTFS/Problems 2016/terenuri")
    test_with_dir("/mnt/NTFS/Problems 2016/teroristi")
    test_with_dir("/mnt/NTFS/Problems 2016/test")
    test_with_dir("/mnt/NTFS/Problems 2016/tgame")
    test_with_dir("/mnt/NTFS/Problems 2016/theater")
    test_with_dir("/mnt/NTFS/Problems 2016/threat")
    test_with_dir("/mnt/NTFS/Problems 2016/ticket")
    test_with_dir("/mnt/NTFS/Problems 2016/timer")
    test_with_dir("/mnt/NTFS/Problems 2016/toll")
    test_with_dir("/mnt/NTFS/Problems 2016/tour")
    test_with_dir("/mnt/NTFS/Problems 2016/traffic")
    test_with_dir("/mnt/NTFS/Problems 2016/traffic (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/transform")
    test_with_dir("/mnt/NTFS/Problems 2016/travel")
    test_with_dir("/mnt/NTFS/Problems 2016/travel (2)")
    test_with_dir("/mnt/NTFS/Problems 2016/travel (3)")
    test_with_dir("/mnt/NTFS/Problems 2016/treasure")
    test_with_dir("/mnt/NTFS/Problems 2016/tree")
    test_with_dir("/mnt/NTFS/Problems 2016/treeline")
    test_with_dir("/mnt/NTFS/Problems 2016/treeline2")
    test_with_dir("/mnt/NTFS/Problems 2016/trees")
    test_with_dir("/mnt/NTFS/Problems 2016/trian")
    test_with_dir("/mnt/NTFS/Problems 2016/triangle")
    test_with_dir("/mnt/NTFS/Problems 2016/tribonacci")
    test_with_dir("/mnt/NTFS/Problems 2016/tricount")
    test_with_dir("/mnt/NTFS/Problems 2016/triple")
    test_with_dir("/mnt/NTFS/Problems 2016/trisub")
    test_with_dir("/mnt/NTFS/Problems 2016/trojke")
    test_with_dir("/mnt/NTFS/Problems 2016/twoarray")
    test_with_dir("/mnt/NTFS/Problems 2016/twocolor")
    test_with_dir("/mnt/NTFS/Problems 2016/UJAJWRBD")
    test_with_dir("/mnt/NTFS/Problems 2016/UKGMARRG")
    test_with_dir("/mnt/NTFS/Problems 2016/vending")
    test_with_dir("/mnt/NTFS/Problems 2016/vote")
    test_with_dir("/mnt/NTFS/Problems 2016/VZOVQAXR")
    test_with_dir("/mnt/NTFS/Problems 2016/wasbrac")
    test_with_dir("/mnt/NTFS/Problems 2016/wealthy")
    test_with_dir("/mnt/NTFS/Problems 2016/weather")
    test_with_dir("/mnt/NTFS/Problems 2016/weight")
    test_with_dir("/mnt/NTFS/Problems 2016/wg")
    test_with_dir("/mnt/NTFS/Problems 2016/wordpow")
    test_with_dir("/mnt/NTFS/Problems 2016/WTLWPIJV")
    test_with_dir("/mnt/NTFS/Problems 2016/xgame")
    test_with_dir("/mnt/NTFS/Problems 2016/xor")
    test_with_dir("/mnt/NTFS/Problems 2016/XOR")
    test_with_dir("/mnt/NTFS/Problems 2016/xyz")
    test_with_dir("/mnt/NTFS/Problems 2016/zigzac")
