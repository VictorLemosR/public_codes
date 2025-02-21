//Tutorial: https://github.com/fogarecious/iced_tutorial/blob/main/tutorial/more_than_one_page.md
use iced::{
    widget::{button, column, text},
    Sandbox, Settings,
};

fn main() -> iced::Result {
    MyApp::run(Settings::default())
}

enum Page {
    A,
    B,
}

#[derive(Debug, Clone)]
enum MyAppMessage {
    GoToBButtonPressed,
    GoToAButtonPressed,
}

struct MyApp {
    page: Page,
}

impl Sandbox for MyApp {
    type Message = MyAppMessage;

    fn new() -> Self {
        Self { page: Page::A }
    }

    fn title(&self) -> String {
        String::from("My App")
    }

    fn update(&mut self, message: Self::Message) {
        self.page = match message {
            MyAppMessage::GoToBButtonPressed => Page::B,
            MyAppMessage::GoToAButtonPressed => Page::A,
        }
    }

    fn view(&self) -> iced::Element<Self::Message> {
        match self.page {
            Page::A => column![
                text("Page A"),
                button("Go to B").on_press(MyAppMessage::GoToBButtonPressed),
            ],
            Page::B => column![
                text("Page B"),
                button("Go to A").on_press(MyAppMessage::GoToAButtonPressed),
            ],
        }
        .into()
    }
}
