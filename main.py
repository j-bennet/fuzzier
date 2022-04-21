from pprint import pprint
from thefuzz import fuzz
from thefuzz.process import extractBests
from operator import itemgetter
import difflib
import timeit
import fonetika.soundex as soundex
import fonetika.metaphone as metaphone

SOUNDEX_IMPL = {
    "ru": soundex.RussianSoundex(),
    "en": soundex.EnglishSoundex(),
}


METAPHONE_IMPL = {
    "ru": metaphone.RussianMetaphone(),
    "en": metaphone.Metaphone(),
}


def _fonetica_find_matches(word, possibilities, phonetic_impl):
    word_code = phonetic_impl.transform(word)
    result = []
    for poss in possibilities:
        poss_code = phonetic_impl.transform(poss)
        res = fuzz.UWRatio(word_code, poss_code)
        result.append((poss, res))
    result = sorted(result, key=itemgetter(1), reverse=True)
    return result


def metaphone_find_matches(word, possibilities, lang):
    """Find matches using soundex"""
    phonetic_impl = METAPHONE_IMPL[lang]
    return _fonetica_find_matches(word, possibilities, phonetic_impl)


def soundex_find_matches(word, possibilities, lang):
    """Find matches using soundex"""
    phonetic_impl = SOUNDEX_IMPL[lang]
    return _fonetica_find_matches(word, possibilities, phonetic_impl)


def difflib_find_matches(word, possibilities, lang):
    """Snippet from difflib. I want to see scores, so I don't use get_close_matches"""
    result = []
    s = difflib.SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        result.append((x, round(100 * s.ratio())))
    result = sorted(result, key=itemgetter(1), reverse=True)
    return result


def thefuzz_find_matches(word, possibilities, lang):
    """Get scores with thefuzz and difflib and compare"""
    return extractBests(word, possibilities, scorer=fuzz.UWRatio)


SCORING_METHODS = {
    "thefuzz": thefuzz_find_matches,
    "difflib": difflib_find_matches,
    "soundex": soundex_find_matches,
    "metaphone": metaphone_find_matches,
}


def match_and_print(items, lang):
    """Get scores with thefuzz and difflib and compare"""
    word = items[0]
    possibilities = items[1:]
    print("-" * 40)
    print(f"word: {word}")
    for method_name, method_handler in SCORING_METHODS.items():
        result = method_handler(word, possibilities, lang)
        print(f"{method_name}: {result}")


def match_and_time(items, language, n=10000):
    """Get scores with thefuzz and difflib and compare timing"""
    for method_name, method_handler in SCORING_METHODS.items():
        elapsed = timeit.timeit(
            lambda: method_handler(items[0], items[1:], language), number=n
        )
        print(f"n={n}, {method_name}: {elapsed}")


def main():
    datasets = [
        (["Pyotr", "Petr", "Peter", "Piotr"], "en"),
        (["Иван", "Иванко", "Ваня", "Ванюша"], "ru"),
        (["Vladimirovich", "Wladymiryowich", "Wladimyrowitch", "Vladislavovich"], "en"),
        ([
            "Chelyabinsk, ul. Lenina, d.15, kv.33",
            "Chelyabinsk, ul Lenina, 15-33",
            "Tchelabinsk Lenina 15-33",
            "Tchelabinsk ulitsa Lenina d 15 kv 33",
        ], "en"),
        ([
            "Харьков, Волонтерская 72, кв. 42",
            "Харьков, ул. Волонтерская д.72, кв.42",
            "Харьков, ул. Валонтерская 72-42",
            "Волонтерская 72/42, Харьков",
        ], "ru"),
    ]
    # print matches and scores
    for dataset, language in datasets:
        match_and_print(dataset, language)

    # print how long it takes
    # for i, dataset in enumerate(datasets):
    #     match_and_time(dataset, language)


if __name__ == "__main__":
    main()
