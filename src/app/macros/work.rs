#[macro_export]
macro_rules! create_work {
    ($name:ident; $data:ident, $variables: ident => $code:block) => {
        pub fn $name($data: &crate::Yaml, $variables: &crate::Variables) -> crate::Value<String> {
            $code
        }
    };
}