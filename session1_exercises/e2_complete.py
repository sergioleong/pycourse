'''Exercise 1: Use dotenv to load the environment variables from .env file. Return the value of the variable HELLO.'''
def ex1()-> str:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    return os.getenv('HELLO')

'''Exercise 2: Use dotenv to load the environment variables from file f. Return the value of the variable HELLO.
Tip: use the argument override=True in the function call to load_dotenv() in order to replace any previosly loaded environment variables with new ones.
'''
def ex2(f:str)-> str:
    from dotenv import load_dotenv
    import os
    load_dotenv(f, override=True)
    return os.getenv('HELLO')

'''Exercise 3: Use dotenv to load the environment variables from file f. Return the value of the variable named x. None if the variable does not exist.'''
def ex3(f:str, x:str)-> str:
    from dotenv import load_dotenv
    import os
    load_dotenv(f, override=True)
    return os.getenv(x, None)

'''Exercise 4: Clear the current environment variable and then use dotenv to load the environment variables from file f. Return the value of the variable named x. None if the variable does not exist.'''
def ex4(f:str, x:str)-> str:
    from dotenv import load_dotenv
    import os
    os.environ.clear()
    load_dotenv(f, override=True)
    return os.getenv(x, None)