use crate::{get, raise, Exception, Value};

use yaml_rust::{YamlLoader};
pub use yaml_rust::Yaml;

use std::path::Path;
use std::fs::read_to_string;

pub fn get(filename: &str) -> Value<Yaml> {
    check_extension(filename)?;
    let content: String = read(filename)?;
    let data: Yaml = to_yaml(&content)?;
    check_version(&data)?;
    Ok(data)
}

fn check_extension(filename: &str) -> Value<bool> {
    let path: &Path = Path::new(filename);
    let extension: &str = get!(option; path.extension() => ComposerNoExtension)?
        .to_str().unwrap();
    match extension {
        "yml" | "yaml" => Ok(true),
        _ => raise!(ComposerWrongExtension)
    }    
}

fn read(filename: &str) -> Value<String> {
    get!(result; read_to_string(filename) => ComposerNotFound)
}

fn to_yaml(content: &str) -> Value<Yaml> {
    let documents: Vec<Yaml> = get!(result; YamlLoader::load_from_str(content) => ComposerWrongFormat)?;
    let document: Yaml = get!(option; documents.first() => ComposerEmpty)?.clone();
    Ok(document)
}

fn check_version(data: &Yaml) -> Value<i64> {
    match data["version"].as_i64() {
        Some(1) => Ok(1),
        Some(_) => raise!(ComposerWrongVersion),
        None    => raise!(ComposerNoVersion)
    }
}

pub mod steps {
    use super::*;

    pub fn get(data: &Yaml) -> Value<&Vec<Yaml>> {
        get!(option; data["steps"].as_vec() => ComposerNoSteps)
    }   
}

/* Documentation
    - https://docs.rs/yaml-rust/0.3.5/yaml_rust/
*/