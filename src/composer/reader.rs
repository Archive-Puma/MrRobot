// standard imports
use std::fs;
use std::path::Path;
// internal crates (error handler)
use crate::environment::mrerror::{throw,Result,MrError};
// external crates (yaml serializer/deserializer)
extern crate yaml_rust;
use yaml_rust::YamlLoader;
pub use yaml_rust::Yaml;

fn check_extension
(filename: &str) -> Result<()>
{
	let path: &Path = Path::new(filename);
	match path.extension()
	{
		None => throw(MrError::ComposerNoExtension),
		Some(data) => {
			let extension: &str = data.to_str().unwrap();
			if extension == "yml" || extension == "yaml" { Ok(()) }
			else { throw(MrError::ComposerWrongExtension) }
		}
	}
}

fn get_contents
(filename: &str) -> Result<String>
{
	match fs::read_to_string(filename)
	{
		Ok(content) => Ok(content),
		Err(_)      => throw(MrError::ComposerNotFound)
	}
}

fn to_yaml
(contents: &String) -> Result<Yaml>
{
	match YamlLoader::load_from_str(contents.as_str())
	{
		Ok(data) => Ok(data[0].clone()),
		Err(_)   => throw(MrError::ComposerWrongYamlFormat)
	}
}

pub fn read
(filename: &str) -> Result<Yaml>
{
	check_extension(filename)?;
	let body: String = get_contents(filename)?;
	let data: Yaml = to_yaml(&body)?;

	Ok(data)
}

/* Documentation
	- https://docs.rs/yaml-rust/0.3.5/yaml_rust/
*/