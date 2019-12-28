use crate::composer::Yaml;
use crate::environment::{throw,MrError,Result};

use crate::work::web;

pub fn get_steps(data: &Yaml) -> Result<&Vec<Yaml>> {
    match &data["steps"].as_vec() {
        None => throw(MrError::_Unimplemented),
        Some(steps) => Ok(*steps)
    }
}

pub fn run_steps(steps: &[Yaml]) -> Result<()> {
    for(_index,step) in steps.iter().enumerate() {
        let name: String = get_step_name(step)?;
        let _work = run_by_stepname(&name,step)?;
    }
    Ok(())
}

fn get_step_name(step: &Yaml) -> Result<String> {
    match step["run"].as_str() {
        None => throw(MrError::_Unimplemented),
        Some(name) => Ok(name.to_string())
    }
}

fn run_by_stepname(name: &str, data: &Yaml) -> Result<String> {
    Ok(match name {
        "get_request"   => Ok(web::get::body(data)?),
        "html_comments" => Ok(String::new()),
        _ => throw(MrError::_Unimplemented)
    }?)
}