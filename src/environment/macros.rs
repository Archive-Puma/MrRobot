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