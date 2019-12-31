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
    use crate::{regex,Colorize,Variables};

    pub fn run(data: &Yaml) -> Value<()> {
        let steps: &Vec<Yaml> = get_steps(data)?;
        let variables: Variables = Variables::new();
        
        println!("{}", "[*] Starting the process...".bold().green());

        for(_, step) in steps.iter().enumerate() {
            let name: String = get_name(&step)?;
            run_step(&name, step, &variables)?;
        }
        Ok(())
    }

    fn get_steps(data: &Yaml) -> Value<&Vec<Yaml>> {
        get!(option; data["steps"].as_vec() => ComposerNoSteps)
    }

    fn get_name(step: &Yaml) -> Value<String> {
        let name: String = get!(option; step["run"].as_str() => StepNoRunAttribute)?.to_string();
        Ok(name)
    }

    fn get_param(name: &str, data: &Yaml, variables: &Variables) -> Value<String> {
        let mut value: &str = get!(option; data[name].as_str() => StepNoParam,name)?;
        if let Some(variable) = get_variable(name) {
            value = match variables.contains_key(&variable) {
                true  => Ok(variables.get(&variable).unwrap()),
                false => raise!(StepWrongVariable => variable)
            }?;
        }

        Ok(value.to_string())
    }

    fn get_variable(name: &str) -> Option<String> {
        regex!(one; name, r"^\$\{\{([^\}]+)\}\}$")
    }

    fn run_step(name: &str, data: &Yaml, variables: &Variables) -> Value<String> {
        println!("{} {} {}", "[*]".bold().blue(), "Running".blue(), name.bold().blue());
        match name {
            "get_request" => get_param("url", data, variables),
            _ => raise!(StepWrongWorkName => name)
        }
    }
}

/* Documentation
    - https://docs.rs/yaml-rust/0.3.5/yaml_rust/
*/