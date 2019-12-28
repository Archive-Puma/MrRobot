//! # mrrobot
//! 
//! The `mrrobot` crate let you to automatize the hacking process.
//! 
//! It works by using *YAML* files, which collect all the instructions to be performed against certain objectives.
//! 
//! Here is a `composer-example.yaml` file:
//! 
//! ```yml
//! version: 1
//! hack:
//!   - target:
//!       type: url
//!       url: https://2019shell1.picoctf.com/problem/61676/
//!     steps:
//! 	  - run: gets
//!	      - run: html_comments
//! ```
//!
//! # TODO
//! - [ ] work/web/get_body append url param
//! - [ ] composer/steps -> save results -> link results
//! - [ ] make macro (match Ok(value) => Ok(value), _ => throw($Error))

// Implement the mods
mod environment;
mod composer;
mod work;

// Use crate utilities
use self::composer::{read,validate,Yaml,get_steps,run_steps};
use self::environment::{Arguments,get_arguments,Result};

fn main() {
	match entrypoint() {
		Ok(_)    => println!("[+] All done!"),
		Err(err) => println!("[!] {}.", err.kind.as_str())
	}
}

fn entrypoint() -> Result<()> {
	// Get the arguments
	let arguments: Arguments = get_arguments();
	let composer: &str = arguments.value_of("composer").unwrap();
	// Parse the composer
	let data: &Yaml = &read(composer)?;
	// Validate the data
	validate(data)?;
	// Get the steps
	let steps: &Vec<Yaml> = get_steps(data)?;
	// Run the steps
	let _result = run_steps(steps);

	Ok(())
}

