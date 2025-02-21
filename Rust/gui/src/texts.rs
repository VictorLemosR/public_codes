//Tutorial: https://github.com/fogarecious/iced_tutorial/blob/main/tutorial/text.md
use iced::{
    alignment::{Horizontal, Vertical},
    font::Family,
    widget::{column, text, text::Shaping, Text},
    Font, Length, Sandbox, Settings,
};

fn main() -> iced::Result {
    MyApp::run(Settings::default())
}

struct MyApp;

impl Sandbox for MyApp {
    type Message = ();

    fn new() -> Self {
        Self
    }

    fn title(&self) -> String {
        String::from("My App")
    }

    fn update(&mut self, _message: Self::Message) {}

    fn view(&self) -> iced::Element<Self::Message> {
        column![
            "Construct from &str",
            text("Construct from function"),
            Text::new("Construct from struct"),
            text("Different font").font(Font {
                family: Family::Fantasy,
                ..Font::DEFAULT
            }),
            text("Larger text").size(24),
            text("Special character 😊").shaping(Shaping::Advanced),
            text("Center")
                .width(Length::Fill)
                .horizontal_alignment(Horizontal::Center),
            text("Vertical center")
                .height(Length::Fill)
                .vertical_alignment(Vertical::Center),
        ]
        .into()
    }
}
