use clap::{App, AppSettings, Arg};
pub use clap::ArgMatches as Arguments;

pub fn parse() -> Arguments<'static> {
    App::new("Mr.Robot")
        .version("v1.0")
        .author("Kike Fontán (@CosasDePuma) <kikefontanlorenzo@gmail.com>")
        .about("A robot to automate the hacking process")
        .setting(AppSettings::ArgRequiredElseHelp) // shows help if not arguments provided
        .setting(AppSettings::ColorNever)          // shows the help without colors
        .setting(AppSettings::NextLineHelp)        // places the help string on the line after
        .setting(AppSettings::UnifiedHelpMessage)  // joins FLAGS and OPTIONS in a single group
        .arg(
            Arg::with_name("no-banner")
                .long("no-banner")
                .help("Don't display the banner")
        )
        .arg(
            Arg::with_name("verbosity")
                .short("v")
                .multiple(true)
                .help("Set the verbosity level (Default: -vv).")
        )
        .arg(
            Arg::with_name("logger")
                .short("l")
                .long("logger")
                .takes_value(true)
                .help("Enable and specifies the log file")
        )
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
    - https://docs.rs/clap/2.33.0/clap/
    - https://docs.rs/clap/2.31.1/clap/enum.ArgSettings.html
*/