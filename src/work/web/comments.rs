use crate::composer::{get_param,Variables,Yaml};
use crate::environment::Result;

pub fn html(data: &Yaml, variables: &Variables) -> Result<String> {
    let url: String = get_param("src", data, variables)?;
    println!("{:?}", "Hi");
    Ok(String::new())
}
