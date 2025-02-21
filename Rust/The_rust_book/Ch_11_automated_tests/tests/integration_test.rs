use Ch_11_automated_tests as ch_11;

#[test]
fn it_adds_two_integration() {
    println!("debugging 1");

    panic!("This test will fail");
    assert_eq!(8, ch_11::add_two(6), "Sum function did not add 2");
}
