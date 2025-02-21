fn main() {
    let mut s = String::new();
    println!("{}", s);
    let text = "hello world";
    let s = text.to_string();
    println!("{}", s);
    let s = String::from("hello world");
    println!("{}", s);
    let s = String::from("Olá, mundo");
    println!("{}", s);

    let mut s = String::from("foo");
    s.push_str("|bar");
    println!("{}", s);
    let mut s = String::from("foo");
    let s2 = "|bar";
    s = s + &s2;
    println!("{}", s);
    let s = format!("foo{}", &s2);
    println!("{}", s);
    //let s2 = s[0]; //error
    let s2 = &s[0..1];
    let s = String::from("á, mundo");
    //let s2 = &s[0..1]; //error again, more than 1 byte in this range because of accent.
    //Careful when using slices in strings
}
