use std::collections::HashMap as hash;
fn main() {
    let mut scores = hash::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
    println!("{:?}", scores);
    scores.insert(String::from("Blue"), 40);
    println!("{:?}", scores);

    let blue_score = scores.get("Blue").copied().unwrap_or(0);
    println!("{}", blue_score);

    for (key, value) in &scores {
        println!("{}: {}", key, value);
    }

    scores.entry(String::from("Blue")).or_insert(100);
    scores.entry(String::from("Red")).or_insert(100);
    println!("{:?}", scores);

    let text = "hello world wonderful world";

    let mut map = hash::new();

    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;
    }
    println!("{:?}", map);

    for i in 0..9 / 2 {
        println!("{}", i);
    }
}
