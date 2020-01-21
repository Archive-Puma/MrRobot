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
        version="MrRobot v1.0 (python)",
        help="Prints the version")
    # Version
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Hides the banner")
    # File (Composer)
    parser.add_argument(
        "-f", "--file",
        required=True,
        metavar="FILE",
        action="store",
        help="Specifies the composer")
    # Parse the arguments
    return parser.parse_args()