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


def normal_nim(s):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    # Here, the last player to move wins (last player to remove last stones)
    initial_xor_sum = 0
    for pile in s:
        initial_xor_sum ^= pile

    # In case the initial state is xor_sum equal to 0, any move player 1 makes will
    # change the xor_sum to not 0. As long as player 2 moves to make the xor_sum
    # back to 0, player 1 can never wins
    if initial_xor_sum == 0:
        return "Player 2"
    else:
        return "Player 1"


# Function to a find a winnable move in a nim-game
def move_to_zero_xor(s):
    xor_sum = 0
    for number in s:
        xor_sum ^= number

    if xor_sum == 0:
        return "XOR of all numbers is already 0"
    # Proof that there is always a move that makes the xor_sum from not 0 to 0
    # Let S be the xor of all numbers but the one I'll change, which is x.
    # S^x = xor_sum
    # S^x' = 0 =>  x' = S => x'^x = xor_sum => x^xor_sum = x'
    # To prove that always exist x' < x, just look for the highest bit in xor_sum
    # look for a number that has that bit as well, x' won't have. This way,
    # I can guarantee there will be a number that works and that x' < x.

    copy_xor_sum = xor_sum
    highest_bit = 0
    while copy_xor_sum > 1:
        copy_xor_sum = copy_xor_sum >> 1
        highest_bit += 1

    base_10 = 1 << highest_bit
    for number in s:
        if (number & base_10) == base_10:
            print(f"Move from number {number} to number {xor_sum ^ number}")


def misere_nim(s):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    # Although less obvious than normal nim, the logic is similar. But there is an edge-case
    # As long your next move will not change all columns to be 1, forcing oponent
    # into xor_sum = 0 is a winning move. If all columns are 1, odd columns is a
    # winning move to your oponent and even columns is winning move to you
    xor_sum = 0
    columns_one = 0
    exist_non_one_column = False
    for number in s:
        if number == 1:
            columns_one += 1
        else:
            exist_non_one_column = True
        xor_sum ^= number

    if exist_non_one_column:
        if xor_sum == 0:
            return "Second"
        else:
            return "First"
    else:
        if columns_one % 2 == 0:
            return "First"
        else:
            return "Second"


def gaming_array(arr):
    # Time complexity: O(n)
    # Space complexity (ignoring input): O(1)
    max_number = arr[0]
    turns = 0
    for number in arr:
        if number > max_number:
            max_number = number
            turns += 1
    if turns % 2 == 0:
        return "BOB"
    else:
        return "ANDY"


