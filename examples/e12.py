
def is_even(v: int) -> bool:
    if not type(v) is int:
        raise TypeError(f"Expected int, got {type(v)}")
    if v == 0:
        raise ValueError("Zero is not a valid value")
    return v % 2 == 0

def divide(a:int, b:int) -> float:
    return a / b

def is_valid_username(username):
    if not type(username) is str:
        raise False
    if len(username) < 5 or len(username) > 20:
        return False
    return True

def main(argv):
    try:
        print(is_even(0))
    except Exception as e:
        print(f"Error: {e}")
    try:
        print(is_even(1))
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        print(is_even(2))
    except Exception as e:
        print(f"Error: {e}")
    try:
        print(is_even('hello'))
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        print(is_even(int(argv[0])))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(divide(1, 2))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(divide("a", 2))
    except Exception as e:
        print(f"Error: {e}")
        