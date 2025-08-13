def selection_sort(arr):
    # Time complexity: O(n^2)
    # Space complexity (ignoring input): O(1)
    # Preserve order: No
    for i in range(0, len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    print(arr)


def bubble_sort(arr):
    # Time complexity: O(n^2)
    # Space complexity (ignoring input): O(1)
    # Preserve order: Yes, stable
    for i in range(0, len(arr)):
        not_swapped = True
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                not_swapped = False

        if not_swapped:
            break

    print(arr)


def bubble_sort_recursive(arr, i):
    not_swapped = True
    for j in range(0, len(arr) - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            not_swapped = False

    if not_swapped:
        return arr

    return bubble_sort_recursive(arr, i - 1)


def merge_sort(arr):
    pass


def quick_sort(arr):
    pass
