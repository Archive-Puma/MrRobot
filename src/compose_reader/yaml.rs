use std::fs;

extern crate yaml_rust;

pub fn read
(filename: &str) -> ()
{
	let contents = fs::read_to_string(filename)
		.expect("[!] Something went wrong with the file");
	println!("Contains:\n\n{}", contents);
	// return YamlLoader::load_from_str().unwrap();
}