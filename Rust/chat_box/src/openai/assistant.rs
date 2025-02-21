use async_openai::{
    config::OpenAIConfig,
    types::{AssistantObject, CreateAssistantRequest, ModifyAssistantRequest},
    Client,
};

use crate::Result;

use super::DEFAULT_QUERY;
const EMBEDDED_INSTRUCTIONS: &str = include_str!("..\\config_files\\instructions.md");

#[derive(Debug)]
pub struct AsstId(pub String);

pub async fn load_or_create(
    open_ai_client: &Client<OpenAIConfig>,
    assistant_name: &str,
    assistant_model: &str,
    recreate: bool,
) -> Result<String> {
    let assistant_object = find_by_name(open_ai_client, assistant_name).await?;
    let mut assistant_id = assistant_object.map(|o| o.id);

    if let (true, Some(assistant_id_ref)) = (recreate, assistant_id.as_ref()) {
        delete(open_ai_client, &AsstId(assistant_id_ref.to_string())).await?;
        assistant_id.take();

        println!("Assistant {} deleted", assistant_name);
    }

    if let Some(assistant_id) = assistant_id {
        println!("Assistant {:?} loaded", assistant_name);
        Ok(assistant_id)
    } else {
        let assistant_id = create(open_ai_client, assistant_name, assistant_model).await?;
        println!("Assistant {:?} created", assistant_name);
        Ok(assistant_id)
    }
}

async fn find_by_name(
    open_ai_client: &Client<OpenAIConfig>,
    name: &str,
) -> Result<Option<AssistantObject>> {
    let open_ai_assistants = open_ai_client.assistants();
    let assistants = open_ai_assistants.list(DEFAULT_QUERY).await?.data;
    let assistant_object = assistants
        .into_iter()
        .find(|a| a.name.as_ref().map(|n| n == name).unwrap_or(false));

    Ok(assistant_object)
}

pub async fn delete(open_ai_client: &Client<OpenAIConfig>, assistant_id: &AsstId) -> Result<()> {
    let open_ai_assistants = open_ai_client.assistants();

    open_ai_assistants.delete(&assistant_id.0).await?;
    Ok(())
}

pub async fn create(
    open_ai_client: &Client<OpenAIConfig>,
    assistant_name: &str,
    assistant_model: &str,
) -> Result<String> {
    let open_ai_assistants = open_ai_client.assistants();
    let assistant_object = open_ai_assistants
        .create(CreateAssistantRequest {
            model: assistant_model.to_string(),
            name: Some(assistant_name.to_string()),
            tools: Some(vec![
                async_openai::types::AssistantToolsFileSearch::default().into(),
            ]),
            ..Default::default()
        })
        .await?;
    upload_instructions(open_ai_client, &AsstId(assistant_object.id.clone())).await?;

    Ok(assistant_object.id)
}

pub async fn upload_instructions(
    open_ai_client: &Client<OpenAIConfig>,
    assistant_id: &AsstId,
) -> Result<()> {
    let open_ai_assistants = open_ai_client.assistants();
    let instruction_content = obtain_instructions()?;

    let modify = ModifyAssistantRequest {
        instructions: Some(instruction_content),
        ..Default::default()
    };
    open_ai_assistants.update(&assistant_id.0, modify).await?;
    Ok(())
}

pub fn obtain_instructions() -> Result<String> {
    let instrution_content = std::fs::read_to_string(EMBEDDED_INSTRUCTIONS)?;

    println!("instructions uploaded");
    println!(
        "->> instrution_content; obtain_instructions function; assistant.rs\n{:?}",
        instrution_content
    );
    Ok(instrution_content)
}
