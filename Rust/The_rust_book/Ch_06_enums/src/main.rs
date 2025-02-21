#[derive(Debug)]
enum State {
    Alabama,
    Alaska,
}
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(State),
}
fn value_in_cents(coin:Coin) -> u8 {
    match coin{
        Coin::Penny => {
            println!("Lucky penny!");
            1
        },
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {:?}!", state);
            25
        },
    }
}

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i+1),
    }
}
fn main() {
    let coin = Coin::Penny;
    value_in_cents(coin);
    let coin = Coin::Quarter(State::Alaska);
    value_in_cents(coin);
    println!("{:?}", plus_one(Some(5)));
    println!("{:?}", plus_one(None));
}

