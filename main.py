from pprint import pprint
from thefuzz import fuzz
from thefuzz.process import extractBests
from operator import itemgetter
import difflib
import timeit


def matches_with_scores(word, possibilities):
    """Snippet from difflib. I want to see scores, so I don't use get_close_matches"""
    result = []
    s = difflib.SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        result.append((x, round(100 * s.ratio())))
    result = sorted(result, key=itemgetter(1), reverse=True)
    return result


def match_and_print(items):
    """Get scores with thefuzz and difflib and compare"""
    for item in items:
        print("-" * 40)
        print(f"item: {item}")
        matches1 = extractBests(item, items, scorer=fuzz.UWRatio)
        print("thefuzz:")
        pprint(matches1)
        matches2 = matches_with_scores(item, items)
        print("difflib:")
        pprint(matches2)


def match_and_time(items, n=10000):
    """Get scores with thefuzz and difflib and compare timing"""
    res1 = timeit.timeit(
        lambda: extractBests(items[0], items, scorer=fuzz.UWRatio), number=n
    )
    res2 = timeit.timeit(lambda: matches_with_scores(items[0], items), number=n)
    print(f"n={n}, thefuzz: {res1}, difflib: {res2}")


def main():
    datasets = [
        ["Pyotr", "Petr", "Peter", "Piotr"],
        ["Иван", "Иванко", "Ваня", "Ванюша"],
        ["Vladimirovich", "Wladymiryowich", "Wladimyrowitch", "Vladislavovich"],
        [
            "Chelyabinsk, ul. Lenina, d.15, kv.33",
            "Chelyabinsk, ul Lenina, 15-33",
            "Tchelabinsk Lenina 15-33",
            "Tchelabinsk ulitsa Lenina d 15 kv 33",
        ],
        [
            "Харьков, Волонтерская 72, кв. 42",
            "Харьков, ул. Волонтерская д.72, кв.42",
            "Харьков, ул. Валонтерская 72-42",
            "Волонтерская 72/42, Харьков",
        ],
    ]
    # print matches and scores
    for dataset in datasets:
        match_and_print(dataset)

    # print how long it takes
    for i, dataset in enumerate(datasets):
        match_and_time(dataset)


if __name__ == "__main__":
    main()
