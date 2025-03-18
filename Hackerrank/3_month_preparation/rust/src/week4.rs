fn picking_numbers(a: &[i32]) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(n)
    //You don't need to check for value-1 cases, because that is already checked by the value
    //itself + 1
    let mut a_dict = std::collections::HashMap::new();

    for &value in a {
        match a_dict.get(&value) {
            Some(f) => a_dict.insert(value, f + 1),
            None => a_dict.insert(value, 1),
        };
    }

    let mut longest_subsequence_len = 0;
    let mut current_subsequence_len = 0;
    for (value, frequency) in a_dict.iter() {
        let plus_len = *a_dict.get(&(*value + 1)).unwrap_or(&0);

        current_subsequence_len = frequency + plus_len;
        if current_subsequence_len > longest_subsequence_len {
            longest_subsequence_len = current_subsequence_len
        }
    }

    longest_subsequence_len
}

fn left_rotation(d: i32, arr: &[i32]) -> Vec<i32> {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(n)
    let mut new_array = Vec::new();
    for index in 0..arr.len() {
        new_array.push(arr[(index + d as usize) % arr.len()]);
    }

    new_array
}

fn number_line_jumps(x1: i32, v1: i32, x2: i32, v2: i32) -> String {
    //Time complexity: O(1)
    //Space complexity (ignoring input): O(1)
    if x1 == x2 {
        return "YES".to_string();
    }
    if v1 == v2 {
        return "NO".to_string();
    }

    let relative_speed = v2 - v1;
    let initial_distance = x1 - x2;
    let jumps = initial_distance as f32 / relative_speed as f32;
    if jumps == jumps.abs().floor() {
        return "YES".to_string();
    }

    "NO".to_string()
}

pub fn separate_numbers(s: &str) {
    //Time complexity: O(n^2)
    //Space complexity (ignoring input): O(n)
    //Python solution is way cleaner, made this one first and got lazy to rewrite
    let len_s = s.len();
    if len_s == 1 {
        println!("NO");
        return;
    }
    let vec_chars = s.chars().collect::<Vec<char>>();
    let mut start_number_size = 1;
    let mut number_size = start_number_size;
    let mut index: usize = start_number_size;
    let mut last_number = vec_chars[0]
        .to_string()
        .parse::<i64>()
        .expect("To have a number");
    let mut first_number = last_number;
    loop {
        if (last_number + 1) == (10u64.pow(number_size as u32) as i64) {
            number_size += 1;
        }
        let number = if number_size + index > len_s {
            last_number + 2
        } else {
            vec_chars[index..(number_size + index)]
                .iter()
                .collect::<String>()
                .parse::<i64>()
                .expect("To have a number")
        };
        if ((number - last_number) != 1) || (index + number_size > len_s) {
            start_number_size += 1;
            if start_number_size > (len_s + 1) / 2 {
                println!("NO");
                return;
            };
            number_size = start_number_size;
            index = 0;
            if vec_chars[0] == '0' {
                println!("NO");
                return;
            }
            last_number = vec_chars[0..start_number_size]
                .iter()
                .collect::<String>()
                .parse::<i64>()
                .expect("To have a number");
            first_number = last_number;
        } else {
            last_number = number;
        }
        index += number_size;
        if index == len_s {
            println!("YES {first_number}");
            return;
        }
    }
}
