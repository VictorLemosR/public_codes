use leptos::prelude::*;
use leptos_meta::{provide_meta_context, MetaTags, Stylesheet, Title};
use leptos_router::{
    components::{Route, Router, Routes},
    path, StaticSegment,
};

#[cfg(feature = "ssr")]
use crate::openai::run_thread_msg;
#[cfg(feature = "ssr")]
use crate::openai::AI;
#[cfg(feature = "ssr")]
use std::sync::Arc;
#[cfg(feature = "ssr")]
use tokio::sync::Mutex;

pub fn shell(options: LeptosOptions) -> impl IntoView {
    view! {
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <AutoReload options=options.clone() />
                <HydrationScripts options/>
                <MetaTags/>
            </head>
            <body>
                <App/>
            </body>
        </html>
    }
}

#[component]
pub fn App() -> impl IntoView {
    // Provides context that manages stylesheets, titles, meta tags, etc.
    provide_meta_context();

    view! {
        // injects a stylesheet into the document <head>
        // id=leptos means cargo-leptos will hot-reload this stylesheet
        <Stylesheet id="leptos" href="/pkg/chat_box.css"/>

        // sets the document title
        <Title text="Welcome to Leptos"/>

        // content for this welcome page
        <Router>
            <main>
                <Routes fallback=|| "Page not found.".into_view()>
                    <Route path=StaticSegment("/counter") view=HomePage/>
                    <Route path=path!("/chat_box") view=ChatBox/>
                </Routes>
            </main>
        </Router>
    }
}

/// Renders the home page of your application.
#[component]
fn HomePage() -> impl IntoView {
    // Creates a reactive value to update the button
    let count = RwSignal::new(0);
    let on_click = move |_| *count.write() += 1;

    view! {
        <h1>"Welcome to Leptos!"</h1>
        <button on:click=on_click>"Click Me: " {count}</button>
    }
}
#[derive(Debug, Clone)]
struct ConversationEntry {
    row: u32,
    my_input: String,
    gpt_text: String,
}

impl ConversationEntry {
    fn new() -> Self {
        Self {
            row: 0,
            my_input: "".to_string(),
            gpt_text: "".to_string(),
        }
    }
}
#[server]
async fn ai_answer(user_msg: String) -> Result<String, ServerFnError> {
    println!("->> user_msg; ai_answer function; mod.rs\n{:?}", user_msg);
    if user_msg == String::from("") {
        return Ok("".to_string());
    }
    let msg = run_thread_msg(&user_msg)
        .await
        .expect("To have obtained an answer from gpt");

    println!("->> msg; ai_answer function; mod.rs\n{:?}", msg);
    Ok(msg)
}

#[component]
fn ChatBox() -> impl IntoView {
    let (input_text, input_set_text) = signal("".to_string());
    let (prompt, prompt_set) = signal("".to_string());

    let (data, set_data): (
        ReadSignal<Vec<ConversationEntry>>,
        WriteSignal<Vec<ConversationEntry>>,
    ) = signal(Vec::new());

    let submit_message = move || {
        leptos::logging::log!("submit_message");
        let input_read = input_text.get();
        if input_read.as_str() != "" {
            prompt_set.set(input_read);
            input_set_text.set("".to_string());
        }
    };

    let input_ref: NodeRef<leptos::html::Textarea> = NodeRef::new();
    let on_submit = {
        leptos::logging::log!("on_submit");
        move |_| {
            submit_message();
            let _ = input_ref.get().expect("to find the input box").focus();
        }
    };

    let gpt_answer = Resource::new(move || prompt.get(), move |text| ai_answer(text));

    view! {
        <div class="chat_container">
            <div class="output_box">
                <For
                    each=move || data.get()
                    key=|child| child.row
                    children=move |child| {
                        view! {
                            <div class="right">
                                <span class="right_bubble">{child.my_input}</span>
                            </div>
                            <div class="left">
                                <span>{child.gpt_text}</span>
                            </div>
                        }
                    }
                />
            </div>
            <Suspense fallback=move || view! { <p>"Loading chat box..."</p> } >
            <div class="input_and_button">
                <textarea
                    class="input_box"
                    node_ref=input_ref
                    on:input:target=move |ev| {
                        input_set_text.set(ev.target().value());
                    }
                    on:keydown=move |ev| {
                        if ev.key() == "Enter" {
                            ev.prevent_default();
                            submit_message();
                            leptos::logging::log!("Enter pressionado");
                        }
                    }
                    prop:value=input_text
                />
                <button class="send_button" on:click=on_submit>
                    "Send"
                </button>
            </div>
            </Suspense>
            <Suspense fallback=move || view! { <p>"Prompt: " {prompt.get_untracked()}</p> } >
            {move || {
                 gpt_answer.map(|text| {
                     let text_value = text.clone().expect("To be able to extract value from gpt_answer");
                     if text_value != "".to_string()
                     {
                         set_data.update(move |data| {
                             data.push(ConversationEntry {
                                 row: data.last().unwrap_or(&ConversationEntry::new()).row + 1,
                                 my_input: prompt.get_untracked(),
                                 gpt_text: text_value,
                             });
                         });
                     }
                     prompt_set.set("".to_string());
                     });
                }
            }
            </Suspense>
        </div>
    }
}
