use crate::composer::Yaml;
use crate::environment::{throw,MrError,Result};

extern crate reqwest;
use reqwest::Response;

pub fn run(_data: &Yaml) -> Result<()> {
    let mut response: Response = match reqwest::get("https://fsundays.tech") {
        Ok(response) => Ok(response),
        _ => throw(MrError::_Unimplemented)
    }?;

    let body: String = match response.text() {
        Ok(body) => Ok(body),
        _ => throw(MrError::_Unimplemented)
    }?;

    println!("{}", body);
    Ok(())
}