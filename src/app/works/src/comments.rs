use crate::{composer::steps, create_work, regex};

create_work!(comments; data, variables => {
    let src: String = steps::get_param("src", data, variables)?;
    let language_param: String = steps::get_param("language", data, variables)?;
    let languages: Vec<&str> = language_param.split(",").map(|lang| lang.trim()).collect();
    let mut result: String = String::new();
    for language in languages {
        let (re_line, re_multiline): (&str,&str) = match language.as_ref() {
            "html"               => (r"",r"<!--[\s\S]*?-->"),
            "css" |
            "js"  | "javascript" => (r"//[\s\S]*?$",r"/\*[\s\S]*?\*/"),
            _ => (r"",r"")
        };
        let line: String = regex!(all; &src, re_line);
        let multiline: String = regex!(all; &src, re_multiline);
        result = [result,line,multiline].join("\n").trim().to_string();
    }
    Ok(result)
});