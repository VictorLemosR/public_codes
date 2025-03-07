def lonely_integer(a):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)
    numbers_dictionary = {}
    for number in a:
        if number in numbers_dictionary:
            numbers_dictionary[number] += 1
        else:
            numbers_dictionary[number] = 1

    for key, value in numbers_dictionary.items():
        if value == 1:
            return key


def lonely_integer_elegant(a):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    result = 0
    for number in a:
        result = result ^ number
    return result


def grading_students(grades):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1) if mutating in place or O(n) if not
    for index in range(0, len(grades)):
        grade = grades[index]
        if (grade > 37) and ((grade % 5) > 2):
            grades[index] = grade + 5 - grade % 5

    return grades


def flipping_bits(n):
    # Time complexity: O(1)
    # Space complexity (ignoring input): O(1)
    return (2**32 - 1) ^ n


def flipping_bits_without_xor(n):
    # Time complexity: O(1)
    # Space complexity (ignoring input): O(1)
    reverse_n = 0
    for exp in range(31, -1, -1):
        if 2**exp > n:
            reverse_n += 2**exp
        else:
            n -= 2**exp

    return reverse_n


def diagonal_difference(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    diagonal_1 = 0
    diagonal_2 = 0
    len_arr = len(arr)
    for index in range(0, len_arr):
        diagonal_1 += arr[index][index]
        diagonal_2 += arr[len_arr - index - 1][index]

    return abs(diagonal_1 - diagonal_2)


def counting_sort(arr):
    # Time complexity: O(n+k) or just O(n), since k is constant
    # Space complexity (ignoring input): O(k) or just O(1), since k is constant
    frequency_arr = [0] * 100
    for number in arr:
        frequency_arr[number] += 1

    return frequency_arr


def counting_valleys(steps, path):
    #Time complexity: O(n)
    #Space complexity (ignoring input): O(1)
    height = 0
    valleys = 0
    for letter in path:
        if letter == "D":
            height -= 1
            if height == -1:
                valleys += 1
        if letter == "U":
            height += 1

    return valleys
