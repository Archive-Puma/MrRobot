use std::collections::HashMap;

pub type Variables = HashMap<String,String>;

pub enum Variable {
    Text(String)
}

impl Variable {
    pub fn to_string(&self) -> String {
        match self {
            Variable::Text(value) => value.to_string()
        }
    }
}