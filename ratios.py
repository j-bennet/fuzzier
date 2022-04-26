import functools
import rapidfuzz.fuzz as fuzz
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


@functools.lru_cache(10000)
def fuzzy_ratio(s1, s2):
    return fuzz.token_sort_ratio(s1, s2)


@functools.lru_cache(10000)
def metaphone_ratio(s1, s2, language="en"):
    wc1 = METAPHONE_IMPL[language].transform(s1)
    wc2 = METAPHONE_IMPL[language].transform(s2)
    return fuzz.token_sort_ratio(wc1, wc2)


@functools.lru_cache(10000)
def soundex_ratio(s1, s2, language="en"):
    wc1 = SOUNDEX_IMPL[language].transform(s1)
    wc2 = SOUNDEX_IMPL[language].transform(s2)
    return fuzz.token_sort_ratio(wc1, wc2)
