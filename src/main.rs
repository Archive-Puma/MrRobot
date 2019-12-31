mod app;
use app::*;

fn main() {
    entrypoint();
}

fn entrypoint() {
    // Parse the Arguments
    let args: Arguments = arguments::parse();    
    // Show the banner
    if ! args.is_present("no-banner") { banner::show(); }
}