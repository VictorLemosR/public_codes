//Tutorial from: https://leafheap.com/articles/iced-tutorial-version-0-12
use iced::widget::{button, column, container, row, scrollable, text, text_input, Column};
use iced::{alignment, Element, Length, Padding, Sandbox, Settings};

struct GroceryList {
    grocery_items: Vec<String>,
    input_value: String,
}

#[derive(Debug, Clone)]
enum Message {
    InputValue(String),
    Submitted,
    DeleteItem(usize),
}

impl Sandbox for GroceryList {
    type Message = Message;

    fn new() -> GroceryList {
        Self {
            grocery_items: vec!["Top".to_owned(), "TR".to_owned(), "Small".to_owned()],
            input_value: String::default(),
        }
    }

    //Title of window
    fn title(&self) -> String {
        String::from("Fundos")
    }

    fn update(&mut self, message: Self::Message) {
        match message {
            Message::InputValue(value) => self.input_value = value,
            Message::Submitted => {
                self.grocery_items.push(self.input_value.clone());
                self.input_value = String::default()
            }
            Message::DeleteItem(index) => {
                self.grocery_items.remove(index);
            }
        }
    }

    fn theme(&self) -> iced::Theme {
        iced::Theme::Dark
    }

    fn view(&self) -> Element<Self::Message> {
        container(
            column!(
                row!(
                    text_input("Adicione um fundo", &self.input_value)
                        .on_input(|value| Message::InputValue(value))
                        .on_submit(Message::Submitted),
                    button("Submit").on_press(Message::Submitted)
                )
                .spacing(30)
                .padding(Padding::from(30)),
                items_list_view(&self.grocery_items),
            )
            .align_items(iced::Alignment::Center),
        )
        .height(Length::Fill)
        .width(Length::Fill)
        .align_x(alignment::Horizontal::Center)
        .align_y(alignment::Vertical::Center)
        .into()
    }
}
pub fn create_grocery() -> iced::Result {
    GroceryList::run(Settings::default())
}

fn items_list_view(items: &Vec<String>) -> Element<'static, Message> {
    println!("debugging 2");

    let mut column = Column::new()
        .spacing(20)
        .align_items(iced::Alignment::Center)
        .width(Length::Fill);

    for (index, value) in items.into_iter().enumerate() {
        column = column.push(grocery_item(index, value));
    }

    scrollable(container(column)).height(250).width(300).into()
}

fn grocery_item(index: usize, value: &str) -> Element<'static, Message> {
    row!(
        text(value),
        button("Delete").on_press(Message::DeleteItem(index))
    )
    .align_items(iced::Alignment::Center)
    .spacing(30)
    .into()
}
