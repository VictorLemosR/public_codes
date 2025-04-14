def max_min(k, arr):
    # Time complexity: O(n*log(n))
    # Space complexity (ignoring input): O(1)
    arr.sort()
    minimum_unfairness = arr[k - 1] - arr[0]
    for index in range(1, len(arr) - k + 1):
        if minimum_unfairness > arr[index + k - 1] - arr[index]:
            minimum_unfairness = arr[index + k - 1] - arr[index]

    return minimum_unfairness


def strong_password(n, password: str):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
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


def dynamic_array(n, queries):
    # Time complexity: O(n+q)
    # Space complexity (ignoring input): O(n+q)
    array = []
    for _ in range(0, n):
        array.append([])
    last_answer = 0
    result = []
    for query in queries:
        if query[0] == 1:
            array[(query[1] ^ last_answer) % n].append(query[2])

        if query[0] == 2:
            idx = (query[1] ^ last_answer) % n
            last_answer = array[idx][query[2] % len(array[idx])]
            result.append(last_answer)

    return result


def is_smart_number(num):
    val = int(math.sqrt(num))
    # Just change the line below
    if num / val == val:
        return True
    return False


def missing_numbers(arr, brr):
    # Time complexity: O(a + b)
    # Space complexity (ignoring input): O(a + b)
    arr_dict = {}
    for value in arr:
        if value in arr_dict:
            arr_dict[value] += 1
        else:
            arr_dict[value] = 1

    brr_dict = {}
    for value in brr:
        if value in brr_dict:
            brr_dict[value] += 1
        else:
            brr_dict[value] = 1

    missing_values = []
    for key in brr_dict.keys():
        if key in arr_dict:
            if arr_dict[key] <= brr_dict[key]:
                missing_values.append(key)
        else:
            missing_values.append(key)

    missing_values.sort()
    return missing_values


def full_counting_sort(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    sorted_array = [""] * 101
    for index in range(0, len(arr)):
        sorted_index = int(arr[index][0])
        if index < len(arr) / 2:
            sorted_array[sorted_index] += " -"
        else:
            sorted_array[sorted_index] += " "
            for letter in arr[index][1]:
                sorted_array[sorted_index] += letter

    result_string = ""
    for string in sorted_array:
        result_string += string

    print(result_string[1:])


def grid_challenge(grid):
    #Time complexity: O(n^2*log(n))
    #Space complexity (ignoring input): O(n)
    sorted_grid = []
    for string in grid:
        sorted_grid.append(sorted(string))

    for row in range(0, len(grid) - 1):
        for column in range(0, len(grid[0])):
            if sorted_grid[row][column] > sorted_grid[row + 1][column]:
                return "NO"

    return "YES"


def sansa_and_xor(arr):
    #Time complexity: O(n)
    #Space complexity (ignoring input): O(1)
    #A number will appear in {(index+1)*(n-index)} subsequences
    #In case arr.len() is par, the appearences of any number will be par as well
    xor_value = 0
    for index in range(0, len(arr)):
        frequency_number = (index + 1) * (len(arr) - index)
        if frequency_number % 2 != 0:
            xor_value ^= arr[index]

    return xor_value
