use crate::{get,create_work};
use crate::composer::{get_param, Variables, Yaml};
use crate::environment::{throw, MrError, Result};

use reqwest::Response;

create_work!(data, variables => {
    let url: String = get_param("url", data, variables)?;
    let mut response: Response = get_response(&url)?;
    get_body(&mut response)
});

fn get_response(url: &str) -> Result<Response> {
    Ok(get!(reqwest::get(url), MrError::Unimplemented))
}

fn get_body(response: &mut Response) -> Result<String> {
    Ok(get!(response.text(), MrError::Unimplemented))
}
