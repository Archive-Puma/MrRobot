use crate::{composer::steps, create_work, debug, regex, Variable};

use regex::{Regex,RegexBuilder};

create_work!(regex; data, variables => {
    let text: String = steps::get_param("text", data, variables)?;
    debug!("text: {}", text);

    let pattern: String = steps::get_param("pattern", data, variables)?;
    let regex_pattern: Regex = RegexBuilder::new(&pattern)
        .build().unwrap();
    debug!("pattern: {}", regex_pattern);

    let result: String = regex!(all; &text, &pattern);
    Ok(Variable::Text(result))
});