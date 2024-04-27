
import argparse
from .seeder import into_the_db
from sys import path
path.append(".")

# Create a function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Populate the database')
    parser.add_argument('my_uid', type=str, help='Your UID')
    return parser.parse_args()

# Main function to run when script is executed
def main():
    # Parse command line arguments
    args = parse_args()
    print(args.my_uid)
    # Call into_the_db function with the provided UID
    into_the_db(args.my_uid)

if __name__ == '__main__':
    main()