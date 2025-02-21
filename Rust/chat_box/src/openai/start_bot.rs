use crate::openai::{client, thread, vector_store};
use crate::Result;

use super::client::AI;

pub async fn start() -> Result<AI> {
    let mut chat_bot = client::AI::new().await?;
    let client = chat_bot.client()?;

    let files_on_client = chat_bot.update_files_client().await?;

    let thread_id = thread::load_or_create(&chat_bot).await?;

    let chosen_files = files_on_client;
    if !chosen_files.is_empty() {
        let mut ids_chosen = Vec::new();
        for file in chosen_files {
            println!("{}", file.file_name);
            ids_chosen.push(file.id.expect("Id not found for file"));
        }
        vector_store::associate_files_vector(client, ids_chosen, chat_bot.vector_id()?).await?;
    }
    chat_bot.update_thread_id(thread_id);
    
    println!("Ask your question\n");
    //loop {
    //    let mut input = String::new();
    //    std::io::stdin()
    //        .read_line(&mut input)
    //        .expect("unable to read user input");
    //    let cmd = Cmd::from_input(&input);

    //    match cmd {
    //        Cmd::Quit => break,
    //        Cmd::Chat(msg) => {
    //            let res = thread::run_thread_msg(client, chat_bot.assistant_id()?, &thread_id, &msg).await?;
    //            //let res = wrap(&res, 80).join("\n");
    //            println!("{}", res);
    //        }
    //    }
    //}
    Ok(chat_bot)
}
