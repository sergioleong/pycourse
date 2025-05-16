import sys

examples_direct = ["e1_original", "e1", "e2_types", "e2_lists", "e2_conditionals"]
examples_direct_function = ["e4", "e5"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No example selected")
        exit(0)

    example_id = sys.argv[1]
    if example_id in examples_direct:
        print(f"Executing {example_id}")
        __import__(f"examples.{example_id}")
    elif example_id in examples_direct_function:
        print(f"Executing {example_id}")
        cls = __import__(
            f"examples.{example_id}", globals(), locals(), fromlist=["main"]
        )
        cls.main(sys.argv[2:])
    else:
        print(f"Invalid example {example_id}")
