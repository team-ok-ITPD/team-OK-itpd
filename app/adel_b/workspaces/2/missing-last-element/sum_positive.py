def sum_positive(numbers):
    total = 0
    for i in range(len(numbers) ):
        if numbers[i] > 0:
            total += numbers[i]
    return total
