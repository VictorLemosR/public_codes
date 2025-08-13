def create_all_subarrays(arr):
    # Time complexity: O(n^3)
    # Space complexity (ignoring input): O(n^3)
    subarrays = []
    for sub_len in range(1, len(arr) + 1):
        for index in range(0, len(arr) - sub_len + 1):
            subarrays.append(arr[index : index + sub_len])

    print(
        f"->> subarrays <<- function: create_all_subarrays; file: extras.py\n{subarrays}"
    )


def create_all_subsequences(arr):
    # Time complexity: O()
    # Space complexity (ignoring input): O()
    subsequences = []
    for i in range(0, len(arr)):
        # list comprehension was the way I found out to create a deepcopy in python
        # Technically, I just wanted 'aux_subsequences = subsequences.deepcopy()'
        aux_subsequences = [subsequence[:] for subsequence in subsequences]
        for subsequence in aux_subsequences:
            subsequence.append(arr[i])
        subsequences.append([arr[i]])
        if aux_subsequences:
            subsequences.extend(aux_subsequences)

    print(
        f"->> subsequences <<- function: create_all_subsequences; file: extras.py\n{subsequences}"
    )


def create_all_subsequences2(arr):
    n = len(arr)
    subsequences = []
    # There are 2^n possible subsequences (each element can be either included or excluded)
    for mask in range(1 << n):  # 1 << n equals 2^n
        subseq = []
        for i in range(n):
            # Check if the i-th bit of mask is set. If so, include arr[i]
            if mask & (1 << i):
                subseq.append(arr[i])
        subsequences.append(subseq)

    print(subsequences)


if __name__ == "__main__":
    arr = [1, 3, 5, 3, 2, 4, 1]
    # create_all_subarrays(arr)
    # create_all_subsequences(arr)
    # create_all_subsequences2(arr)
    # bubble_sort(arr)
    # bubble_sort_recursive(arr, len(arr))
