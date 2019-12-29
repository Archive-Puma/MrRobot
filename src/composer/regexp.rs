extern crate regex;
use regex::Regex;

pub fn get_variable_name(text: &str) -> Option<String> {
    let re: Regex = Regex::new(r"^\{\{([^\}])\}\}$").unwrap();
    if re.is_match(text) {
        let input: &str = re.captures(text).unwrap().get(0).unwrap().as_str().trim();
        Some(input.to_string())
    } else { None }
}