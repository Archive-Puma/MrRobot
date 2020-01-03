use log::*;
use simplelog::*;
use std::fs::File;

fn num2level(lvl: u64) -> LevelFilter {
    match lvl {
        0 => LevelFilter::Warn,
        1 => LevelFilter::Info,
        2 => LevelFilter::Debug,
        _ => LevelFilter::Trace
    }
}

fn config() -> Config {
    ConfigBuilder::new()
        .clear_filter_allow()
        .add_filter_allow_str("mrrobot")
        .set_target_level(LevelFilter::Off)
        .set_thread_level(LevelFilter::Off)
        .set_time_to_local(true)
        .build()
}

pub fn init(file: &str, lvl: u64) {
    let log_level: LevelFilter = num2level(lvl);
    CombinedLogger::init(vec![
        WriteLogger::new(log_level, config(), File::create(file).unwrap())
    ]).unwrap();
}