use std::{
    ffi::OsStr,
    fs::{read_to_string, File},
    io::{BufRead, BufReader, BufWriter, Write},
    path::{Path, PathBuf},
};

use color_eyre::eyre::eyre;
use globset::{Glob, GlobSet, GlobSetBuilder};
use walkdir::WalkDir;

use crate::Result;

pub fn bundle_to_file(files: Vec<PathBuf>, dst_file: &Path) -> Result<()> {
    let mut writer = BufWriter::new(File::create(dst_file)?);

    for file in files {
        if !file.is_file() {
            return Err(eyre!("Cannot bundle. {:?} is not a file.", file));
        }

        let reader = BufReader::new(File::open(&file)?);

        writeln!(writer, "\n// file path: {}\n", file.to_string_lossy())?;

        for line in reader.lines() {
            let line = line?;
            writeln!(writer, "{}", line)?;
        }
        writeln!(writer, "\n\n")?;
    }
    writer.flush()?;

    Ok(())
}

///Returns true if any folder was created
pub fn ensure_dir(dir: &Path) -> Result<bool> {
    if dir.is_dir() {
        Ok(false)
    } else {
        std::fs::create_dir_all(dir)?;
        Ok(true)
    }
}

pub fn list_files(
    dir: &Path,
    include_globs: Option<&[&str]>,
    exclude_globs: Option<&[&str]>,
) -> Result<Vec<PathBuf>> {
    let base_dir_exclude = base_dir_exclude_globs()?;

    let include_globs = include_globs.map(get_glob_set).transpose()?;
    let exclude_globs = exclude_globs.map(get_glob_set).transpose()?;

    let walk_dir_it = WalkDir::new(dir).into_iter().filter_entry(|e|
        //if dir, check the dir exclude
        if e.file_type().is_dir(){
            !base_dir_exclude.is_match(e.path())
        }
        // apply include and exclude globs
        else {
            if let Some(exclude_globs) = exclude_globs.as_ref() {
                if exclude_globs.is_match(e.path()){return false}
            }
            match include_globs.as_ref(){
                Some(globs) => globs.is_match(e.path()),
                None => true,
            }
        }
    ).filter_map(|e| e.ok().filter(|e| e.file_type().is_file()));

    let paths = walk_dir_it.map(|e| e.into_path());

    Ok(paths.collect())
}

fn base_dir_exclude_globs() -> Result<GlobSet> {
    get_glob_set(&[".git", "target"])
}

fn get_glob_set(globs: &[&str]) -> Result<GlobSet> {
    let mut builder = GlobSetBuilder::new();
    for glob in globs {
        builder.add(Glob::new(glob)?);
    }

    Ok(builder.build()?)
}

pub fn load_from_toml<T>(file: Option<&Path>, content: Option<&str>) -> Result<T>
where
    T: serde::de::DeserializeOwned,
{
    if let Some(content) = content {
        return Ok(toml::from_str(content)?);
    }
    if let Some(file) = file {
        let content = read_to_string(file)?;
        return Ok(toml::from_str(&content)?);
    }
    Err(eyre!("No file or content to read TOML"))
}

pub fn load_from_json<T>(file: impl AsRef<Path>) -> Result<T>
where
    T: serde::de::DeserializeOwned,
{
    let val = serde_json::from_reader(get_reader(file.as_ref())?)?;
    Ok(val)
}

pub fn save_to_json<T>(file: impl AsRef<Path>, data: &T) -> Result<()>
where
    T: serde::Serialize,
{
    let file = file.as_ref();
    let file = File::create(file).map_err(|e| eyre!("Cannote Create file {:?}: {}", file, e))?;

    serde_json::to_writer_pretty(file, data)?;

    Ok(())
}

fn get_reader(file: &Path) -> Result<BufReader<File>> {
    let Ok(file) = File::open(file) else {
        return Err(eyre!("File not found: {}", file.display()));
    };
    Ok(BufReader::new(file))
}

//Traits
pub trait AnyFile {
    fn to_str_mine(&self) -> &str;
}

impl AnyFile for Path {
    fn to_str_mine(&self) -> &str {
        self.file_name().and_then(OsStr::to_str).unwrap_or("")
    }
}

fn one_drive_folder() -> Result<PathBuf> {
    let data_dir = PathBuf::from(std::env::var("USERPROFILE")?)
        .join("OneDrive - QUEST INVESTIMENTOS LTDA")
        .join("Portfolio Overview");
    Ok(data_dir)
}
pub fn data_files_dir() -> Result<PathBuf> {
    let dir = one_drive_folder()?;
    ensure_dir(&dir)?;
    Ok(dir)
}

pub fn thread_path() -> Result<PathBuf> {
    let data_dir = PathBuf::from(std::env::var("USERPROFILE")?)
        .join("victor")
        .join(".thread");
    ensure_dir(&data_dir)?;
    let thread_path = data_dir.join("thread.json");
    Ok(thread_path)

}
