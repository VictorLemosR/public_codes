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
