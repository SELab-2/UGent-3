"""Main file of the seeder package, will parse given uid and pass it to the seeder function"""
import argparse
from sys import path

from .seeder import into_the_db

path.append(".")

# Create a function to parse command line arguments
def parse_args():
    """Parse the given uid from the command line"""
    parser = argparse.ArgumentParser(description='Populate the database')
    parser.add_argument('my_uid', type=str, help='Your UID')
    return parser.parse_args()

# Main function to run when script is executed
def main():
    """Parse arguments, pass them to into_the_db function"""
    args = parse_args()
    into_the_db(args.my_uid)

if __name__ == '__main__':
    main()
