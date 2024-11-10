import argparse
import asyncio

from utils.seeder import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", help="tbd lol") # Add support for passing tables
    args = parser.parse_args()
    asyncio.run(main(args.arg))
