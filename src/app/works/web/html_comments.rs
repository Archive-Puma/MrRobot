use crate::{composer::steps, create_work, regex};

create_work!(html_comments; data, variables => {
    let src: String = steps::get_param("src", data, variables)?;
    let result: String = regex!(all; &src, r"<!--[\s\S]*?-->");
    Ok(result)
});