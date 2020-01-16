#[macro_export]
macro_rules! raise {
    ($exception:ident) => {
        Err(crate::Exception::$exception)
    };
    ($exception:ident => $name:expr) => {
        Err(crate::Exception::$exception($name.to_string()))
    };
    ($exception:ident => $one:expr,$two:expr) => {
        Err(crate::Exception::$exception($one.to_string(),$two.to_string()))
    };
}

#[macro_export]
macro_rules! get {
    (result; $expr:expr => $exception:ident) => {
        match $expr {
            Ok(value) => Ok(value),
            Err(_) => crate::raise!($exception)
        }
    };
    (option; $expr:expr => $exception:ident) => {
        match $expr {
            Some(value) => Ok(value),
            None => crate::raise!($exception)
        }
    };
    (option; $expr:expr => $exception:ident, $name:expr) => {
        match $expr {
            Some(value) => Ok(value),
            None => crate::raise!($exception => $name)
        }
    };
}