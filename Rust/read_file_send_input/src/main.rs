use enigo::{Enigo, Keyboard, Settings};
use std::fs::File;
use std::io::{self, BufRead};
use std::process::{Command, Stdio};
use std::thread::sleep;
use std::time::Duration;
use winapi::shared::minwindef::{BOOL, LPARAM};
use winapi::shared::windef::HWND;
use winapi::um::winuser::{EnumWindows, GetWindowTextA, GetWindowTextLengthA, IsWindowVisible};
use winapi::um::winuser::{FindWindowA, SetForegroundWindow};

fn main() -> io::Result<()> {
    let characters_path: String = obtain_txt_path();
    println!("characters_filename: {}", characters_path);

    let exe_path = std::env::current_exe()?;
    let exe_dir = exe_path.parent().unwrap();

    // Define the path to the .txt file in the same directory as the executable
    let txt_file_path = exe_dir.join(characters_path);

    // Open the file in read-only mode
    let file = File::open(txt_file_path)?;
    let reader = io::BufReader::new(file);

    // Initialize variables
    let lines = reader.lines();
    let mut exe_path = String::new();
    let mut characters_log_in = Vec::new();
    let mut characters_screen = Vec::new();
    let mut quantity_characters = 0;

    // Process each line
    for line in lines {
        let line = line?;
        if line.starts_with("//") || line.is_empty() {
            continue;
        }
        if quantity_characters == 0 {
            exe_path = line;
        } else if line.ends_with(";character_screen") {
            let character_line_part: Vec<String> = line
                .split(";character_screen")
                .map(|s| s.to_string())
                .collect();
            characters_screen.push(character_line_part[0].clone());
        } else {
            characters_log_in.push(line);
        }

        quantity_characters += 1;
    }
    quantity_characters -= 1;

    println!("Characters to login: {}", quantity_characters);
    // Open all the .exe file
    for _ in 0..quantity_characters {
        sleep(Duration::from_millis(50));
        Command::new(&exe_path)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()?;
    }

    sleep(Duration::from_millis(1500));
    let mut opened_clients = 0;

    for line in characters_log_in.iter() {
        open_character_in_launcher(line);
        opened_clients += 1;
        if opened_clients == 5 {
            cycle_through_clients(true);
            opened_clients = 0;
        }
    }
    cycle_through_clients(true);

    println!("\nPersonagens para ficar na screen character");
    for line in characters_screen.iter() {
        open_character_in_launcher(line);
    }
    cycle_through_clients(false);

    Ok(())
}

fn obtain_txt_path() -> String {
    let mut input = String::new();

    // Prompt the user for input
    println!("Coloque o nome do txt a ser lido (não precisa do .txt)\nSe der enter, o default será 'characters'.");
    // Read the input from the user
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    input = input.split("\r\n").collect();
    if input.is_empty() {
        input = String::from("default_characters.txt");
    } else {
        input += ".txt"
    }
    input
}

fn bring_to_front(app_name: &str) {
    // Wait for the .exe to start and bring the window to the front
    let window_name = std::ffi::CString::new(app_name).unwrap();
    let mut hwnd = std::ptr::null_mut();
    for _ in 0..20 {
        // Try for up to 20 times (2 seconds)
        unsafe {
            hwnd = FindWindowA(std::ptr::null(), window_name.as_ptr());
        }
        if !hwnd.is_null() {
            break;
        }
        sleep(Duration::from_millis(100));
    }
    assert!(
        !hwnd.is_null(),
        "Tried to bring {} to front, but no window found",
        app_name
    );

    unsafe {
        SetForegroundWindow(hwnd);
    }
}

