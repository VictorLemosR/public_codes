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
