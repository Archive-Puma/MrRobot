// external crates (argument parser)
pub use clap::ArgMatches as Arguments;
use clap::{App, AppSettings, Arg};

pub fn get_arguments() -> Arguments<'static> {
    App::new("Mr.Robot")
        .version("1.0.0")
        .author("Kike Fontán (@CosasDePuma) <kikefontanlorenzo@gmail.com>")
        .about("A robot to automate the hacking process")
        .setting(AppSettings::ArgRequiredElseHelp) // shows help if not arguments provided
        .setting(AppSettings::ColorNever) // shows the help without colors
        .setting(AppSettings::NextLineHelp) // places the help string on the line after
        .setting(AppSettings::UnifiedHelpMessage) // joins FLAGS and OPTIONS in a single group
        .arg(
            Arg::with_name("composer")
                .short("f")
                .long("file")
                .required(true)
                .takes_value(true)
                .help("Specifies the composer"),
        )
        .get_matches()
}

/* Documentation
    - https://docs.rs/clap/2.31.1/clap/enum.AppSettings.html
    - https://docs.rs/clap/2.31.1/clap/enum.ArgSettings.html
*/
