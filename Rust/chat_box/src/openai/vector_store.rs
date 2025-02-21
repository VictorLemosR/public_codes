use async_openai::{
    config::OpenAIConfig,
    types::{CreateVectorStoreRequest, VectorStoreExpirationAfter, VectorStoreObject},
    Client,
};

use crate::Result;

use super::DEFAULT_QUERY;

pub async fn associate_files_vector(
    open_ai_client: &Client<OpenAIConfig>,
    files_id: Vec<String>,
    vector_id: &str,
) -> Result<()> {
    //DELETAR association com os vector_stores
    open_ai_client
        .vector_stores()
        .file_batches(vector_id)
        .create(async_openai::types::CreateVectorStoreFileBatchRequest {
            file_ids: files_id,
            chunking_strategy: None,
        })
        .await?;
    Ok(())
}

pub async fn load_or_create(
    open_ai_client: &Client<OpenAIConfig>,
    recreate: bool,
) -> Result<(String, bool)> {
    let vector_name = format!("{}--transcript--vector", std::env::var("USERNAME")?);
    let vector_object = find_by_name(open_ai_client, &vector_name).await?;
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .expect("Error obtaining current time")
        .as_secs();
    let mut vector_id = match vector_object {
        Some(o)
            if o.expires_at
                .map_or(false, |expires_at| u64::from(expires_at) > now) =>
        {
            Some(o.id)
        }
        _ => None,
    };

    println!("->> vector_id; load_or_create function; vector_store.rs\n{:?}", vector_id);
    if let (true, Some(vector_id_ref)) = (recreate, vector_id.as_ref()) {
        delete(open_ai_client, vector_id_ref).await?;
        vector_id.take();

        println!("vector {} deleted", vector_name);
    }

    let recreate_thread = false;
    if let Some(vector_id) = vector_id {
        println!("vector {:?} loaded", vector_name);
        Ok((vector_id, recreate_thread))
    } else {
        println!("vector {:?} created", vector_name);

        let recreate_thread = true;
        let vector_id = create(open_ai_client, vector_name).await?;
        Ok((vector_id, recreate_thread))
    }
}

pub async fn delete(open_ai_client: &Client<OpenAIConfig>, vector_id: &str) -> Result<()> {
    let open_ai_vectors = open_ai_client.vector_stores();

    open_ai_vectors.delete(vector_id).await?;
    Ok(())
}

async fn create(open_ai_client: &Client<OpenAIConfig>, vector_name: String) -> Result<String> {
    let vector_store = open_ai_client
        .vector_stores()
        .create(CreateVectorStoreRequest {
            name: Some(vector_name),
            expires_after: Some(VectorStoreExpirationAfter {
                anchor: "last_active_at".to_string(),
                days: 5,
            }),
            ..Default::default()
        })
        .await?;
    Ok(vector_store.id)
}

async fn find_by_name(
    open_ai_client: &Client<OpenAIConfig>,
    name: &str,
) -> Result<Option<VectorStoreObject>> {
    let open_ai_vector_stores = open_ai_client.vector_stores();
    let vector_stores = open_ai_vector_stores.list(DEFAULT_QUERY).await?.data;
    let vector_store_object = vector_stores
        .into_iter()
        .find(|a| a.name.as_ref().map(|n| n == name).unwrap_or(false));

    Ok(vector_store_object)
}
