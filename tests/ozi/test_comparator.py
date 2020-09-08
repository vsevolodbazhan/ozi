from ozi.comparator import (
    normalize,
    distance_is_acceptable as is_acceptable,
    levenshtein_distance as distance,
)


def test_normalizes_correctly():
    text_1 = "Hello, World! 12 3"
    text_2 = "Hello, World! 123"
    text_3 = "he ll o, world ! 1 2 3"
    empty = ""

    result = "hello,world!123"

    assert normalize(text_1) == result
    assert normalize(text_2) == result
    assert normalize(text_3) == result
    assert normalize(empty) == empty


def test_distance_is_begin_evaluated_correctly():
    distance_1 = 0
    distance_2 = 1
    distance_3 = 2
    distance_4 = 3

    assert is_acceptable(distance_1)
    assert is_acceptable(distance_2)
    assert is_acceptable(distance_3)
    assert is_acceptable(distance_4) is False


def test_texts_are_begin_compared_correctly():
    reference = "Lorem ipsum dolor"

    good = [
        reference,
        reference.lower(),
        "Larem ipsum dalor",
        "Loremipsumdolor",
        "lorem ipsum dolor",
    ]
    bad = ["lrem psum dolr", "ipsum lorem dolor", "dolor lorem ipsum", "dolor sit amet"]

    assert is_acceptable(distance(good[0], reference))
    assert is_acceptable(distance(good[1], reference))
    assert is_acceptable(distance(good[2], reference))
    assert is_acceptable(distance(good[3], reference))
    assert is_acceptable(distance(good[4], reference))

    assert is_acceptable(distance(bad[0], reference)) is False
    assert is_acceptable(distance(bad[1], reference)) is False
    assert is_acceptable(distance(bad[2], reference)) is False
    assert is_acceptable(distance(bad[3], reference)) is False
