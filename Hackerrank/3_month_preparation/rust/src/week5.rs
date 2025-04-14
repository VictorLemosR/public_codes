fn max_min(k: i32, arr: &[i32]) -> i32 {
    //Time complexity: O(n*log(n))
    //Space complexity (ignoring input): O(n)
    let mut arr = arr.to_vec();
    let k = k as usize;
    arr.sort_unstable();
    let mut minimun_unfairness = arr[k - 1] - arr[0];
    for index in 1..(arr.len() - k + 1) {
        if minimun_unfairness > arr[k - 1 + index] - arr[index] {
            minimun_unfairness = arr[k - 1 + index] - arr[index];
        };
    }
    minimun_unfairness
}

fn strong_password(n: i32, password: &str) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let special_characters: std::collections::HashSet<char> = "!@#$%^&*()-+".chars().collect();

    let mut add_lower = true;
    let mut add_upper = true;
    let mut add_special = true;
    let mut add_number = true;
    for letter in password.chars() {
        if letter.is_uppercase() {
            add_upper = false;
        }
        if letter.is_lowercase() {
            add_lower = false;
        }
        if letter.is_numeric() {
            add_number = false;
        }
        if special_characters.contains(&letter) {
            add_special = false;
        }
    }

    let mut characters_to_add: i32 = 0;

    if add_lower {
        characters_to_add += 1;
    }
    if add_upper {
        characters_to_add += 1;
    }
    if add_special {
        characters_to_add += 1;
    }
    if add_number {
        characters_to_add += 1;
    }

    if (password.len() + characters_to_add as usize) < 6 {
        return 6 - password.len() as i32;
    }
    characters_to_add
}

fn dynamic_array(n: i32, queries: &[Vec<i32>]) -> Vec<i32> {
    //Time complexity: O(n+q)
    //Space complexity (ignoring input): O(n+q)
    let mut array = Vec::with_capacity(n as usize);
    for _ in 0..n {
        array.push(Vec::new());
    }
    let mut result_array = Vec::new();
    let mut last_answer = 0;
    for query in queries {
        let idx = ((query[1] ^ last_answer) % n) as usize;
        if query[0] == 1 {
            array[idx].push(query[2])
        }
        if query[0] == 2 {
            let size = query[2] as usize % (array[idx].len());
            last_answer = array[idx][size];
            result_array.push(last_answer);
        }
    }
    result_array
}

fn missing_numbers(arr: &[i32], brr: &[i32]) -> Vec<i32> {
    //Time complexity: O(a+b)
    //Space complexity (ignoring input): O(a+b)
    let mut arr_hash = std::collections::HashMap::new();
    for value in arr {
        match arr_hash.get(value) {
            Some(f) => arr_hash.insert(value, f + 1),
            None => arr_hash.insert(value, 1),
        };
    }
    let mut brr_hash = std::collections::HashMap::new();
    for value in brr {
        match brr_hash.get(value) {
            Some(f) => brr_hash.insert(value, *f + 1),
            None => brr_hash.insert(value, 1),
        };
    }

    let mut missing_values = Vec::new();
    for (&key, frequency_b) in brr_hash.iter() {
        let frequency_a = arr_hash.get(key).unwrap_or(&0);
        if frequency_a <= frequency_b {
            missing_values.push(*key);
        }
    }

    missing_values.sort_unstable();
    missing_values
}

fn full_countint_sort(arr: &[Vec<String>]) {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut sorted_array: Vec<String> = vec!["".to_string(); 101];
    for index in 0..arr.len() {
        let sorted_index = arr[index][0]
            .parse::<usize>()
            .expect("To be able to parse correctly");
        if index < arr.len() / 2 {
            sorted_array[sorted_index].push_str(" -");
        } else {
            sorted_array[sorted_index].push(' ');
            sorted_array[sorted_index].push_str(&arr[index][1]);
        }
    }
    let mut result_array = String::new();
    for string in sorted_array {
        if !string.is_empty() {
            if result_array.is_empty() {
                result_array = string[1..].to_string();
            } else {
                result_array.push_str(&string);
            }
        }
    }
    println!("{}", result_array);
}

fn grid_challenge(grid: &[String]) -> String {
    //Time complexity: O(n^2*log(n))
    //Space complexity (ignoring input): O(n)
    let mut sorted_grid = Vec::new();
    for string in grid {
        let mut vec_chars = string.chars().collect::<Vec<char>>();
        vec_chars.sort_unstable();
        sorted_grid.push(vec_chars);
    }
    for row in 0..sorted_grid.len() - 1 {
        for column in 0..sorted_grid[0].len() {
            if sorted_grid[row][column] > sorted_grid[row + 1][column] {
                return "NO".to_string();
            }
        }
    }
    return "YES".to_string();
}
fn sansa_and_xor(arr: &[i32]) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    //A number will appear in {(index+1)*(n-index)} subsequences
    //In case arr.len() is par, the appearences of any number will be par as well
    if arr.len() % 2 == 0 {
        return 0;
    }
    let mut xor_value = 0;
    for index in 0..arr.len() {
        let appearences = (index + 1) * (arr.len() - index);
        if appearences % 2 != 0 {
            xor_value ^= arr[index]
        }
    }
    return xor_value;
}
