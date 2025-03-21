def picking_numbers(a):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)
    a_dict = {}
    for value in a:
        if value in a_dict:
            a_dict[value] += 1
        else:
            a_dict[value] = 1

    longest_subsequence_len = 0
    current_subsequence_len = 0
    plus_len = 0
    for value, frequency in a_dict.items():
        # You don't need to check for value-1 cases, because that is already checked by the value
        # itself + 1
        if (value + 1) in a_dict:
            plus_len = a_dict[value + 1]

        current_subsequence_len = frequency + plus_len
        if current_subsequence_len > longest_subsequence_len:
            longest_subsequence_len = current_subsequence_len

        plus_len = 0

    return longest_subsequence_len


def left_rotation(d, arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)
    new_array = [0] * len(arr)
    for index in range(0, len(arr)):
        new_array[(index - d) % len(arr)] = arr[index]

    return new_array


def left_rotation_in_place(d, arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    n = len(arr)
    start_range = 0
    end_range = d
    for index in range(0, (end_range - start_range) // 2):
        arr[index + start_range], arr[end_range - index - 1] = (
            arr[end_range - index - 1],
            arr[index + start_range],
        )

    start_range = d
    end_range = n
    for index in range(0, (end_range - start_range) // 2):
        arr[index + start_range], arr[end_range - index - 1] = (
            arr[end_range - index - 1],
            arr[index + start_range],
        )

    start_range = 0
    end_range = n
    for index in range(0, (end_range - start_range) // 2):
        arr[index + start_range], arr[end_range - index - 1] = (
            arr[end_range - index - 1],
            arr[index + start_range],
        )

    return arr


def number_line_jumps(x1, v1, x2, v2):
    # Time complexity: O(1)
    # Space complexity (ignoring input): O(1)
    if x1 == x2:
        return "YES"
    if v1 == v2:
        return "NO"

    relative_speed = v2 - v1
    initial_distance = x1 - x2
    jumps = initial_distance / relative_speed

    if jumps == abs(int(jumps)):
        return "YES"

    return "NO"


def separate_numbers(s: str):
    # Time complexity: O(n^2)
    # Space complexity (ignoring input): O(n)
    if len(s) == 1:
        print("NO")
        return

    for len_search in range(1, (len(s)) // 2 + 1):
        first_number = int(s[:len_search])

        index = len_search
        next_number = first_number
        next_number_string = str(next_number)
        next_len = len(next_number_string)
        return_value = "YES"
        while index + next_len <= len(s):
            next_number = next_number + 1
            next_number_string = str(next_number)
            next_len = len(next_number_string)

            if next_number_string != s[index : index + next_len]:
                return_value = "NO"
                break
            index += next_len

        if (index == len(s)) and (return_value == "YES"):
            print(f"YES {first_number}")
            return

    print("NO")


def closest_numbers(arr):
    # Time complexity: O(n*log(n))
    # Space complexity (ignoring input): O(n)
    arr.sort()
    minimum_diff = arr[1] - arr[0]
    pairs = [arr[0], arr[1]]
    for index in range(2, len(arr)):
        if (arr[index] - arr[index - 1]) == minimum_diff:
            pairs.append(arr[index - 1])
            pairs.append(arr[index])
        if (arr[index] - arr[index - 1]) < minimum_diff:
            minimum_diff = arr[index] - arr[index - 1]
            pairs = [arr[index - 1], arr[index]]

    return pairs


def tower_breakers(n, m):
    # Time complexity: O(1)
    # Space complexity (ignoring input): O(1)
    # If number of towers is pair, whatever player 1 does, player 2 mimics and wins.
    # If n is odd, player 1 push a tower to 1 and the game becomes a n is pair case
    if m == 1:
        return 2

    if n % 2 == 0:
        return 2
    else:
        return 1


def minimum_absolute_difference(arr):
    # Time complexity: O(n*log(n))
    # Space complexity (ignoring input): O(1)
    arr.sort()
    minimum_difference = abs(arr[0] - arr[1])
    for index in range(2, len(arr)):
        difference = abs(arr[index] - arr[index - 1])
        if minimum_difference > difference:
            minimum_difference = difference

    return minimum_difference


def caesar_cipher(s, k):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)
    new_string = ""
    for letter in s:
        if (letter.lower() <= "z") and (letter.lower() >= "a"):
            if letter == letter.lower():
                sum_a = ord("a")
            else:
                sum_a = ord("A")
            new_string += chr(
                ((ord(letter) - sum_a + k) % (ord("z") - ord("a") + 1)) + sum_a
            )
        else:
            new_string += letter

    return new_string
