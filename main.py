import sys
from dotenv import load_dotenv
load_dotenv()


examples=[
    "e1_original", "e1",
    "e2",
    "e4"
    ]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No example selected")
        exit(0)
        
    example_id = sys.argv[1]
    if example_id in examples:
        __import__(f'examples.{example_id}')
    else:
        print(f'Invalid example {example_id}')