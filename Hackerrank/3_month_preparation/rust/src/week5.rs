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
fn sansa_and_xor(arr: &[i32]) {}
