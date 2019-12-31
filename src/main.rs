mod app;
use app::*;

fn main() {
    match entrypoint() {
        Ok(_) => println!("{}", "[+] All done!".bold().green()),
        Err(exception) => println!("{} {}", "[!]".bold().red(), exception.message().bold().red()),
    }
}

fn entrypoint() -> Value<Report> {
    // Parse the Arguments
    let args: Arguments = arguments::parse();    
    // Show the banner
    if ! args.is_present("no-banner") { banner::show(); }
    // Read the composer
    let filename: &str = args.value_of("composer").unwrap();
    let data: Yaml = composer::get(filename)?;
    // Run the steps
    let report: Report = composer::steps::run(&data)?;
    report.display(100);

    Ok(report)
}