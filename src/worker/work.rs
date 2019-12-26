use crate::environment::mrerror::{throw,Result,MrError};

#[derive(Debug)]
pub struct Work
{
	pub target: Target
}

#[derive(Debug)]
pub struct Target
{
	pub kind:   TargetType,
	pub route:  String
}

#[derive(Debug)]
pub enum TargetType
{
	URL,
	DOMAIN,
	IPADDR,
	IPADDR6,
	FILE
}

pub fn as_targettype
(kind: &str) -> Result<TargetType>
{
	match kind
	{
		"domain" => Ok(TargetType::DOMAIN),
		"file"   => Ok(TargetType::FILE),
		"ip"     => Ok(TargetType::IPADDR),
		"ipv4"   => Ok(TargetType::IPADDR),
		"ipv6"   => Ok(TargetType::IPADDR6),
		"url"    => Ok(TargetType::URL),
		_        => throw(MrError::WorkWrongTarget)
	}
}

impl Target
{
	pub fn new
	(kind: TargetType, route: String) -> Target
	{
		Target {
			route: route,
			kind: kind
		}
	}
}