def magic_squares(s):
    # Time complexity: O(1)
    # Space complexity (ignoring input): O(1)
    # Hard coded or not, both are O(1), since it's maximum of 9! to create all possible
    # squares, which is a costant (and that is the inefficient way)
    magic_squares_hard_coded = [
        [[2, 7, 6], [9, 5, 1], [4, 3, 8]],
        [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
        [[8, 3, 4], [1, 5, 9], [6, 7, 2]],
        [[6, 1, 8], [7, 5, 3], [2, 9, 4]],
        [[6, 7, 2], [1, 5, 9], [8, 3, 4]],
        [[2, 9, 4], [7, 5, 3], [6, 1, 8]],
        [[4, 3, 8], [9, 5, 1], [2, 7, 6]],
        [[8, 1, 6], [3, 5, 7], [4, 9, 2]],
    ]
    all_magic_squares = magic_squares_creating_efficiently()

    minimum_cost = 99
    for square in all_magic_squares:
        cost = 0
        for i in range(0, 3):
            for j in range(0, 3):
                cost += abs(s[i][j] - square[i][j])

        minimum_cost = min(minimum_cost, cost)

    return minimum_cost


def magic_squares_creating_inefficiently():
    # create magic squares

    blank_square = []
    for row in range(0, 3):
        row = []
        for column in range(0, 3):
            row.append(None)
        blank_square.append(row)

    possible_squares = []
    for row in range(0, 3):
        for column in range(0, 3):
            blank_square[row][column] = 1
            possible_squares.append([[cell for cell in row] for row in blank_square])
            blank_square[row][column] = None

    old_squares = []
    for number in range(2, 10):
        old_squares = possible_squares
        possible_squares = []
        for possible_square in old_squares:
            for row in range(0, 3):
                for column in range(0, 3):
                    if possible_square[row][column] is None:
                        possible_square[row][column] = number
                        possible_squares.append(
                            [[cell for cell in row] for row in possible_square]
                        )
                        possible_square[row][column] = None

    magic_squares = []
    for square in possible_squares:
        square_is_magic = True
        # check sum columns
        for column in range(0, 3):
            if square[0][column] + square[1][column] + square[2][column] != 15:
                square_is_magic = False
        # check sum rows
        for row in range(0, 3):
            if square[row][0] + square[row][1] + square[row][2] != 15:
                square_is_magic = False

        # check sum diagonals
        if square[0][0] + square[1][1] + square[2][2] != 15:
            square_is_magic = False
        if square[0][2] + square[1][1] + square[2][0] != 15:
            square_is_magic = False

        if square_is_magic:
            magic_squares.append(square)

    return magic_squares


def magic_squares_creating_efficiently():
    # create magic squares
    blank_square = []
    for row in range(0, 3):
        row = []
        for column in range(0, 3):
            row.append(None)
        blank_square.append(row)

    possible_squares = []
    for row in range(0, 3):
        for column in range(0, 3):
            blank_square[row][column] = 9
            possible_squares.append([[cell for cell in row] for row in blank_square])
            blank_square[row][column] = None

    old_squares = []
    # start by big numbers to filter magic numbers faster
    for number in range(8, 0, -1):
        old_squares = possible_squares
        possible_squares = []
        for possible_square in old_squares:
            for row in range(0, 3):
                for column in range(0, 3):
                    if possible_square[row][column] is None:
                        # check row validity
                        sum_row = number
                        for j in range(0, 3):
                            if possible_square[row][j] is not None:
                                sum_row += possible_square[row][j]

                        if sum_row < 16:
                            # check column validity
                            sum_column = number
                            for i in range(0, 3):
                                if possible_square[i][column] is not None:
                                    sum_column += possible_square[i][column]

                            if sum_column < 16:
                                possible_square[row][column] = number
                                possible_squares.append(
                                    [[cell for cell in row] for row in possible_square]
                                )
                                possible_square[row][column] = None

    magic_squares = []
    for square in possible_squares:
        square_is_magic = True
        # check sum columns
        for column in range(0, 3):
            if square[0][column] + square[1][column] + square[2][column] != 15:
                square_is_magic = False
        # check sum rows
        for row in range(0, 3):
            if square[row][0] + square[row][1] + square[row][2] != 15:
                square_is_magic = False

        # check sum diagonals
        if square[0][0] + square[1][1] + square[2][2] != 15:
            square_is_magic = False
        if square[0][2] + square[1][1] + square[2][0] != 15:
            square_is_magic = False

        if square_is_magic:
            magic_squares.append(square)

    return magic_squares


def superDigit(n, k):
    # Time complexity: O(log(n))
    # Space complexity (ignoring input): O(1)
    if (len(n) == 1) and (k == 1):
        return int(n)

    sum = 0
    for number in n:
        sum += int(number)
    return superDigit(str(sum * k), 1)


def counter_game(n):
    # Time complexity: O(log(n))
    # Space complexity (ignoring input): O(1)
    if n == 1:
        return "Louise"

    count = 0
    while n > 1:
        is_power_of_2 = (n & (n - 1)) == 0
        if is_power_of_2:
            while n > 1:
                n = n / 2
                count += 1
        else:
            power_of_2 = 2
            while power_of_2 * 2 < n:
                power_of_2 = power_of_2 * 2
            n = n - power_of_2
            count += 1
    if count % 2 == 0:
        return "Richard"

    return "Louise"


def sum_xor(n):
    # Time complexity: O(log(n))
    # Space complexity (ignoring input): O(1)
    if n == 0:
        return 1
    # count 0 in binary of number
    count = 0
    while n > 0:
        if n & 1 == 0:
            count += 1
        n = n >> 1

    return 2**count
