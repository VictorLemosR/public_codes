pub fn permuting_two_arrays(k: i32, A: &[i32], B: &[i32]) -> String {
    //Time complexity: O(n*log(n))
    //Space complexity (ignoring input): O(n)
    let mut A = A.to_vec();
    A.sort_unstable();
    let mut B = B.to_vec();
    B.sort_unstable_by(|x, y| y.cmp(x));
    for (index, a_value) in A.iter().enumerate() {
        let b_value = B[index];
        if a_value + b_value < k {
            return "NO".to_string();
        }
    }

    "YES".to_string()
}

pub fn subarray_division_2(s: &[i32], d: i32, m: i32) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(1)
    let mut ways_to_divide = 0;
    let mut sum: i32 = s[0..m as usize].iter().sum();
    if sum == d {
        ways_to_divide += 1
    }
    for index in 1..(s.len() - m as usize + 1) {
        sum += s[index + m as usize - 1] - s[index - 1];
        if sum == d {
            ways_to_divide += 1
        }
    }

    ways_to_divide
}

//XOR Strings 3
fn main() {
    read_input();
}

fn read_input() {
    let mut buffer = String::new();
    loop {
        let read_line_result = std::io::stdin().read_line(&mut buffer);
        match read_line_result {
            Ok(0) => break,
            Ok(_n) => (),
            Err(error) => println!("error: {:?}", error),
        }
    }
    treat_input(buffer)
}
fn treat_input(buffer: String) {
    let buffer = buffer.split('\n').collect::<Vec<_>>();
    xor_strings_3(buffer[0], buffer[1]);
}

fn xor_strings_3(s1: &str, s2: &str) {
    let _ = s1
        .chars()
        .zip(s2.chars())
        .map(|(a, b)| if a == b { print!("0") } else { print!("1") })
        .collect::<Vec<_>>();
}

fn sales_by_match(n: i32, ar: &[i32]) -> i32 {
    //Time complexity: O(n)
    //Space complexity (ignoring input): O(n)
    let mut socks_hash = std::collections::HashMap::new();
    for sock in ar {
        match socks_hash.get(sock) {
            Some(v) => socks_hash.insert(sock, v + 1),
            None => socks_hash.insert(sock, 1),
        };
    }
    let mut total_pairs = 0;
    for values in socks_hash.values() {
        total_pairs += values / 2;
    }
    total_pairs
}
