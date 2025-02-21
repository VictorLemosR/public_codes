pub fn add_two(a: i32) -> i32 {
    if a < -10 {
        panic!("Negative number not allowed");
    }
    a + 2
}

#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn it_works() {
        let result = 2 + 2;
        println!("This message is not shown, because the test passes");
        assert_eq!(result, 4);
    }

    #[test]
    fn failing_test() {
        println!("This message is shown, because the test does not pass");
        panic!("This test will fail");
    }
    #[test]
    fn larger_can_hold_smaller() {
        let larger = Rectangle {
            width: 8,
            height: 7,
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };

        assert!(!smaller.can_hold(&larger));
    }
    #[test]
    fn it_adds_two() {
        assert_eq!(9, add_two(6), "Sum function did not add 2");
    }

    #[test]
    #[should_panic(expected = "Negative number not allowed")]
    fn negative_number() {
        add_two(-2);
    }

    #[test]
    fn it_works2() -> Result<(), String> {
        if 2 + 2 == 4 {
            Ok(())
        } else {
            Err("two plus two does not equal four".to_string())
        }
    }
    #[test]
    #[ignore]
    fn ignored_test() {
        for i in 0..1000000 {
            1 + 1;
        }
        println!("This test is ignored");
    }
}

//Run all tests that has some specific text
//cargo test works
