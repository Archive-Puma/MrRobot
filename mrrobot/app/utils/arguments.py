import argparse

def parse():
    # Name and description
    parser = argparse.ArgumentParser(
        prog="mrrobot",
        description="A robot to automate the hacking process",
        add_help=True)
    # ---- Information
    information = parser.add_argument_group(title="information")
    # Version
    information.add_argument(
        "--version",
        action="version",
        version="MrRobot v1.0.0 (Python)",
        help="Prints the version")
    # ---- Performance
    performance = parser.add_argument_group(title="configuration")
    # Clean
    performance.add_argument(
        "--clean",
        action="store_true",
        help="Removes the default configuration if exists")
    # File (Configuration)
    performance.add_argument(
        "-c", "--config",
        metavar="INI",
        action="store",
        help="Specifies the configuration file")
    # Flag format
    performance.add_argument(
        "-f", "--flag",
        metavar="FLAG",
        action="store",
        help="Specifies the regex-based flag format")
    # Banner
    performance.add_argument(
        "--no-banner",
        action="store_true",
        help="Hides the banner")
    # Threads
    performance.add_argument(
        "-T", "--threads",
        metavar="#",
        type=int,
        help="Specifies the number of threads")
    # ---- Units Group
    units = parser.add_argument_group(title="available categories")
    # All
    units.add_argument(
        "-a", "--all",
        action="store_true",
        help="Loads all the units"
    )
    # Esoteric
    units.add_argument(
        "-e", "--esoteric",
        action="store_true",
        help="Loads the esoteric units"
    )
    # Parse the arguments
    return parser.parse_args()