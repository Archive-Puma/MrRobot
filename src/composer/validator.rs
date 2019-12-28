use crate::composer::{get_steps,Yaml};
use crate::environment::{throw,MrError,Result};

fn check_version(data: &Yaml) -> Result<()> {
	match data["version"].as_i64() {
		None => throw(MrError::ComposerNoVersion),
		Some(1) => Ok(()),
		Some(_) => throw(MrError::ComposerWrongVersion)
	}
}

pub fn validate(data: &Yaml) -> Result<()> {
	// Check the version
	check_version(data)?;
	// Check the steps
	if get_steps(data)?.is_empty() { throw(MrError::_Unimplemented)?; }

	Ok(())
}