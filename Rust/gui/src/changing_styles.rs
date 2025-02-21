//Tutorial: https://github.com/fogarecious/iced_tutorial/blob/main/tutorial/changing_styles.md
use iced::{
    theme,
    widget::{button, column, row, text},
    Color, Sandbox, Settings,
};

fn main() -> iced::Result {
    MyApp::run(Settings::default())
}

#[derive(Debug, Clone)]
enum MyAppMessage {
    DummyMessage,
}

struct MyApp;

impl Sandbox for MyApp {
    type Message = MyAppMessage;

    fn new() -> Self {
        Self
    }

    fn title(&self) -> String {
        String::from("My App")
    }

    fn update(&mut self, _message: Self::Message) {}

    fn view(&self) -> iced::Element<Self::Message> {
        column![
            text("Ready?").style(Color::from_rgb(1., 0.6, 0.2)),
            row![
                button("Cancel")
                    .style(theme::Button::Secondary)
                    .on_press(MyAppMessage::DummyMessage),
                button("Go!~~")
                    .style(theme::Button::Primary)
                    .on_press(MyAppMessage::DummyMessage),
            ],
        ]
        .into()
    }
}
