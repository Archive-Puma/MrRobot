extern crate yaml_rust;
use yaml_rust::Yaml;

use crate::environment::mrerror::{throw,Result,MrError};

fn check_version
(version: i64) -> Result<()>
{
	if version == 1 { Ok(()) }
	else { throw(MrError::ComposerWrongVersion) }
}

pub fn validate
(data: &Yaml) -> Result<()>
{
	match data["version"].as_i64()
	{
		None          => throw(MrError::ComposerNoVersion),
		Some(version) => Ok(check_version(version)?)
	}
}