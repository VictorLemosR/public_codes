//Aditional iced widgets: https://github.com/iced-rs/iced_aw/tree/main
mod counter;
mod grocery;
mod primes;
mod subscriptions;
mod checkbox;

//use counter::create_interface;
//use grocery::create_grocery;
use primes::interface_primes;


fn main() {
    //create_grocery();
    //subscriptions::interface_subscription();
    //checkbox::main();
    //interface_primes();
    //grocery::create_grocery();
    subscriptions::interface_subscription();
}
