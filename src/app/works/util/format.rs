use crate::{composer::steps, create_work, debug, Variable};

create_work!(format; data, variables => {
    let text: String = steps::get_param("text", data, variables)?;
    let vars_str: String = steps::get_param("variables", data, variables)?;
    
    let splitted: Vec<&str> = text.split("^v^").collect();
    let mut vars: Vec<String> = vars_str.split(",").into_iter().map(|element|  {
        let var: &str = element.trim();
        match variables.contains_key(var) {
            true  => variables.get(var).unwrap().to_string(),
            false => String::new()
        }
    }).collect();

    let result: String = splitted.into_iter().map(|element| match vars.len() > 0 {
        false => element.to_string(),
        true => [element.to_string(),vars.pop().unwrap()].join("")
    }).fold(String::new(), |buffer,chunk| [buffer,chunk].join(""));

    debug!("format ({}) ({}): {}", text, vars_str, result);

    Ok(Variable::Text(result))
});