use regex::Regex;

pub fn get_variable_name(text: &str) -> Option<String> {
    let re: Regex = Regex::new(r"^\$\{\{([^\}]+)\}\}$").unwrap();
    match re.captures(text) {
        None => None,
        Some(captures) => Some(captures[1].trim().to_string())
    }
}

pub fn get_all_matches(text: &str, pattern: &str) -> Option<String> {
    let re: Regex = Regex::new(pattern).unwrap();
    let mut result: String = String::new();
    for capture in re.captures_iter(text) {
        result = [result, String::from(&capture[0])].join("\n");
    }
    match result.len() {
        0 => None,
        _ => Some(result.trim_start().to_string())
    }
}
