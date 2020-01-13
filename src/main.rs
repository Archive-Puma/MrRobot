mod app;
use app::*;
// Test workflow

fn main() {
    match entrypoint() {
        Ok(_) => {
            info!("All correctly done.");
            println!("{}", "[+] All done!".bold().green());
        },
        Err(exception) => {
            error!("{}", exception.message());
            println!("{} {}", "[!]".bold().red(), exception.message().bold().red());
        },
    }
}

fn entrypoint() -> Value<Report> {
    // Parse the Arguments
    let args: Arguments = arguments::parse();  
    // Verbosity and log
    let verbosity: u64 = args.occurrences_of("verbosity");
    if args.is_present("logger") {
        let logfile: &str = args.value_of("logger").unwrap_or("mrrobot.log");
        logger::init(logfile, verbosity);
    }
    // Show the banner
    if ! args.is_present("no-banner") { banner::show(); }
    // Read the composer
    let filename: &str = args.value_of("composer").unwrap();
    let data: Yaml = composer::get(filename)?;
    // Run the steps
    let report: Report = composer::steps::run(&data)?;
    report.display(100);

    info!("Result: {}", report.to_str());

    Ok(report)
}