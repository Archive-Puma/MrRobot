#[macro_export]
macro_rules! get {
    ($input:expr) => {
        match $input {
            Ok(value) => Ok(value),
            _ => throw(MrError::_Unimplemented)
        }?
    };
    ($input:expr,$error:expr) => {
        match $input {
            Ok(value) => Ok(value),
            _ => throw($error)
        }?
    };
}