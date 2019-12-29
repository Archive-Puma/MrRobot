use crate::get;
use crate::environment::{throw,Result,MrError};

use std::fs;
use std::path::Path;

extern crate yaml_rust;
use yaml_rust::YamlLoader;
pub use yaml_rust::Yaml;

fn check_extension (filename: &str) -> Result<()> {
	let path: &Path = Path::new(filename);
	let extension: &str = get!(path.extension() => MrError::ComposerNoExtension).to_str().unwrap();
	if extension != "yml" && extension != "yaml" { throw(MrError::ComposerWrongExtension)? }
	Ok(())
}

fn get_contents(filename: &str) -> Result<String> {
	Ok(get!(fs::read_to_string(filename), MrError::ComposerNotFound))
}

fn to_yaml(contents: &str) -> Result<Yaml> {
	let docs: Vec<Yaml> = get!(YamlLoader::load_from_str(contents), MrError::ComposerWrongYamlFormat);
	Ok(get!(docs.first() => MrError::ComposerEmpty).clone())
}

pub fn read(filename: &str) -> Result<Yaml> {
	check_extension(filename)?;
	let body: String = get_contents(filename)?;
	let data: Yaml = to_yaml(&body)?;

	Ok(data)
}

/* Documentation
	- https://docs.rs/yaml-rust/0.3.5/yaml_rust/
*/