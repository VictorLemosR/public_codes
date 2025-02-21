//Tutorial: https://leafheap.com/articles/iced-v0-12-tutorial-asynchronous-actions-with-commands
use iced::{
    advanced::graphics::futures::backend::default::Executor,
    widget::{button, column, row, scrollable, text, text_input},
    Application, Command, Element, Settings, Theme,
};

struct PrimeNumbersApp {
    result: Vec<usize>,
    text_value: String,
}

#[derive(Clone, Debug)]
enum Message {
    ButtonPress,
    TextInputted(String),
    ListOfPrimes(Vec<usize>),
}

impl Application for PrimeNumbersApp {
    type Message = Message;
    type Executor = Executor;
    type Theme = Theme;
    type Flags = ();

    fn new(_: ()) -> (Self, Command<Message>) {
        (
            Self {
                result: Vec::new(),
                text_value: String::new(),
            },
            Command::none(),
        )
    }

    fn title(&self) -> String {
        String::from("Prime numbers")
    }

    fn update(&mut self, message: Self::Message) -> Command<Message> {
        match message {
            Message::ButtonPress => {
                let number: Result<usize, _> = self.text_value.parse();
                if let Ok(number) = number {
                    return Command::perform(async move { list_of_primes(number) }, |value| {
                        Message::ListOfPrimes(value)
                    });
                }
                Command::none()
            }
            Message::TextInputted(input) => {
                self.text_value = input;
                Command::none()
            }
            Message::ListOfPrimes(primes) => {
                self.result = primes;
                Command::none()
            }
        }
    }

    fn view(&self) -> Element<'_, Self::Message> {
        let text_items = prime_numbers_items(&self.result);
        column!(
            row!(
                button(text("Calculate primes")).on_press(Message::ButtonPress),
                text_input("Numbers only", &self.text_value)
                    .on_input(|value| Message::TextInputted(value))
            )
            .spacing(50)
            .padding(50),
            scrollable(column(text_items)).width(200)
        )
        .align_items(iced::Alignment::Center)
        .into()
    }
}

pub fn interface_primes() -> iced::Result {
    PrimeNumbersApp::run(Settings::default())
}

fn prime_numbers_items(items: &Vec<usize>) -> Vec<Element<Message>> {
    let mut element_items = Vec::new();
    for i in items {
        element_items.push(text(i).into());
    }
    element_items
}

fn list_of_primes(n: usize) -> Vec<usize> {
    let mut prime_numbers = Vec::new();
    for i in 2..n {
        if is_prime(i) {
            prime_numbers.push(i);
        }
    }
    prime_numbers
}

fn is_prime(n: usize) -> bool {
    if n <= 1 {
        return false;
    }
    for possible_multiple in 2..n {
        if n % possible_multiple == 0 {
            return false;
        }
    }
    true
}
