//https://github.com/fogarecious/iced_tutorial/blob/main/tutorial/loading_images_asynchronously.md
use iced::{
    executor,
    widget::{button, column, container, image, image::Handle},
    Application, Command,
};
use tokio::{fs::File, io::AsyncReadExt};

fn main() -> iced::Result {
    MyApp::run(iced::Settings::default())
}

#[derive(Debug, Clone)]
enum MyMessage {
    Load,
    Loaded(Vec<u8>),
}

struct MyApp {
    image_handle: Option<Handle>,
    show_container: bool,
}

impl Application for MyApp {
    type Executor = executor::Default;
    type Message = MyMessage;
    type Theme = iced::Theme;
    type Flags = ();

    fn new(_flags: Self::Flags) -> (Self, iced::Command<Self::Message>) {
        (
            Self {
                image_handle: None,
                show_container: false,
            },
            Command::none(),
        )
    }

    fn title(&self) -> String {
        String::from("My App")
    }

    fn update(&mut self, message: Self::Message) -> iced::Command<Self::Message> {
        match message {
            MyMessage::Load => {
                self.show_container = true;
                return Command::perform(
                    async {
                        let mut file = File::open("ferris.png").await.unwrap();
                        let mut buffer = Vec::new();
                        file.read_to_end(&mut buffer).await.unwrap();
                        buffer
                    },
                    MyMessage::Loaded,
                );
            }
            MyMessage::Loaded(data) => self.image_handle = Some(Handle::from_memory(data)),
        }
        Command::none()
    }

    fn view(&self) -> iced::Element<Self::Message> {
        column![
            button("Load").on_press(MyMessage::Load),
            if self.show_container {
                match &self.image_handle {
                    Some(h) => container(image(h.clone())),
                    None => container("Loading..."),
                }
            } else {
                container("")
            },
        ]
        .padding(20)
        .into()
    }
}
