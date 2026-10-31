from django.db import migrations

# The exercises shown on the New challenge and Practice pages.
EXERCISES = [   {   'slug': 'remove-negatives',
        'title': 'The surviving negative',
        'category': 'arrays',
        'topic': 'Arrays & loops',
        'difficulty': 'Easy',
        'language': 'Python 3',
        'duration': '10–15 min',
        'summary': 'A filter should drop every negative number, but some survive.',
        'description': 'remove_negatives() should return the list without any negative '
                       'numbers. It runs without raising an exception, yet some '
                       'negative values are still in the result. Reproduce the failure '
                       'and find out why.',
        'file_name': 'remove_negatives.py',
        'function_name': 'remove_negatives',
        'buggy_code': '"""Functions for the list-mutation debugging exercise."""\n'
                      '\n'
                      '\n'
                      'def remove_negatives(numbers: list[int]) -> list[int]:\n'
                      '    """Return the input list without negative numbers."""\n'
                      '    for number in numbers:\n'
                      '        if number < 0:\n'
                      '            numbers.remove(number)\n'
                      '    return numbers',
        'tests': [   {'name': 'Empty list', 'input': [], 'expected': []},
                     {   'name': 'Mixed numbers',
                         'input': [4, -3, -2, 5],
                         'expected': [4, 5]},
                     {   'name': 'Consecutive negatives',
                         'input': [-3, -2, -1],
                         'expected': []}],
        'symptom': 'Wrong result · no exception raised',
        'explanation': 'The function finishes normally, but negative numbers that sit '
                       'next to another negative are still in the returned list. '
                       'Nothing crashes, so the bug is in the logic, not the syntax.',
        'has_workspace': True},
    {   'slug': 'total-starts-late',
        'title': 'A total that starts too late',
        'category': 'arrays',
        'topic': 'Arrays & loops',
        'difficulty': 'Easy',
        'language': 'Python 3',
        'duration': '5–10 min',
        'summary': 'Adding up every score gives a total that is always too small.',
        'description': 'sum_scores() should add up every score in the list. For most '
                       'inputs the total comes out smaller than expected, and a '
                       'one-item list sums to zero.',
        'file_name': 'sum_scores.py',
        'function_name': 'sum_scores',
        'buggy_code': 'def sum_scores(scores):\n'
                      '    """Return the total of every score in the list."""\n'
                      '    total = 0\n'
                      '    for i in range(1, len(scores)):\n'
                      '        total += scores[i]\n'
                      '    return total',
        'tests': [   {'name': 'Empty list', 'input': [], 'expected': 0},
                     {'name': 'Single score', 'input': [7], 'expected': 7},
                     {'name': 'Several scores', 'input': [3, 4, 5], 'expected': 12}],
        'symptom': 'Wrong result · no exception raised',
        'explanation': 'The total is consistently too small, and the difference is '
                       'always one of the input values. The loop runs, but something '
                       'about which items it visits is off.',
        'has_workspace': False},
    {   'slug': 'duplicated-result',
        'title': 'The duplicated result',
        'category': 'arrays',
        'topic': 'Arrays & loops',
        'difficulty': 'Easy',
        'language': 'Python 3',
        'duration': '10–15 min',
        'summary': 'A de-duplication helper hands back every repeat it was given.',
        'description': 'unique_items() should keep the first copy of each value and '
                       'drop the repeats, preserving order. Lists that are already '
                       'unique look fine, but repeated values come straight back out.',
        'file_name': 'unique_items.py',
        'function_name': 'unique_items',
        'buggy_code': 'def unique_items(items):\n'
                      '    """Return items without repeats, keeping first-seen '
                      'order."""\n'
                      '    seen = []\n'
                      '    result = []\n'
                      '    for item in items:\n'
                      '        if item not in seen:\n'
                      '            result.append(item)\n'
                      '    return result',
        'tests': [   {'name': 'Empty list', 'input': [], 'expected': []},
                     {   'name': 'Already unique',
                         'input': [1, 2, 3],
                         'expected': [1, 2, 3]},
                     {   'name': 'Repeated values',
                         'input': [2, 2, 3, 2],
                         'expected': [2, 3]}],
        'symptom': 'Wrong result · no exception raised',
        'explanation': 'Every repeat survives, so the duplicate check never seems to '
                       'trigger. Watch what the function remembers between iterations.',
        'has_workspace': False},
    {   'slug': 'missing-last-element',
        'title': 'The missing last element',
        'category': 'arrays',
        'topic': 'Arrays & loops',
        'difficulty': 'Easy',
        'language': 'Python 3',
        'duration': '5–10 min',
        'summary': 'Summing the positive numbers quietly ignores part of the list.',
        'description': 'sum_positive() should add every positive number in the list. '
                       'Some inputs work, but a list with a single positive value sums '
                       'to zero.',
        'file_name': 'sum_positive.py',
        'function_name': 'sum_positive',
        'buggy_code': 'def sum_positive(numbers):\n'
                      '    total = 0\n'
                      '    for i in range(len(numbers) - 1):\n'
                      '        if numbers[i] > 0:\n'
                      '            total += numbers[i]\n'
                      '    return total',
        'tests': [   {'name': 'Empty list', 'input': [], 'expected': 0},
                     {'name': 'Single positive', 'input': [5], 'expected': 5},
                     {'name': 'Mixed numbers', 'input': [4, -3, 2], 'expected': 6}],
        'symptom': 'Wrong result · no exception raised',
        'explanation': 'The function returns a number for every input, but the total '
                       'is too low whenever a positive value sits in a particular '
                       'position. Compare which items the loop actually reads with the '
                       'ones it should.',
        'has_workspace': False},
    {   'slug': 'count-words',
        'title': 'Duplicate dictionary keys',
        'category': 'dicts',
        'topic': 'Dictionaries',
        'difficulty': 'Medium',
        'language': 'Python 3',
        'duration': '10–15 min',
        'summary': 'Word counts split one word across several dictionary keys.',
        'description': 'count_words() should count words case-insensitively, ignoring '
                       'surrounding spaces. The same word sometimes shows up under '
                       'more than one key.',
        'file_name': 'count_words.py',
        'function_name': 'count_words',
        'buggy_code': 'def count_words(words):\n'
                      '    """Count words case-insensitively, ignoring surrounding '
                      'spaces."""\n'
                      '    counts = {}\n'
                      '    for word in words:\n'
                      '        key = word.strip()\n'
                      '        counts[key] = counts.get(key, 0) + 1\n'
                      '    return counts',
        'tests': [   {   'name': 'Single word',
                         'input': ['apple'],
                         'expected': {'apple': 1}},
                     {   'name': 'Mixed case',
                         'input': ['Apple', 'apple'],
                         'expected': {'apple': 2}},
                     {   'name': 'Padded word',
                         'input': ['pear ', 'pear'],
                         'expected': {'pear': 2}}],
        'symptom': 'Wrong result · no exception raised',
        'explanation': 'Counts come back split across keys that look like the same '
                       'word to a reader. Compare the keys the function builds with '
                       'the rule in its docstring.',
        'has_workspace': False}]


def seed_page_exercises(apps, schema_editor):
    Bug = apps.get_model("bugs", "Bug")
    for exercise in EXERCISES:
        fields = dict(exercise)
        Bug.objects.update_or_create(slug=fields.pop("slug"), defaults=fields)


def unseed_page_exercises(apps, schema_editor):
    slugs = [exercise["slug"] for exercise in EXERCISES if exercise["slug"] != "remove-negatives"]
    apps.get_model("bugs", "Bug").objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("bugs", "0003_exercise_details"),
    ]

    operations = [
        migrations.RunPython(seed_page_exercises, unseed_page_exercises),
    ]
