use crate::composer::{get_param,get_all_matches,Variables,Yaml};
use crate::environment::{throw,MrError,Result};

pub fn html(data: &Yaml, variables: &Variables) -> Result<String> {
    let src: String = get_param("src", data, variables)?;
    if let Some(matches) = get_all_matches(&src, r"<!--([\s\S]*?)-->") {
        Ok(matches)
    } else { throw(MrError::_Unimplemented) }
}
