from remove_negatives import remove_negatives


def test_empty_list() -> None:
    assert remove_negatives([]) == []


def test_mixed_numbers() -> None:
    assert remove_negatives([4, -3, -2, 5]) == [4, 5]


def test_consecutive_negatives() -> None:
    assert remove_negatives([-3, -2, -1]) == []
