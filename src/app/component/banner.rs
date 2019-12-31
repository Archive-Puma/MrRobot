use colored::Colorize;

pub fn show() {
    let banner = &[
        "",
        "        \\  |         _ \\         |           |",
        "       |\\/ |   __|  |   |   _ \\  __ \\   _ \\  __|",
        "       |   |  |     __ <   (   | |   | (   | |",
        "      _|  _| _| _) _| \\_\\ \\___/ _.__/ \\___/ \\__|",
        "                                   @CosasDePuma",
        ""
    ].join("\n");

    println!("{}", banner.bold().red())
}