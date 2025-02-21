use async_openai::types::{CreateMessageRequest, CreateMessageRequestContent, MessageContent, MessageObject, MessageRole};
use color_eyre::eyre::eyre;

use crate::Result;

pub fn user_msg(content: impl Into<String>) -> CreateMessageRequest {
    CreateMessageRequest {
        role: MessageRole::User,
        content: CreateMessageRequestContent::Content(content.into()),
        ..Default::default()
    }
}

pub fn get_text_content(msg: MessageObject) -> Result<String> {
    let msg_content = msg
        .content
        .into_iter()
        .next()
        .expect("No message content found");

    let text = match msg_content{
        MessageContent::Text(text)=>text.text.value,
        MessageContent::ImageFile(_)=>{
            return Err(eyre!("Image not supported yet"))

        },
        MessageContent::Refusal(_)=>{
            return Err(eyre!("Message content Refusal not supported yet"))
        },
        MessageContent::ImageUrl(_)=>{
            return Err(eyre!("ImageUrl not supported yet"))
        }
    };

    Ok(text)
}
