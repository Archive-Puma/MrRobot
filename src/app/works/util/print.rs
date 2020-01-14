use crate::{composer::steps, create_work, debug, get, Variable};

create_work!(print; data, variables => {
    let name: String = steps::get_param("variable", data, variables)?;

    let variable: &Variable = get!(option; variables.get(&name) => StepWrongVariable, name.to_string())?;
    let value: String = variable.to_string();

    debug!("printing variable: {}\n{}", name, value);

    Ok(Variable::Text(value))
});