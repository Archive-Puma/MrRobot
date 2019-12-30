use regex::Regex;

pub fn get_variable_name(text: &str) -> Option<String> {
    let re: Regex = Regex::new(r"^\$\{\{([^\}]+)\}\}$").unwrap();
    match re.captures(text) {
        None => None,
        Some(captures) => Some(captures[1].trim().to_string())
    }
}
