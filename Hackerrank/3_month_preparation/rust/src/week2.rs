pub fn lonely_integer(a: &[i32]) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(n)
    let mut numbers_dictionary = std::collections::HashMap::new();

    for &number in a {
        match numbers_dictionary.get(&number) {
            Some(n) => numbers_dictionary.insert(number, n + 1),
            None => numbers_dictionary.insert(number, 1),
        };
    }

    for (&key, &value) in numbers_dictionary.iter() {
        if value == 1 {
            return key;
        }
    }

    0
}

fn lonely_integer_elegant(a: &[i32]) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut result = 0;
    for number in a {
        result ^= number;
    }
    result
}

pub fn grading_students(grades: &[i32]) -> Vec<i32> {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(n)
    let mut new_grades = Vec::new();

    for &grade in grades {
        if (grade < 37) && ((grade % 5) > 2) {
            new_grades.push(grade + 5 - (grade % 5));
        } else {
            new_grades.push(grade);
        }
    }

    new_grades
}

pub fn flippings_bits(n: i64) -> i64 {
    //Time complexity: O(1)
    //Space complexity (ignoring input): O(1)
    (2_i64.pow(32) - 1) ^ n
}

pub fn diagonal_difference(arr: &[Vec<i32>]) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut diagonal_1 = 0;
    let mut diagonal_2 = 0;
    for index in 0..arr.len() {
        diagonal_1 += arr[index][index];
        diagonal_2 += arr[arr.len() - 1 - index][index];
    }
    (diagonal_1 - diagonal_2).abs()
}
