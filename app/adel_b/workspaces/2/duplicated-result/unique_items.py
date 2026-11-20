def unique_items(items):
    """Return items without repeats, keeping first-seen order."""
    seen = []
    result = []
    for item in items:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result
