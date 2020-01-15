use crate::{composer::steps, create_work, debug, Exception, regex, works::web::request, works::web::inspector, Variable, Variables, Value, Yaml};

create_work!(robots; data, variables => {
    let url: String = steps::get_param("url", data, variables)?;
    debug!("searching robots.txt: {}", url);

    let robots: String = get_robots(&url,data,variables)?;

    let maybe_filter: Value<String> = steps::get_param("filter", data, variables);
    let maybe_filter_and_inspect: Value<String> = steps::get_param("filter and inspect", data, variables);

    if let Ok(filter) = maybe_filter { Ok(filter_robots(&robots, &filter)) }
    else if let Ok(filter) = maybe_filter_and_inspect {
        let filtered: Variable = filter_robots(&robots, &filter);
        let result: String = filtered.to_vec().iter().map(|link| {
            let new_url: String = format!("{}{}", &url, &link);
            let robot: Yaml = steps::change_attribute(data, "url", &new_url);
            inspector(&robot,variables).unwrap_or(Variable::Text(String::new())).to_string()
        }).filter(|result| !result.is_empty()).fold(String::new(), |result,element| [result,element.to_string()].join("\n"));
        Ok(Variable::Text(result))
    } else { Ok(Variable::Text(robots)) }
});

fn get_robots(url: &str, data: &Yaml, variables: &Variables) -> Value<String> {
    let new_url: String = format!("{}/robots.txt", url);
    let current_data: Yaml = steps::change_attribute(data, "url", &new_url);
    let robots: Value<Variable> = request(&current_data, variables);

    match robots {
        Ok(value) => Ok(value.to_string()),
        Err(Exception::NoInternetConnection) => Ok("There are not robots.txt".to_string()),
        Err(other_error) => Err(other_error)
    }
}

fn filter_robots(robots: &str, filter: &str) -> Variable {
    let regex_query: String = format!("{}: (.*)", filter);
    let filtered_robots: Vec<String> = robots.lines()
        .map(|line| regex!(one; line, &regex_query).unwrap_or(String::new()))
        .filter(|robot| !robot.is_empty()).collect();
    Variable::MultipleText(filtered_robots)
}