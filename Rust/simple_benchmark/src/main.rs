use std::time::Instant;
fn main() {
    println!("Hello, world!");
    let start = Instant::now();
    for _ in 0..10_000 {}
    let time1 = start.elapsed();
    for _ in 0..100_000 {}
    let time2 = start.elapsed();
    println!("{:?}", time1);
    println!("{:?}", time2 - time1);
}
