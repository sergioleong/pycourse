import os
from dotenv import load_dotenv


def main(argv):
    load_dotenv()
    if argv:
        print(f"This is the content of {argv[0]} environment variable:")
        print(os.getenv(argv[0]))
