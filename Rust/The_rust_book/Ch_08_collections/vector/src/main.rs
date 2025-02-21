fn main() {
    let v = vec![1, 2, 3];
    println!("{:?}", v);

    let v: Vec<i32> = Vec::new();
    println!("{:?}", v);

    let mut v = vec![1, 2, 3];

    v.push(8);

    println!("{:?}", v);

    //2 types of access on vectors
    let x: &i32 = &v[2];

    let y: Option<&i32> = v.get(20);
    match y {
        Some(&value) => println!("value is {}", &value),
        None => println!("Index out of bounds. Max index is {}", v.len() - 1),
    }
    println!("value is {}", x);

    for element in &v {
        println!("element: {}", element);
        let plus_one = element + 1;
        println!("{}\n", plus_one);
    }

    for (i, &element) in v.iter().enumerate() {
        println!("index: {}, element: {}", i, element);
        let plus_one = element + 1;
        println!("{}\n", plus_one);
    }

    for element in &mut v {
        *element += 1;
        println!("element: {}", element);
    }

    let mut v = Vec::new();
    let s = String::from("Hello ");
    v.push(s);
    v[0].push_str("world");
    //println!("original: {}", s);
    println!("new: {}", v[0]);

    // Storing multiple types in a vector
    enum SpreadsheetCell {
        Int(i32),
        Float(f64),
        Text(String),
    }

    let row = vec![
        SpreadsheetCell::Int(3),
        SpreadsheetCell::Text(String::from("blue")),
        SpreadsheetCell::Float(10.12),
    ];
}
