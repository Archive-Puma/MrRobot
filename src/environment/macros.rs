#[macro_export]
macro_rules! get {
    ($input:expr, $error:expr) => {
        match $input {
            Ok(value) => Ok(value),
            Err(_) => throw($error),
        }?
    };
    ($input:expr => $error:expr) => {
        match $input {
            Some(value) => Ok(value),
            None => throw($error),
        }?
    };
}

#[macro_export]
macro_rules! create_work {
    ($data:ident, $variables: ident => $code:block) => {
        pub fn run($data: &Yaml, $variables: &Variables) -> Result<String> {
            $code
        }
    };
}

#[macro_export]
macro_rules! run_work {
    ($category:ident, $work:ident => $data: expr, $variables: expr) => {
        Ok($category::$work($data,$variables)?)
    };
}