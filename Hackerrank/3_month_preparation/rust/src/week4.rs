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
