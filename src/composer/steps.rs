use std::collections::HashMap;

use colored::*;
use std::fs::File;
use std::io::Write;

use crate::{get,run_work};
use crate::composer::{get_variable_name, Yaml};
use crate::environment::{throw, MrError, Result};

use crate::work::*;

pub type Variables = HashMap<String, String>;

pub fn get_steps(data: &Yaml) -> Result<&Vec<Yaml>> {
    Ok(*get!(&data["steps"].as_vec() => MrError::Unimplemented))
}

pub fn get_param(name: &str, data: &Yaml, variables: &Variables) -> Result<String> {
    let mut value: &str = get!(&data[name].as_str() => match name {
        _ => MrError::Unimplemented
    });
    
    if let Some(input) = get_variable_name(value) {
        if variables.contains_key(&input) {
            value = variables.get(&input).unwrap();
        } else {
            throw(MrError::_Unimplemented)?;
        }
    }

    Ok(String::from(value))
}

pub fn run_steps(steps: &[Yaml]) -> Result<()> {
    // Output
    let mut report: String = String::new();
    // Variables
    let mut variables: Variables = Variables::new();
    // Works
    for (_index, step) in steps.iter().enumerate() {
        let name: String = get_step_name(step)?;
        let result: String = run_by_stepname(name, step, &variables)?;
        
        if let Some(out) = &step["out"].as_str() {
            variables.insert(out.to_string(), String::from(&result));
        } else {
            report = [report,result].join("\n");
        }
    }
    // File
    let mut file: File = File::create("report.txt").unwrap();
    file.write_all(report.trim().as_bytes()).unwrap();

    Ok(())
}

fn get_step_name(step: &Yaml) -> Result<String> {
    Ok(get!(step["run"].as_str() => MrError::_Unimplemented).to_string())
}

fn run_by_stepname(name: String, data: &Yaml, variables: &Variables) -> Result<String> {
    println!("{} {} {}", "[*]".bold().blue(), "Running".blue(), &name.bold().blue());
    Ok(match name.as_ref() {
        "get_request"   => run_work!(web,get_request    => data,variables),
        "html_comments" => run_work!(web,html_comments  => data,variables),
        _ => throw(MrError::_Unimplemented),
    }?)
}
