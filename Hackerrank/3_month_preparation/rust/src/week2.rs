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

pub fn counting_sort(arr: &[i32]) -> Vec<i32> {
    //Time complexity: O(n+k) or just O(n), since k is constant
    //Space complexity (ignoring input): O(k) or just O(1), since k is constant
    let mut frequency_arr = vec![0; 100];
    for &number in arr {
        frequency_arr[number as usize] += 1;
    }

    frequency_arr
}

pub fn counting_valleys(steps: i32, path: &str) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut height = 0;
    let mut valleys = 0;

    for letter in path.chars() {
        if letter == 'U' {
            height += 1;
        }
        if letter == 'D' {
            height -= 1;
            if height == -1 {
                valleys += 1
            }
        }
    }
    valleys
}

pub fn pangrams(s: &str) -> String {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut bit_mask = 0;
    for letter in s.to_lowercase().chars() {
        if ('a'..='z').contains(&letter) {
        let bit_pos = letter as u32 - 'a' as u32;
        bit_mask |= 1 << bit_pos;
        };
    }
    if bit_mask == (1 << 26) - 1 {
        return "pangram".to_string();
    };

    "not pangram".to_string()
}

pub fn mars_exploration(s: &str) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let sos_array: Vec<_> = "SOS".chars().collect();
    let mut changed_letters = 0;
    for (index, letter) in s.char_indices(){
        if letter != sos_array[index%3]{
            changed_letters += 1;
        }
    }
    changed_letters
}
