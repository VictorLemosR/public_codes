mod week1;

fn main() {
    let arr = vec![3, 9, 10, 3, 2];
    //week1::plus_minus(&[1, -1, 0, 0, 0, 3, 5]);
    //week1::mini_max_sum(&arr);
    //let a = week1::time_conversion("12:00:03PM");
    //let a = week1::breaking_the_records(&arr);
    week1::divisible_sum_pairs(5, 3, &arr);
}
