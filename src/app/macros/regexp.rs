#[macro_export]
macro_rules! regex {
    (one; $text:expr, $regex:expr) => {
        match regex::Regex::new($regex).unwrap().captures($text) {
            None => None,
            Some(captures) => Some(captures[1].trim().to_string())
        }
    };
    (all; $text:expr, $regex:expr) => {
        regex::Regex::new($regex).unwrap()
            .captures_iter($text)
            .fold(String::new(), |result, capture| [result, capture[0].to_string()].join("\n"))
            .trim().to_string()
    };
}

