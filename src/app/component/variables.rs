use std::collections::HashMap;

pub type Variables = HashMap<String,Variable>;

pub enum Variable {
    Text(String),
    MultipleText(Vec<String>)
}

impl Variable {
    pub fn concat(&self, other: Variable) -> Variable {
        match self {
            Variable::Text(value) => Variable::Text([value.to_string(),other.to_string()].join("\n")),
            Variable::MultipleText(vector) => {
                match other {
                    Variable::MultipleText(other_vector) => Variable::MultipleText([&vector[..], &other_vector[..]].concat()),
                    _ => panic!("ERROR AL CONCATENAR UN VECTOR CON ALGO QUE NO ES UN VECTOR")
                }
            }
        }
    }
    
    pub fn to_string(&self) -> String {
        match self {
            Variable::Text(value) => value.to_string(),
            Variable::MultipleText(vector) => vector.iter().fold(String::new(), |result, element| [result,element.to_string()].join("\n"))
        }
    }

    pub fn to_vec(&self) -> Vec<String> {
        match self {
            Variable::Text(value) => vec![value.to_string()],
            Variable::MultipleText(vector) => vector.to_vec()
        }
    }
}