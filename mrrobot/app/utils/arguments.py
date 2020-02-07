import argparse

def parse():
    # Name and description
    parser = argparse.ArgumentParser(
        prog="mrrobot",
        description="A robot to automate the hacking process")
    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="MrRobot v1.0 (Python)",
        help="Prints the version")
    # Banner
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Hides the banner")
    # File (Configuration)
    parser.add_argument(
        "-f", "--file",
        required=False,
        metavar="FILE",
        action="store",
        default=None,
        help="Specifies the configuration file")
    parser.add_argument(
        "-T", "--threads",
        required=False,
        metavar="THREADS",
        type=int,
        default=None,
        help="Specifies the number of threads")
    # Parse the arguments
    return parser.parse_args()