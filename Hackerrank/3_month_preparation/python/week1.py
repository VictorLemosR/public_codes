def plus_minus(arr):
    len_arr = len(arr)
    positive_numbers = 0
    negative_numbers = 0
    for number in arr:
        if number >0:
            positive_numbers += 1
        elif number < 0:
            negative_numbers += 1

    print(round(positive_numbers/len_arr, 6))
    print(round(negative_numbers/len_arr, 6))
    print(round((len_arr -positive_numbers-negative_numbers)/len_arr, 6))

plus_minus([-4, 3, -9, 0, 4, 1])
