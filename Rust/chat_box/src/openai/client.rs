use std::collections::HashMap;
use std::path::PathBuf;

use async_openai::types::{CreateFileRequest, FilePurpose};
use async_openai::{config::OpenAIConfig, Client};
use serde::Deserialize;

use crate::utils::files::{list_files, load_from_toml};
use crate::Result;

const EMBEDDED_CONFIG_TOML: &str = include_str!("..\\config_files\\config.toml");

#[derive(Debug, Clone)]
pub struct AI {
    client: Client<OpenAIConfig>,
    assistant_id: String,
    config: Config,
    vector_id: String,
    thread_id: String,
    recreate_thread: bool,
}

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub name: String,
    pub model: String,
    pub secret_key: String,
    pub file_bundles: Vec<FileBundle>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct FileBundle {
    pub bundle_name: String,
    pub src_dir: String,
    pub dst_ext: String,
    pub src_globs: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct FileInfo {
    pub file_name: String,
    pub id: Option<String>,
    pub path: Option<PathBuf>,
}

impl AI {
    pub async fn new() -> Result<Self> {
        let config: Config = load_from_toml(None, Some(EMBEDDED_CONFIG_TOML))?;
        let client = create_client(&config.secret_key)?;
        let (vector_id, recreate_thread) = crate::openai::vector_store::load_or_create(&client, false).await?;
        let assistant_id =
            super::assistant::load_or_create(&client, &config.name, &config.model, false).await?;
        let thread_id = "".to_string();

        Ok(AI {
            config,
            client,
            assistant_id,
            vector_id,
            thread_id,
            recreate_thread,
        })
    }

    pub fn client(&self) -> Result<&Client<OpenAIConfig>> {
        Ok(&self.client)
    }

    pub fn assistant_id(&self) -> Result<&str> {
        Ok(&self.assistant_id)
    }
    pub fn vector_id(&self) -> Result<&str> {
        Ok(&self.vector_id)
    }
    pub fn thread_id(&self) -> Result<&str> {
        Ok(&self.thread_id)
    }
    pub fn update_thread_id(&mut self, thread_id: String) {
        self.thread_id = thread_id;
    }

    pub fn recreate_thread(&self) -> Result<bool> {
        Ok(self.recreate_thread)
    }

    pub fn update_recreate_thread(&mut self, boolean: bool) {
        self.recreate_thread = boolean;
    }

    pub fn file_bundles(&self) -> Result<&Vec<FileBundle>> {
        Ok(&self.config.file_bundles)
    }

    pub async fn update_files_client(&self) -> Result<Vec<FileInfo>> {
        let mut files_on_client = Vec::new();
        let client = self.client()?;

        let hash_files_client = self.query_files_on_client(client).await?;

        let files_dir = crate::utils::files::data_files_dir()?;

        let mut hash_files_to_upload = HashMap::new();

        //Per folder and file_type configured in toml, update them in vector
        for bundle in self.file_bundles()?.iter() {
            let src_dir = files_dir.join(&bundle.src_dir);

            if src_dir.is_dir() {
                let src_globs: Vec<&str> = bundle.src_globs.iter().map(AsRef::as_ref).collect();
                let files = list_files(&src_dir, Some(&src_globs), None)?;

                for file in files {
                    let name = file.file_name().unwrap().to_str().unwrap().to_string();
                    hash_files_to_upload.insert(
                        name.clone(),
                        FileInfo {
                            file_name: name,
                            id: None,
                            path: Some(file.to_path_buf()),
                        },
                    );
                }

                let files_to_delete =
                    unique_to_first_hash(&hash_files_client, &hash_files_to_upload)?;

                self.delete_files_client(files_to_delete).await?;

                let files_to_upload =
                    unique_to_first_hash(&hash_files_to_upload, &hash_files_client)?;

                let files_uploaded = self.upload_files_client(files_to_upload).await?;

                let files_not_deleted = hash_files_client
                    .clone()
                    .into_iter()
                    .filter(|f| hash_files_to_upload.contains_key(&f.0))
                    .map(|f| f.1)
                    .collect::<Vec<FileInfo>>();
                files_on_client.extend(files_not_deleted);
                files_on_client.extend(files_uploaded);
            }
        }
        Ok(files_on_client)
    }
}

//Private functions
impl AI {
    async fn query_files_on_client(
        &self,
        open_ai_client: &Client<OpenAIConfig>,
    ) -> Result<HashMap<String, FileInfo>> {
        let client_files = open_ai_client.files();
        let files_on_client = client_files.list(&[("limit", "100")]).await?.data;
        let hash_files_client: HashMap<String, FileInfo> = files_on_client
            .into_iter()
            .map(|f| {
                (
                    f.filename.clone(),
                    FileInfo {
                        file_name: f.filename,
                        id: Some(f.id),
                        path: None,
                    },
                )
            })
            .collect();
        Ok(hash_files_client)
    }

    async fn upload_files_client(&self, files_to_upload: Vec<FileInfo>) -> Result<Vec<FileInfo>> {
        let mut files_uploaded = Vec::new();
        for file in files_to_upload {
            println!("Uploading file {}", file.file_name);
            let uploaded_file = self
                .client
                .files()
                .create(CreateFileRequest {
                    file: file.clone().path.unwrap().into(),
                    purpose: FilePurpose::Assistants,
                })
                .await?;
            println!("Uploaded file {}", file.file_name);

            files_uploaded.push(FileInfo {
                file_name: file.file_name,
                id: Some(uploaded_file.id),
                path: file.path,
            })
        }
        Ok(files_uploaded)
    }

    async fn delete_files_client(&self, files_to_delete: Vec<FileInfo>) -> Result<()> {
        for file in files_to_delete {
            println!("Deleting file: {}", &file.file_name);
            self.client.files().delete(&file.id.unwrap()).await?;
            println!("File deleted");
        }
        Ok(())
    }
}
pub fn create_client(secret_key: &str) -> Result<Client<OpenAIConfig>> {
    Ok(Client::with_config(
        OpenAIConfig::new().with_api_key(secret_key),
    ))
}

fn unique_to_first_hash(
    hash1: &HashMap<String, FileInfo>,
    hash2: &HashMap<String, FileInfo>,
) -> Result<Vec<FileInfo>> {
    Ok(hash1
        .clone()
        .into_iter()
        .filter(|f| !hash2.contains_key(&f.0))
        .map(|f| f.1)
        .collect())
}
