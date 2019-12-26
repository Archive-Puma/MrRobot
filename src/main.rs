// Implement the mods
mod composer;
mod environment;
mod worker;

// Bind the real names for the mods;
use composer::reader::{read,Yaml};
use composer::validator::validate;
use environment::arguments;
use environment::arguments::Arguments;
use environment::mrerror::Result;

fn main
() -> ()
{
	match entrypoint()
	{
		Ok(_)    => println!("[+] All done!"),
		Err(err) => println!("[!] {}.", err.kind.as_str())
	}
}

fn entrypoint
() -> Result<()>
{
	// Get the arguments
	let arguments: Arguments = arguments::get();
	let composer: &str = arguments.value_of("composer").unwrap();
	// Parse the composer
	let data: &Yaml = &read(composer)?;
	let _work: () = validate(data)?;

	Ok(())
}

