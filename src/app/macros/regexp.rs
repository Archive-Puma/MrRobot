#[macro_export]
macro_rules! regex {
    (one; $text:expr, $regex:expr) => {
        match regex::Regex::new($regex).unwrap().captures($text) {
            None => None,
            Some(captures) => Some(captures[1].trim().to_string())
        }
    };
}