use std::collections::HashMap;

use crate::get;
use crate::composer::{get_variable_name,Yaml};
use crate::environment::{throw,MrError,Result};

use crate::work::web;

pub type Variables = HashMap<String,String>;

pub fn get_steps(data: &Yaml) -> Result<&Vec<Yaml>> {
    Ok(*get!(&data["steps"].as_vec() => MrError::_Unimplemented))
}

pub fn get_param(name: &str, data: &Yaml, variables: &Variables) -> Result<String> {
    let mut value: &str = get!(&data[name].as_str() => match name {
        _ => MrError::_Unimplemented
    });

    if let Some(input) = get_variable_name(value) {
        if variables.contains_key(&input) { value = variables.get(&input).unwrap(); }
        else { throw(MrError::_Unimplemented)?; }
    }

    println!("{:?}", value);

    Ok(String::from(value))
}

pub fn run_steps(steps: &[Yaml]) -> Result<()> {
    let mut variables: Variables = Variables::new();
    for(_index,step) in steps.iter().enumerate() {
        let name: String = get_step_name(step)?;
        let result = run_by_stepname(&name,step,&variables)?;

        if let Some(out) = &step["out"].as_str() {
            variables.insert(out.to_string(), result);
        } else {
            println!("{:?}", result);
        }
    }
    Ok(())
}

fn get_step_name(step: &Yaml) -> Result<String> {
    Ok(get!(step["run"].as_str() => MrError::_Unimplemented).to_string())
}

fn run_by_stepname(name: &str, data: &Yaml, variables: &Variables) -> Result<String> {
    Ok(match name {
        "get_request"   => Ok(web::get::body(data,variables)?),
        "html_comments" => Ok(String::from("Hi")),
        _ => throw(MrError::_Unimplemented)
    }?)
}