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
