use crate::get;
use crate::composer::Yaml;
use crate::environment::{throw,MrError,Result};

extern crate reqwest;
use reqwest::{Response};

pub fn body(_data: &Yaml) -> Result<String> {
    let mut response: Response = get_response("https://fsundays.tech")?;
    get_body(&mut response)
}

fn get_response(url: &str) -> Result<Response> {
    Ok(get!(reqwest::get(url), MrError::_Unimplemented))
}

fn get_body(response: &mut Response) -> Result<String> {
    Ok(get!(response.text(), MrError::_Unimplemented))
}