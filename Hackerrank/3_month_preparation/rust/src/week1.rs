use std::collections::HashMap;

pub fn plus_minus(arr: &[i32]) {
    let len_arr = arr.len() as f64;
    let mut positive_numbers = 0;
    let mut zero_numbers = 0;
    for number in arr.iter().skip(1) {
        if number > &0 {
            positive_numbers += 1;
        }
        if number == &0 {
            zero_numbers += 1;
        }
    }

    let positive_numbers = positive_numbers as f64;
    let zero_numbers = zero_numbers as f64;

    println!("{:.6}", (positive_numbers / len_arr));
    println!(
        "{:.6}",
        ((len_arr - zero_numbers - positive_numbers) / len_arr)
    );
    println!("{:.6}", (zero_numbers / len_arr));
}

pub fn mini_max_sum(arr: &[i32]) {
    let mut sum = 0_i64;
    let mut minimum_number = arr[0] as i64;
    let mut maximum_number = arr[0] as i64;
    for &number in arr.iter().skip(1) {
        sum += number as i64;
        if (number as i64) < minimum_number {
            minimum_number = number as i64
        }
        if (number as i64) > maximum_number {
            maximum_number = number as i64
        }
    }
    print!("{} {}", sum - maximum_number, sum - minimum_number);
}

pub fn time_conversion(s: &str) -> String {
    let s_len = s.len();
    let hour = &s[0..2];
    let am_pm = &s[s_len - 2..];
    let mut hour_int = hour.parse::<i8>().expect("To be a number");
    if hour == "12" {
        if am_pm == "AM" {
            hour_int = 00;
        }
        if am_pm == "PM" {
            hour_int = 12;
        }
    } else if am_pm == "PM" {
        hour_int += 12;
    }

    format!("{hour_int:02}{}", &s[2..s_len - 2])
}

pub fn breaking_the_records(scores: &[i32]) -> Vec<i32> {
    let mut minimum_score = scores[0];
    let mut maximum_score = scores[0];
    let mut records = vec![0, 0];

    for &score in scores.iter().skip(1) {
        println!("{}", score);
        if score < minimum_score {
            minimum_score = score;
            records[1] += 1;
        }
        if score > maximum_score {
            maximum_score = score;
            records[0] += 1;
        }
    }

    records
}

//Camel case functions
fn split(words: &str) -> String {
    let words = match words.strip_suffix("()") {
        Some(stripped) => stripped,
        None => words,
    };
    let mut chars_iter = words.chars();
    let mut splitted_words = chars_iter
        .next()
        .expect("To have found the first letter")
        .to_lowercase()
        .to_string();
    for letter in chars_iter {
        if letter.is_uppercase() {
            splitted_words.push(' ');
            splitted_words.push_str(&letter.to_lowercase().collect::<String>());
        } else {
            splitted_words.push(letter);
        }
    }

    splitted_words
}

fn combine(words: &str, capitalize: bool) -> String {
    let mut combined_words = if capitalize {
        words
            .chars()
            .next()
            .expect("To have found first letter")
            .to_uppercase()
            .collect::<String>()
    } else {
        words
            .chars()
            .next()
            .expect("To have found first letter")
            .to_string()
    };

    let mut index = 1;
    while index < words.len() {
        let letter = words.chars().nth(index).expect("To have found index");
        if letter == ' ' {
            index += 1;
            combined_words.push_str(
                &words
                    .chars()
                    .nth(index)
                    .expect("To have found index")
                    .to_uppercase()
                    .to_string(),
            )
        } else {
            combined_words.push(letter);
        }
        index += 1;
    }

    combined_words
}
pub fn treat_input(input: String) {
    let lines: Vec<&str> = input.split("\r\n").collect();
    for line in lines {
        let words: Vec<&str> = line.split(";").collect();
        if words[0] == "S" {
            let word = split(words[2]);
            println!("{}", word);
        }
        if words[0] == "C" {
            let capitalize = words[1] == "C";
            let mut word = combine(words[2], capitalize);
            if words[1] == "M" {
                word.push_str("()");
            }
            println!("{}", word);
        }
    }
}

pub fn read_input() {
    let mut input = String::new();
    loop {
        let read_line_result = std::io::stdin().read_line(&mut input);
        match read_line_result {
            Ok(0) => break,
            Ok(_n) => (),
            Err(error) => println!("error: {error}"),
        }
    }
    treat_input(input)
}

pub fn divisible_sum_pairs(n: i32, k: i32, ar: &[i32]) -> i32 {
    //Time complexity: O(n+k)
    //Space complexity (ignoring input): O(k)
    let mut remainder_dictionary = std::collections::HashMap::new();
    for number in ar {
        let remainder = number % k;
        match remainder_dictionary.get(&remainder) {
            Some(n) => remainder_dictionary.insert(remainder, n + 1),
            None => remainder_dictionary.insert(remainder, 1),
        };
    }

    let mut total_pairs = 0;
    //For remainders 0 and k/2, the total pairs will be n choose 2
    println!(
        "->> remainder_dictionary <<- function: divisible_sum_pairs; file: week1.rs\n{:?}",
        remainder_dictionary
    );
    total_pairs += match remainder_dictionary.get(&0) {
        Some(n) => n * (n - 1) / 2,
        None => 0,
    };
    let k_is_pair = k % 2 == 0;
    if k_is_pair {
        total_pairs += match remainder_dictionary.get(&(k / 2)) {
            Some(n) => n * (n - 1) / 2,
            None => 0,
        };
    }

    for remainder in 1..(k + 1) / 2 {
        total_pairs += remainder_dictionary.get(&remainder).unwrap_or(&0)
            * remainder_dictionary.get(&(k - remainder)).unwrap_or(&0);
    }

    total_pairs
}

pub fn sparse_arrays(strings: &[String], queries: &[String]) -> Vec<i32> {
    //Time complexity: O(n+m)
    //Space complexity (ignoring input): O(n+m)
    let mut strings_hash_map = std::collections::HashMap::new();

    for string in strings {
        match strings_hash_map.get(&string) {
            Some(n) => strings_hash_map.insert(string, n + 1),
            None => strings_hash_map.insert(string, 1),
        };
    }

    let mut strings_matched = Vec::new();
    for query in queries {
        strings_matched.push(*strings_hash_map.get(&query).unwrap_or(&0));
    }

    strings_matched
}
