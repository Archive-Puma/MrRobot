use crate::{composer::steps, create_work, debug, default, get, raise, Value, Variable, Variables, warn, Yaml};

use reqwest::{blocking::Client,blocking::Response,header};

create_work!(request; data, variables => {
    let url: String = steps::get_param("url", data, variables)?;
    
    let maybe_method: Value<String> = steps::get_param("method", data, variables);
    let method: String = match maybe_method {
        Ok(value) => match value.as_ref() {
            "POST" | "GET" => value,
            other => raise!(StepWrongMethod => other)?
        },
        Err(_) => "GET".to_string()
    };
    
    debug!("{} request: {}", method, url);

    let client: Client = Client::new();
    let request = match method.as_ref() {
        "GET" => client.get(&url),
        "POST" => client.post(&url),
        _ => unreachable!() 
    };

    let response: Response = get!(result; request.headers(set_headers(data, variables)).send() => NoInternetConnection)?;

    debug!("status code: {}", response.status());
    let result: String = get!(result; response.text() => ComposerEmpty)?;
    Ok(Variable::Text(result))
});

fn set_headers(data: &Yaml, variables: &Variables) -> header::HeaderMap {
    let mut headers: header::HeaderMap = header::HeaderMap::new();
    if let Some(useragent) = get_useragent(data, variables) {
        headers.insert(header::USER_AGENT, header::HeaderValue::from_str(&useragent).unwrap());
    }
    if let Some(cookies) = get_cookies(data, variables) {
        headers.insert(header::COOKIE, header::HeaderValue::from_str(&cookies).unwrap());
    }
    if let Some(auth_basic) = get_auth_basic(data, variables) {
        let auth: &str = &["Basic", &auth_basic].join(" ");
        headers.insert(header::AUTHORIZATION, header::HeaderValue::from_str(auth).unwrap());
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

fn get_cookies(data: &Yaml, variables: &Variables) -> Option<String> {
    let mut maybe_cookies: Value<String> = steps::get_param("cookies", data, variables);
    if let Err(_) = maybe_cookies { maybe_cookies = steps::get_param("cookie", data, variables); }
    match maybe_cookies {
        Ok(cookies) => { debug!("cookies: {}", cookies); Some(cookies) }
        Err(_) => None
    }
}

fn get_auth_basic(data: &Yaml, variables: &Variables) -> Option<String> {
    let maybe_basic: Value<String> = steps::get_param("basic", data, variables);
    match maybe_basic {
        Ok(basic) => {
            match basic.ends_with("=") {
                true => Some(basic),
                false => Some(base64::encode(&basic).to_string())
            }
        }
        Err(_) => None
    }
}
