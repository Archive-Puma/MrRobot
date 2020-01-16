use crate::{composer::steps, create_work, debug, Variable};

create_work!(string; data, variables => {
    let mut string: String = steps::get_param("string", data, variables)?;
    let conversion: String = steps::get_param("convert", data, variables)?;

    debug!("string ({}) to {}", &string, &conversion);

    for step in conversion.split(",") {
        match step.trim().to_ascii_lowercase().as_ref() {
            "uppercase" => { string = string.to_ascii_uppercase(); },
            "lowercase" => { string = string.to_ascii_lowercase(); },
            "reverse"   => { string = string.chars().rev().collect(); }
            _ => { }
        }
    }

    Ok(Variable::Text(string))
});