extern crate clap;

use clap::{App,Arg,AppSettings,ArgMatches};

pub fn get
() -> ArgMatches <'static>
{
	return App::new("Mr.Robot")
		.version("1.0.0")
		.author("Kike Fontán (@CosasDePuma) <kikefontanlorenzo@gmail.com>")
		.about("A robot to automate the hacking process")

		.setting(AppSettings::ArgRequiredElseHelp)		// shows help if not arguments provided
		.setting(AppSettings::ColorNever)				// shows the help without colors
		.setting(AppSettings::NextLineHelp)				// places the help string on the line after
		.setting(AppSettings::UnifiedHelpMessage)		// joins FLAGS and OPTIONS in a single group

		.arg(Arg::with_name("file")
				.short("f")
				.long("file")
				.required(true)
				.takes_value(true)
				.help("Specifies the compose file"))
		.get_matches();
}

/* Documentation
	- https://docs.rs/clap/2.31.1/clap/enum.AppSettings.html
	- https://docs.rs/clap/2.31.1/clap/enum.ArgSettings.html
*/