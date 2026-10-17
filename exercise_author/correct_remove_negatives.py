"""Reference implementation used to validate the curated exercise."""


def remove_negatives(numbers: list[int]) -> list[int]:
    """Return the input list without negative numbers."""
    return [number for number in numbers if number >= 0]
