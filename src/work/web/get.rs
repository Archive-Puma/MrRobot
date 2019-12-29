use crate::get;
use crate::composer::{get_param,Yaml,Variables};
use crate::environment::{throw,MrError,Result};

extern crate reqwest;
use reqwest::{Response};

pub fn body(data: &Yaml, variables: &Variables) -> Result<String> {
    let url: String = get_param("url", data, variables)?;
    let mut response: Response = get_response(&url)?;
    get_body(&mut response)
}

fn get_response(url: &str) -> Result<Response> {
    Ok(get!(reqwest::get(url), MrError::_Unimplemented))
}

fn get_body(response: &mut Response) -> Result<String> {
    Ok(get!(response.text(), MrError::_Unimplemented))
}