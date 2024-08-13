fn main() {
    let x = 5;
    println!("The value of x is: {x}");
    let x = 6;
    println!("The value of x is: {x}");
    {
        let x = 7;
        println!("The value of x is: {x}");
    };

    println!("The value of x is: {x}");

    let guess: u32 = "42".parse().expect("Not a number!");
    println!("The value of guess is: {guess}");

    let x: u8 = 249;
    println!("The value of x is: {x}");

    let x = 30 % 7;
    println!("The value of x is: {x}");

    let bool_variable = true;
    println!("The value of bool_variable is: {bool_variable}");
    let bool_variable: bool = false;
    println!("The value of bool_variable is: {bool_variable}");
    let x: u32 = 1;
    let y = x - 1;
    println!("The value of y is: {y}");
    let tup: (u8, char) = (10, 'V');
    let (x, y) = tup;
    println!("The value of x, y is: {x}, {y}");
    let _x = tup.0;
    let _arr = [1, 3, 4];
    let _arr = [3; 5];

    let x: u16 = 10;
    println!("Double the value of x: {}", double(x));
    let x = {
        let y = 3;
        y + 1
    };
    {
        let x = 3;
        let _ = x + 1;
    };
    println!("The value of x is: {x}");
    let x = if x == 4 { 3 } else { 4 };
    println!("The value of x is: {x}");
    let z = if x == 3 { 3 } else { 4 };
    println!("The value of z is: {z}");
    let mut counter = 0;
    let char = loop {
        counter += 1;
        println!("Loop one more time");
        if counter == 10 {
            break 'C';
        }
    };
    println!("The value of char is: {char}");

    let mut counter = 0;
    let y = 'loop1: loop {
        counter += 1;
        println!("count={counter}");
        let mut inner_counter = 0;
        'loop2: loop {
            inner_counter += 1;
            println!("inner_count={inner_counter}");
            if counter==5 {
                break 'loop1 2;
            };
            if inner_counter==5 {
                break 'loop2;
            };
        }
    };
    println!("The value of y is: {y}");
    for number in ( 1..4 ).rev() {
        println!("{number}!");
    }
}

fn double(x: u16) -> u16 {
    if x == 3 {
        return 2;
    } else if x < 5 {
        return 3;
    } else {
        return 4;
    };
}
