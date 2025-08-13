fn sherlock_and_array(arr: &[i32]) -> String {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let total_sum: i32 = arr.iter().sum();

    let mut left_sum = 0;
    for value in arr {
        let right_sum = total_sum - left_sum - value;
        if left_sum == right_sum {
            return "YES".to_string();
        }
        left_sum += value;
    }

    "NO".to_string()
}

fn misere_nim(s: &[i32]) -> String {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut xor_sum = 0;
    let mut exist_column_over_1 = false;
    for &number in s {
        xor_sum ^= number;
        if number > 1 {
            exist_column_over_1 = true;
        }
    }

    if exist_column_over_1 {
        if xor_sum == 0 {
            return String::from("Second");
        } else {
            return String::from("First");
        }
    } else {
        if s.len() % 2 == 0 {
            return String::from("First");
        } else {
            return String::from("Second");
        }
    }
}

fn gaming_array(arr: &[i32]) -> String {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut max_number = arr[0];
    let mut turns = 0;
    for &number in arr {
        if number > max_number {
            max_number = number;
            turns += 1
        }
    }
    if turns % 2 == 0 {
        String::from("BOB")
    } else {
        String::from("ANDY")
    }
}

fn magic_squares(s: &[Vec<i32>]) -> i32 {
    // Time complexity: O(1)
    // Space complexity (ignoring input): O(1)
    // Hard coded or not, both are O(1), since it's maximum of 9! to create all possible
    // squares, which is a costant (and that is the inefficient way)
    let all_magic_squares = build_magic_squares();

    let mut minimum_cost = 99;
    for square in all_magic_squares {
        let mut cost = 0;

        for row in 0..3 {
            for column in 0..3 {
                cost += (square[row][column] - s[row][column]).abs();
            }
        }
        minimum_cost = std::cmp::min(minimum_cost, cost);
    }
    minimum_cost
}

pub fn build_magic_squares() -> Vec<Vec<[i32; 3]>> {
    let mut possible_squares = Vec::new();
    let null_square = Vec::from([[0, 0, 0], [0, 0, 0], [0, 0, 0]]);
    for row in 0..3 {
        for column in 0..3 {
            let mut square = null_square.clone();
            square[row][column] = 9;
            possible_squares.push(square);
        }
    }
    let mut old_squares = Vec::new();
    for number in (1..=8).rev() {
        old_squares = possible_squares;
        possible_squares = Vec::new();
        for mut square in old_squares {
            for row in 0..3 {
                for column in 0..3 {
                    if square[row][column] == 0 {
                        // Check row validity
                        if square[row][0] + square[row][1] + square[row][2] + number < 16 {
                            // Check column validity
                            if square[0][column] + square[1][column] + square[2][column] + number
                                < 16
                            {
                                let mut possible_square = square.clone();
                                possible_square[row][column] = number;
                                possible_squares.push(possible_square);
                            }
                        }
                    }
                }
            }
        }
    }

    let mut all_magic_squares = Vec::new();
    //Check diagonals
    for square in possible_squares {
        if square[0][0] + square[1][1] + square[2][2] == 15
            && square[2][0] + square[1][1] + square[0][2] == 15
        {
            all_magic_squares.push(square);
        }
    }
    all_magic_squares
}

fn superDigit(n: &str, k: i32) -> i32 {
    //Time complexity: O(log(n))
    //Space complexity (ignoring input): O(1)
    if (n.len() == 1) && (k == 1) {
        return n.parse::<i32>().unwrap();
    }

    let mut sum = 0;
    for number in n.chars() {
        let number = number.to_digit(10).unwrap();
        sum += number;
    }
    if k != 1 {
        sum = (superDigit(&(sum as i32).to_string(), 1) * k) as u32;
    }
    superDigit(&(sum as i32).to_string(), 1) * 1
}

fn counter_game(n: i64) -> String {
    //Time complexity: O(log(n))
    //Space complexity (ignoring input): O(1)
    let mut n = n;
    let mut count_turns = 0;
    while n > 1 {
        let n_is_power_2 = n & (n - 1) == 0;
        if n_is_power_2 {
            while n > 1 {
                n = n >> 1;
                count_turns += 1;
            }
        } else {
            let mut pow_2 = 1;
            while pow_2 * 2 < n {
                pow_2 = pow_2 << 1;
            }
            n = n - pow_2;
            count_turns += 1;
        }
    }

    if count_turns % 2 == 0 {
        return String::from("Richard");
    } else {
        return String::from("Louise");
    }
}

fn sum_xor(n: i64) -> i64 {
    // Time complexity: O(log(n))
    // Space complexity (ignoring input): O(1)
    let mut n = n;
    let mut zeros_in_binary = 0;
    while n > 1 {
        if n & 1 == 0 {
            zeros_in_binary += 1;
        }
        n = n >> 1;
    }

    // The answer is that the number can have 1 or 0 in the positions where 'n' has 0, so 2 to the n
    return 1<<zeros_in_binary
}