fn send_inputs(input: &str) {
    let mut enigo =
        Enigo::new(&Settings::default()).expect("Error creating enigo to be able to send inputs");

    //check for guest
    if input.starts_with("Guest:") {
        let input_splitted: Vec<&str> = input.split(";").collect();
        let account = input_splitted[0]
            .get(7..)
            .expect("Error slicing guest line");
        let password = input_splitted[1]
            .get(11..)
            .expect("Error slicing guest line");

        let _ = enigo.key(enigo::Key::Control, enigo::Direction::Press);
        let _ = enigo.key(enigo::Key::Unicode('f'), enigo::Direction::Click);
        let _ = enigo.key(enigo::Key::Control, enigo::Direction::Release);
        sleep(Duration::from_millis(200));

        let _ = enigo.key(enigo::Key::Shift, enigo::Direction::Press);
        let _ = enigo.key(enigo::Key::Tab, enigo::Direction::Click);
        let _ = enigo.key(enigo::Key::Shift, enigo::Direction::Release);
        sleep(Duration::from_millis(200));

        let _ = enigo.key(enigo::Key::RightArrow, enigo::Direction::Click);
        sleep(Duration::from_millis(200));
        let _ = enigo.key(enigo::Key::RightArrow, enigo::Direction::Click);
        sleep(Duration::from_millis(200));
        let _ = enigo.key(enigo::Key::Tab, enigo::Direction::Click);
        sleep(Duration::from_millis(200));

        let _ = enigo.text(account);
        let _ = enigo.key(enigo::Key::Tab, enigo::Direction::Click);
        sleep(Duration::from_millis(200));
        let _ = enigo.text(password);

        let _ = enigo.key(enigo::Key::Return, enigo::Direction::Click);
    } else {
        let _ = enigo.key(enigo::Key::Control, enigo::Direction::Press);
        let _ = enigo.key(enigo::Key::Unicode('f'), enigo::Direction::Click);
        let _ = enigo.key(enigo::Key::Control, enigo::Direction::Release);
        sleep(Duration::from_millis(200));

        let _ = enigo.text(input);

        sleep(Duration::from_millis(100));
        let _ = enigo.key(enigo::Key::Return, enigo::Direction::Click);
        let _ = enigo.key(enigo::Key::Return, enigo::Direction::Click);
    }
}

struct WindowSearch {
    title_start: String,
    hwnds: Vec<HWND>,
}

unsafe extern "system" fn enum_windows_proc(hwnd: HWND, lparam: LPARAM) -> BOOL {
    let search = &mut *(lparam as *mut WindowSearch);

    if IsWindowVisible(hwnd) == 0 {
        return 1; // Continue enumeration
    }

    let title_length = GetWindowTextLengthA(hwnd);
    if title_length == 0 {
        return 1; // Continue enumeration
    }

    let mut title: Vec<u8> = vec![0; (title_length + 1) as usize];
    GetWindowTextA(hwnd, title.as_mut_ptr() as *mut i8, title_length + 1);

    let title = String::from_utf8_lossy(&title);
    if title.starts_with(&search.title_start) {
        search.hwnds.push(hwnd);
    }

    1 // Continue enumeration
}

fn obtain_windows_by_title_start(title_start: &str) -> Vec<HWND> {
    sleep(Duration::from_millis(1000));
    let mut search = WindowSearch {
        title_start: title_start.to_string(),
        hwnds: Vec::new(),
    };

    unsafe {
        EnumWindows(Some(enum_windows_proc), &mut search as *mut _ as LPARAM);
    }

    assert!(
        !search.hwnds.is_empty(),
        "No window with the name '{}' found",
        title_start
    );

    search.hwnds
}
fn open_character_in_launcher(line: &str) {
    let mut keyboard =
        Enigo::new(&Settings::default()).expect("Error creating enigo to be able to send inputs");
    sleep(Duration::from_millis(3500));
    bring_to_front("Arcadia Launcher");
    let _ = keyboard.key(enigo::Key::Return, enigo::Direction::Click);

    println!("Character: {}", line);
    sleep(Duration::from_millis(3000));
    send_inputs(line);
    sleep(Duration::from_millis(300));
}

fn cycle_through_clients(login: bool) {
    let mut keyboard =
        Enigo::new(&Settings::default()).expect("Error creating enigo to be able to send inputs");

    sleep(Duration::from_millis(2000));
    let windows = obtain_windows_by_title_start("Arcadia Client");
    println!("number of windows: {}", windows.len());

    for window in windows.iter() {
        sleep(Duration::from_millis(100));
        unsafe {
            SetForegroundWindow(*window);
        }
        sleep(Duration::from_millis(100));
        let _ = keyboard.key(enigo::Key::Return, enigo::Direction::Click);
        sleep(Duration::from_millis(100));
        let _ = keyboard.key(enigo::Key::Return, enigo::Direction::Click);
    }
    if login {
        println!("Logar esses personagens");
        sleep(Duration::from_millis(2500));
        for window in windows.iter() {
            sleep(Duration::from_millis(100));
            unsafe {
                SetForegroundWindow(*window);
            }
            sleep(Duration::from_millis(100));
            let _ = keyboard.key(enigo::Key::Return, enigo::Direction::Click);
        }
    }
}
