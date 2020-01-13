use crate::{debug, get, info, raise, Value, Variable};

use yaml_rust::YamlLoader;
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
    use crate::{Colorize, regex, Report, Variables, works::*};

    pub fn run(data: &Yaml) -> Value<Report> {
        let mut report: Report = Report::new("stdout");
        let steps: &Vec<Yaml> = get_steps(data)?;
        let mut variables: Variables = Variables::new();
        
        println!("{}", "[*] Starting the process...".bold().green());

        for(_, step) in steps.iter().enumerate() {
            let (name, output): (String, Option<String>) = split_run(&step)?;
            info!("Work: {}", &name);

            let mut result: Variable = run_step(&name, step, &variables)?;
            match output {
                None => { report.append(result.to_string()); }
                Some(mut variable) => {
                    if let Some(concat) = regex!(one; &variable, r">([^>]\S+)") {
                        debug!("concat in: {}", concat);
                        let var: Option<&Variable> = variables.get(&concat);
                        let old_value: &Variable = get!(option; var => StepWrongVariable, concat.to_string())?;
                        variable = concat;
                        result = old_value.concat(result);
                    } else { debug!("stored in: {}", variable); }

                    variables.insert(variable.to_string(), result);
                }
            }
        }

        Ok(report)
    }

    fn get_steps(data: &Yaml) -> Value<&Vec<Yaml>> {
        get!(option; data["steps"].as_vec() => ComposerNoSteps)
    }

    pub fn get_param(name: &str, data: &Yaml, variables: &Variables) -> Value<String> {
        let mut value: String = get!(option; data[name].as_str() => StepNoParam,name)?
            .to_string();
        if let Some(variable) = get_variable(&value) {
            value = match variables.contains_key(&variable) {
                true  => Ok(variables.get(&variable).unwrap().to_string()),
                false => raise!(StepWrongVariable => variable)
            }?;
        }

        Ok(value)
    }

    fn get_variable(name: &str) -> Option<String> {
        regex!(one; name, r"^\$\{\{([^\}]+)\}\}$")
    }

    fn split_run(step: &Yaml) -> Value<(String, Option<String>)> {
        let run: String = get!(option; step["run"].as_str() => StepNoRunAttribute)?.to_string();
        let splitted: Vec<&str> = run.splitn(2, ">")
            .map(|segment| segment.trim()).collect();

        let output: Option<String> = match splitted.len() {
            1 => Ok(None),
            2 => Ok(Some(splitted[1].to_string())),
            _ => raise!(StepWrongRunAttribute)
        }?;

        Ok((splitted[0].to_string(), output))
    }

    fn run_step(name: &str, data: &Yaml, variables: &Variables) -> Value<Variable> {
        println!("{} {} {}", "[*]".bold().blue(), "Running".blue(), name.bold().blue());
        match name {
            "src/comments"    => src::comments(data,variables),
            "util/regex"      => util::regex(data,variables),
            "web/get_request" => web::get_request(data,variables),
            _ => raise!(StepWrongWorkName => name)
        }
    }
}

/* Documentation
    - https://docs.rs/yaml-rust/0.3.5/yaml_rust/
*/