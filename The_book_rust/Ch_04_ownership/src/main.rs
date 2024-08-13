fn main() {
    let first = String::from("Ferris");
    let full = add_suffix(first.clone());
    let second = &first;
    println!("{full}");
    println!("{first}");
    println!("{second}");
    let x = 42;
    let y = double(x);
    println!("{x}, {y}");

    let x: Box<i32> = Box::new(-1);
    let x_abs1 = i32::abs(*x); // explicit dereference
    let x_abs2 = x.abs(); // implicit dereference
    assert_eq!(x_abs1, x_abs2);

    let r: &Box<i32> = &x;
    let r_abs1 = i32::abs(**r); // explicit dereference (twice)
    let r_abs2 = r.abs(); // implicit dereference (twice)
    assert_eq!(r_abs1, r_abs2);

    let s = String::from("Hello");
    let s_len1 = str::len(&s); // explicit reference
    let s_len2 = s.len(); // implicit reference
    assert_eq!(s_len1, s_len2);

    let mut v: Vec<i32> = vec![1, 2];
    let num = &mut v[1];
    *num += 1;
    println!("Third element is {}", num);
    println!("Third element is {}", *num);
    println!("Third element is {}", v[1]);
    v.push(4);
    v.push(4);

    let mut x = 1;
    let y = &x;
    let z = *y;
    x += 1;
    x += z;
    println!("{}", x);
    println!("{}", z);

    let n = 1;
    incr(n);
    println!("{n}");
    let mut n = 1;
    incr2(&mut n);
    println!("{n}");

    let mut s = String::from("hello");
    let _s2 = &s;
    let s3 = &mut s;
    s3.push_str(" world");
    //println!("{s2}");

    let name = vec![String::from("Ferris")];
    let first = &name[0];
    stringify_name_with_title(&name);
    println!("{}", first);

    let s = String::from("Hello world");
    let s_ref = &s;
    let s2 = s_ref;
    println!("{s2}");

    let mut s = String::from("hello world");
    first_word(&s);
    s.clear();

    let x = 1;
    let y = &x;
    let z = &x;
    println!("{x}, {y}, {z}");

    let mut v = vec![0, 1, 2, 3];
    let (r0, r1) = (&mut v[0..2], &mut v[2..4]);
    r0[0] += 1;
}

fn add_suffix(mut name: String) -> String {
    name.push_str(" Jr.");
    name
}

fn incr(mut _n: i32) {
    _n += 1
}

fn incr2(n: &mut i32) {
    *n += 1;
}

fn double(mut x: i32) -> i32 {
    x *= 2;
    x
}

fn stringify_name_with_title(name: &Vec<String>) -> String {
    let mut full = name.join(" ");
    full.push_str(" Esq.");
    full
}

fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[..i];
        }
    }

    &s[..]
}
