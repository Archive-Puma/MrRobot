#[macro_export]
macro_rules! raise {
    ($exception:ident) => {
        Err(Exception::$exception)
    };
    ($exception:ident => $name:literal) => {
        Err(Exception::$exception($name.to_string()))
    };
}

#[macro_export]
macro_rules! get {
    (result; $expr:expr => $exception:ident) => {
        match $expr {
            Ok(value) => Ok(value),
            Err(_) => raise!($exception)
        }
    };
    (option; $expr:expr => $exception:ident) => {
        match $expr {
            Some(value) => Ok(value),
            None => raise!($exception)
        }
    };
}