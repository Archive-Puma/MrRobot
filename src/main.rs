mod app;
use app::*;

fn main() {
    match entrypoint() {
        Ok(_) => println!("{}", "[+] All done!".bold().green()),
        Err(exception) => println!("{} {}", "[!]".bold().red(), exception.message().bold().red()),
    }
}

fn entrypoint() -> Value<()> {
    // Parse the Arguments
    let args: Arguments = arguments::parse();    
    // Show the banner
    if ! args.is_present("no-banner") { banner::show(); }
    // Read the composer
    let filename: &str = args.value_of("composer").unwrap();
    let data: Yaml = composer::get(filename)?;
    // Get the steps to follow
    let _steps: &Vec<Yaml> = composer::steps::get(&data)?;
    
    Ok(())
}