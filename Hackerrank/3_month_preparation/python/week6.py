def sherlock_and_array(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    total_sum = 0
    for value in arr:
        total_sum += value

    left_sum = 0
    for value in arr:
        right_sum = total_sum - left_sum - value
        if left_sum == right_sum:
            return "YES"
        left_sum += value

    return "NO"
