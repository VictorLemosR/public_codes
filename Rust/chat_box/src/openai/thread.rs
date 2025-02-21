use std::time::Duration;

use async_openai::{
    config::OpenAIConfig,
    types::{
        CreateAssistantToolFileSearchResources, CreateAssistantToolResources, CreateRunRequest,
        CreateThreadRequest, RunStatus,
    },
    Client,
};
use color_eyre::eyre::eyre;
use serde::{Deserialize, Serialize};
use tokio::time::sleep;

use crate::{
    openai::msg::get_text_content,
    utils::files::{save_to_json, thread_path},
    Result,
};

use super::{msg::user_msg, start, AI};

const POLLING_DURATION_MS: u64 = 500;

#[derive(Debug, Deserialize, Serialize)]
pub struct ThreadId {
    thread_id: String,
}

pub async fn load_or_create(
    chat_bot: &AI,
) -> Result<String> {
    let open_ai_client = chat_bot.client()?;
    let thread_path = thread_path()?;

    println!("->> chat_bot; load_or_create function; thread.rs\n{:?}", chat_bot.recreate_thread()?);
    if chat_bot.recreate_thread()? && thread_path.exists() {
        std::fs::remove_file(&thread_path)?;
    }

    let thread_id = if let Ok(thread_id) =
        crate::utils::files::load_from_json::<ThreadId>(thread_path.clone())
    {
        println!(">> thread_id loaded");
        get_thread(open_ai_client, &thread_id.thread_id)
            .await
            .map_err(|_| eyre!("Cannot find thread_id for {}", &thread_id.thread_id))?
    } else {
        let thread_id = create_thread(chat_bot).await?;
        println!(">> thread_id created");
        save_to_json(
            &thread_path,
            &ThreadId {
                thread_id: thread_id.clone(),
            },
        )?;
        thread_id
    };
    Ok(thread_id)
}

pub async fn create_thread(
    chat_bot: &AI
) -> Result<String> {
    let vector_id = chat_bot.vector_id()?;
    let open_ai_client = chat_bot.client()?;

    let open_ai_threads = open_ai_client.threads();

    let res = open_ai_threads
        .create(CreateThreadRequest {
            tool_resources: Some(CreateAssistantToolResources {
                file_search: Some(CreateAssistantToolFileSearchResources {
                    vector_store_ids: Some(vec![vector_id.to_string()]),
                    ..Default::default()
                }),
                code_interpreter: None,
            }),
            ..Default::default()
        })
        .await?;

    Ok(res.id)
}

pub async fn get_thread(open_ai_client: &Client<OpenAIConfig>, thread_id: &str) -> Result<String> {
    let open_ai_threads = open_ai_client.threads();

    let thread_obj = open_ai_threads.retrieve(thread_id).await?;

    Ok(thread_obj.id)
}

pub async fn run_thread_msg(msg: &str) -> Result<String> {
    let ai_bot = start().await?;

    let msg = user_msg(msg);
    let open_ai_client = ai_bot.client()?;
    let assistant_id = ai_bot.assistant_id()?;
    let thread_id = ai_bot.thread_id()?;

    let _message_object = open_ai_client
        .threads()
        .messages(thread_id)
        .create(msg)
        .await?;

    let run_request = CreateRunRequest {
        assistant_id: assistant_id.to_string(),
        ..Default::default()
    };

    let run = open_ai_client
        .threads()
        .runs(thread_id)
        .create(run_request)
        .await?;

    loop {
        println!(">");
        let run = open_ai_client
            .threads()
            .runs(thread_id)
            .retrieve(&run.id)
            .await?;
        println!("<");
        match run.status {
            RunStatus::Completed => {
                println!("\n");
                return get_first_thread_msg_content(open_ai_client, thread_id).await;
            }
            RunStatus::Queued | RunStatus::InProgress => (),
            other => return Err(eyre!("ERROR WHILE RUNNING: {:?}", other)),
        }
        sleep(Duration::from_millis(POLLING_DURATION_MS)).await;
    }
}

pub async fn get_first_thread_msg_content(
    open_ai_client: &Client<OpenAIConfig>,
    thread_id: &str,
) -> Result<String> {
    const QUERY: [(&str, &str); 1] = [("limit", "1")];

    let messages = open_ai_client
        .threads()
        .messages(thread_id)
        .list(&QUERY)
        .await?;

    let msg = messages.data.into_iter().next().expect("No message found");
    let text = get_text_content(msg)?;
    Ok(text)
}
