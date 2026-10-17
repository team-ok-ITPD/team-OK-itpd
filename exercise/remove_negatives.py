"""Functions for the list-mutation debugging exercise."""


def remove_negatives(numbers: list[int]) -> list[int]:
    """Return the input list without negative numbers."""
    for number in numbers:
        if number < 0:
            numbers.remove(number)
    return numbers
