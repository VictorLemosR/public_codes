def permuting_two_arrays(k, A, B):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)
    A = sorted(A)
    B = sorted(B, reverse=True)

    for index in range(0, len(A)):
        if (A[index] + B[index]) < k:
            return "NO"

    return "YES"


def subarray_division_2(s, d, m):
    # Time complexity: O(n), you could speed up creating a sum variable, but still O(n)
    # Space complexity (ignoring input): O(1)
    ways_to_divide = 0
    for index in range(0, len(s) - m + 1):
        subarray = s[index : index + m]
        if sum(subarray) == d:
            ways_to_divide += 1

    return ways_to_divide


def strings_xor(s, t):
    res = ""
    for i in range(len(s)):
        if s[i] == t[i]:
            res += "0"
        else:
            res += "1"

    return res


def sales_by_match(n, ar):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)
    socks_dict = {}
    for sock in ar:
        if sock in socks_dict:
            socks_dict[sock] += 1
        else:
            socks_dict[sock] = 1

    total_pairs = 0
    for values in socks_dict.values():
        total_pairs += values // 2

    return total_pairs


def migratory_birds(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1). You could use a frequency array instead
    # of a dictionary and use even less space
    birds_dict = {}
    for bird in arr:
        if bird in birds_dict:
            birds_dict[bird] += 1
        else:
            birds_dict[bird] = 1

    most_frequent = [6, 0]
    for bird, frequency in birds_dict.items():
        if frequency > most_frequent[1]:
            most_frequent = [bird, frequency]
        if (frequency == most_frequent[1]) and (bird < most_frequent[0]):
            most_frequent[0] = bird

    return most_frequent[0]


def maximum_perimeter_triangle(sticks: list):
    #Time complexity: O(n*log(n))
    #Space complexity (ignoring input): O(1)
    sticks.sort(reverse=True)
    for index in range(0, len(sticks) - 2):
        if sticks[index] < sticks[index + 1] + sticks[index + 2]:
            triangle = [sticks[index], sticks[index + 1], sticks[index + 2]]
            triangle.sort()
            return triangle

    return [-1]
