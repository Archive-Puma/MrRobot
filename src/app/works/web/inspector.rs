use crate::{composer::steps, create_work, debug, regex, works::web::request, Value, Variable, Variables, Yaml};

create_work!(inspector; data, variables => {
    let url: String = steps::get_param("url", data, variables)?;

    debug!("inspector in: {}", url);

    let real_url: String = absolut_url(&url);
    let root: String = inspect(&url,data,variables)?;
    let refs: String = get_js_and_css(&real_url,&root,data,variables)?;

    let response: String = [root,refs].join("\n");

    Ok(Variable::Text(response))
});

fn get_js_and_css(url: &str, html: &str, data: &Yaml, variables: &Variables) -> Value<String> {
    let mut links: Vec<String> = regex!(all; html,
            r#"(<script.* src="([^"]+)".*>|<link.* href="([^"]+)".*>)"#).split("\n")
        .map(|tag| regex!(one; tag,r#"(?:href|src)="([^(http)][^"]+)"#).unwrap_or(String::new())).collect();
    links.retain(|link| !link.is_empty());
    
    let mut refs: String = String::new();

    for link in links {
        let uri: &str = &[url,&link].join("/");
        debug!("(refs) inspector in: {}", uri);
        let body: String = inspect(uri,data,variables)?;
        refs = [refs, body].join("\n");
    }

    Ok(refs)
}

fn inspect(link: &str, data: &Yaml, variables: &Variables) -> Value<String> {
    let current_data: Yaml = steps::change_attribute(data, "url", link);
    let request: Variable = request(&current_data, variables)?;

    Ok(request.to_string())
}

fn absolut_url(url: &str) -> String {
    let last_dot:   usize = url.rfind('.').unwrap_or_default();
    let last_slash: usize = url.rfind('/').unwrap_or_default();
    if last_dot > last_slash {
        let absoult: Vec<&str> = url.rsplitn(2, "/").collect();
        absoult.last().unwrap().to_string()
    } else { url.to_string() }
}