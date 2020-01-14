use std::collections::HashMap;

pub type Variables = HashMap<String,Variable>;

pub enum Variable {
    Text(String)
}

impl Variable {
    pub fn concat(&self, other: Variable) -> Variable {
        match self {
            Variable::Text(value) => {
                let concated = [value.to_string(),other.to_string()].join("\n");
                Variable::Text(concated)
            }
        }
    }
    
    pub fn to_string(&self) -> String {
        match self {
            Variable::Text(value) => value.to_string()
        }
    }
}