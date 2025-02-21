//Tutorial: https://github.com/fogarecious/iced_tutorial/blob/main/tutorial/custom_styles.md
use iced::{
    theme,
    widget::{column, radio},
    Color, Sandbox, Settings,
};

fn main() -> iced::Result {
    MyApp::run(Settings::default())
}

#[derive(Debug, Clone)]
enum MyAppMessage {
    Choose(String),
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
            radio("Choice A", "A", Some("A"), |s| MyAppMessage::Choose(
                s.to_string()
            ))
            .style(theme::Radio::Custom(Box::new(RadioStyle))),
            radio("Choice B", "B", Some("A"), |s| MyAppMessage::Choose(
                s.to_string()
            ))
            .style(theme::Radio::Custom(Box::new(RadioStyle))),
            radio("Choice C", "C", Some("A"), |s| MyAppMessage::Choose(
                s.to_string()
            )),
        ]
        .into()
    }
}

struct RadioStyle;

impl radio::StyleSheet for RadioStyle {
    type Style = iced::Theme;

    fn active(&self, style: &Self::Style, is_selected: bool) -> radio::Appearance {
        radio::Appearance {
            text_color: Some(if is_selected {
                Color::from_rgb(0., 0., 1.)
            } else {
                Color::from_rgb(0.5, 0.5, 0.5)
            }),
            ..style.active(&theme::Radio::Default, is_selected)
        }
    }

    fn hovered(&self, style: &Self::Style, is_selected: bool) -> radio::Appearance {
        style.hovered(&theme::Radio::Default, is_selected)
    }
}
