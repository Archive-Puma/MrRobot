use crate::{composer::steps, create_work, debug, regex, works::web::get_request, Value, Variable, Variables, Yaml};

use yaml_rust::YamlLoader;

// TODO: get_js_and_css and inspect should get YAML param modifying url to use headers

create_work!(inspector; data, variables => {
    let url: String = steps::get_param("url", data, variables)?;
    debug!("inspector in: {}", url);

    let root: String = inspect(&url,variables)?;
    let refs: String = get_js_and_css(&url,&root,variables)?;

    let response: String = [root,refs].join("\n");

    Ok(Variable::Text(response))
});

fn get_js_and_css(url: &str, html: &str, variables: &Variables) -> Value<String> {
    let mut links: Vec<String> = regex!(all; html,
            r#"(<script.* src="([^"]+)".*>|<link.* href="([^"]+)".*>)"#).split("\n")
        .map(|tag| match regex!(one; tag,r#"(?:href|src)="([^(http)][^"]+)"#) {
            None => "".to_string(),
            Some(link) => link.to_string()
        }).collect();
    links.retain(|link| !link.is_empty());
    
    let mut refs: String = String::new();

    for link in links {
        let uri: &str = &[url,&link].join("/");
        debug!("(refs) inspector in: {}", uri);
        let body: String = inspect(uri,variables)?;
        refs = [refs, body].join("\n");
    }

    Ok(refs)
}

fn inspect(link: &str, variables: &Variables) -> Value<String> {
    let current_data: Yaml = YamlLoader::load_from_str(&format!("url: {}", link))
        .unwrap().first().unwrap().clone();
    let request: Variable = get_request(&current_data, variables)?;

    Ok(request.to_string())
}