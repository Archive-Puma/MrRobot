extern crate yaml_rust;
use crate::worker::work::{as_targettype,Work,Target,TargetType};
use yaml_rust::Yaml;

use crate::environment::mrerror::{throw,Result,MrError};

fn check_version
(version: i64) -> Result<()>
{
	if version == 1 { Ok(()) }
	else { throw(MrError::ComposerWrongVersion) }
}

fn get_target
(target: &Yaml) -> Result<Target>
{
	let kind_str: &str = match target["type"].as_str()
	{
		None        => throw(MrError::Unimplemented),
		Some(kind)  => Ok(kind)
	}?;
	let kind: TargetType = as_targettype(kind_str)?;
	let route: String = String::from(match target[kind_str].as_str()
	{
		None        => throw(MrError::Unimplemented),
		Some(route) => Ok(route)
	}?);

	Ok(Target{ kind: kind, route: route })
}

pub fn validate
(data: &Yaml) -> Result<()>
{
	// Check if the version is set and is a number
	match data["version"].as_i64()
	{
		None            => throw(MrError::ComposerNoVersion),
		Some(version)   => Ok(check_version(version)?)
	}?;
	// Check if there is a 'hack' key and is a vector
	let hack_key: &Vec<Yaml> = match data["hack"].as_vec()
	{
		None            => throw(MrError::Unimplemented),
		Some(objetives) => Ok(objetives)
	}?;

	// Iterate over the objetives getting the targets
	for (_index,hack_value) in hack_key.iter().enumerate()
	{
		// Check if the 'target' key exists
		let target_key: &Yaml = &hack_value["target"];
		if target_key.is_badvalue() { throw(MrError::Unimplemented)?; }

		// Parse the target type
		let work: Work = Work { target: get_target(target_key)? };

		println!("{:?}", work);
	}


	Ok(())
}