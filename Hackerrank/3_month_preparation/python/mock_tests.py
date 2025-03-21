# Mock test 1
def find_median(arr):
    #Simplest solution
    # Time complexity: O(n*log(n))
    # Space complexity (ignoring input): O(1)
    n = len(arr)
    arr.sort()
    if n % 2 == 0:
        return arr[n / 2] + arr[n / 2 - 1]
    else:
        return arr[n//2]

def find_median2(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(n)

find_median([4, 9, 10, 3, 2, 13, 10])
