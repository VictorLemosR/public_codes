struct User {
    active: bool,
    email: String,
}
fn main() {
    let user1 = User {
        active: false,
        email: format!("asrt"),
    };
    let email = user1.email;
    println!("{email}");
    let user2 = build_user(format!("sr"));
    let email = user2.email;
    println!("{email}");
    let user3 = User {
        email: format!("iiiienenen"),
        ..user2
    };
    struct Point {
        x: i32,
        y: i32,
    }
    let mut p = Point { x: 0, y: 0 };
    let x = &mut p.x;
    *x += 1;
    println!("{}, {}", p.x, p.y);

    let mut p = Point { x: 0, y: 0 };
    p.x += 1;
    let a = Point { y: 10, ..p };
    p.x += 1;
    println!("{} {}", p.x, a.x);

    let rectangle1 = Rectangle {
        width: 30,
        height: 50,
    };
    println!(
        "The area of the rectangle is {} square pixels.",
        area(&rectangle1)
    );
    println!("{:?}", rectangle1);
    println!("{:#?}", rectangle1);
    dbg!(&rectangle1);

    let mut rectangle2 = Rectangle2 {
        width: 30,
        height: 50,
    };
    println!("ret2: {}", rectangle2.area());
    rectangle2.double_width();
    println!("ret2: {}", rectangle2.area());
    let rectangle2 = Rectangle2::default_rectangle();
    println!("ret2: {}", rectangle2.area());

    let mut x = format!("ola");
    let y = &x;
    println!("{} {}", x, y);
    x += "asrt";

}

fn build_user(email: String) -> User {
    User {
        active: true,
        email,
    }
}
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn area(rectangle: &Rectangle) -> u32 {
    rectangle.width * rectangle.height
}

struct Rectangle2 {
    width: u32,
    height: u32,
}
impl Rectangle2 {
    fn area(&self) -> u32 {
        self.width * self.height
    }
    fn double_width(&mut self) {
        self.width *= 2;
    }
    fn default_rectangle() -> Self {
        Self {
            width: 20,
            height: 30,
        }
    }
}
