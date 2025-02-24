pub fn plus_minus(arr: &[i32]) {
    let len_arr = arr.len() as f64;
    let mut positive_numbers = 0;
    let mut zero_numbers = 0;
    for number in arr {
        if number > &0 {
            positive_numbers += 1;
        }
        if number == &0 {
            zero_numbers += 1;
        }
    }

    println!("->> len_arr; plus_minus function; week1.rs\n{:?}", len_arr);
    println!("->> positive_numbers; plus_minus function; week1.rs\n{:?}", positive_numbers);
    println!("->> zero_numbers; plus_minus function; week1.rs\n{:?}", zero_numbers);

    let positive_numbers = positive_numbers as f64;
    let zero_numbers = zero_numbers as f64;

    println!("{:.6}", (positive_numbers as f64 / len_arr));
    println!(
        "{:.6}",
        ((len_arr - zero_numbers - positive_numbers) / len_arr)
    );
    println!("{:.6}", (zero_numbers / len_arr));
}
