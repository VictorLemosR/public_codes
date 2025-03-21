def max_min(k, arr):
    #Time complexity: O(n*log(n))
    #Space complexity (ignoring input): O(1)
    arr.sort()
    minimum_unfairness = arr[k - 1] - arr[0]
    for index in range(1, len(arr) - k + 1):
        if minimum_unfairness > arr[index + k - 1] - arr[index]:
            minimum_unfairness = arr[index + k - 1] - arr[index]

    return minimum_unfairness


def strong_password(n, password: str):
    #Time complexity: O(n)
    #Space complexity (ignoring input): O(1)
    add_lower = True
    add_upper = True
    add_number = True
    add_special = True
    for letter in password:
        if letter.islower():
            add_lower = False
        if letter.isupper():
            add_upper = False
        if letter.isnumeric():
            add_number = False
        if letter in "!@#$%^&*()-+":
            add_special = False

    characters_to_add = 0
    if add_lower:
        characters_to_add += 1
    if add_upper:
        characters_to_add += 1
    if add_number:
        characters_to_add += 1
    if add_special:
        characters_to_add += 1

    if len(password) + characters_to_add < 6:
        return 6 - len(password)

    return characters_to_add


def sansa_and_xor(arr):
    xor_value = 0
    for index in range(0, len(arr)):
        frequency_number = (index + 1) * (len(arr) - index)
        if frequency_number % 2 != 0:
            xor_value ^= arr[index]

    return xor_value
