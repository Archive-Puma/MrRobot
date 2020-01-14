use crate::{composer::steps, create_work, debug, default, get, Value, Variable, Variables, warn, Yaml};

use reqwest::{blocking::Client,blocking::Response,header};

create_work!(get_request; data, variables => {
    let url: String = steps::get_param("url", data, variables)?;
    debug!("url: {}", url);

    let client: Client = Client::new();
    let response: Response = get!(result; client.get(&url).headers(set_headers(data, variables)).send() => NoInternetConnection)?;

    debug!("status code: {}", response.status());
    let result: String = get!(result; response.text() => ComposerEmpty)?;
    Ok(Variable::Text(result))
});

fn set_headers(data: &Yaml, variables: &Variables) -> header::HeaderMap {
    let mut headers: header::HeaderMap = header::HeaderMap::new();
    if let Some(useragent) = get_useragent(data, variables) {
        headers.insert(header::USER_AGENT, header::HeaderValue::from_str(&useragent).unwrap());
    } 

    headers
}

fn get_useragent(data: &Yaml, variables: &Variables) -> Option<String> {
    let mut maybe_useragent: Value<String> = steps::get_param("useragent", data, variables);
    if let Err(_) = maybe_useragent { maybe_useragent = steps::get_param("ua", data, variables); }
    match maybe_useragent {
        Ok(ua) => { debug!("user agent: {}", ua); Some(ua) }
        Err(_) => { warn!("Not User-Agent specified. Set to default: {}", default::USER_AGENT);
            Some(default::USER_AGENT.to_string()) }
    }
}