# Exceptions and Errors

def main(argv):
    print('''Until now we have considered that our code is correct and there would be no errors during the execution, but thats clearly not always the case as we can also encounter some exceptions in our code, specially if we work with user interaction or external services.

Luckily Python has a very good support for this kind of situations. We will see how to handle them and what are their different types.
''')


    print('''Untreated exceptions will break our program, so we need to be able to catch them and deal with them in some way. This is done by using the try/except statement.

Let's consider the following piece of code:
    b = int(input('Enter an integer: ')) + 1
    print(b)
As you can see, this is a very simple example that will break if we enter something other than an integer. E.g. If we try to run with the value "Hello", Python will raise an exception "ValueError: invalid literal for int() with base 10: 'Hello'" and stop our program.
''')


    print('''We can catch this kind of exceptions using a try/except statement and try to correct the error in some way. For example:
    try:
        b = int(input('Enter an integer: '))
    except :
        b = 1
    print(b)
In this case, for example we will default to 1 if there is any error.
''')
    try:
        b = int(input('Enter an integer: '))
    except:
        b = 1
    print(f'''New value of b is {b}
''')

    print('''While a lot of times we are not really interested in the exception itself and only want to be able to provide an alternative solution, but we can also get the content of the exception using the "as" keyword. E.g.
    try:
        b = int(input('Enter an integer: '))
    except Exception as e:
        b=1
        print(e)

This will print out the error message that Python generated for us. We can use this to provide a more specific solution, e.g. if we want to catch only the "ValueError" exception.
''')
    try:
        b = int(input('Enter an integer: '))
    except Exception as e:
        b=1
        print(e)
    print(f'''New value of b is {b}
''')

    print('''Sometimes we can also be interested in what kind of exceptions are being raised. E.g.
    try:
        b = 1.0/int(input('Enter an integer: '))
    except ValueError as e:
        b=1
    except ZeroDivisionError as e:
        b=0
In that case, we can capture each exception separately and provide a different solution for each one. E.g. If the input is invalid we can provide one solution and if the inputs results in a division by 0 another
''')
    try:
        b = 1.0/int(input('Enter an integer: '))
    except ValueError as e:
        b=1
    except ZeroDivisionError as e:
        b=0
    print(f'''New value of b is {b}
''')

    print('''We can also use the "else" clause to specify a block that will be executed if no exception was raised. E.g.
        try:
            b = 1.0/int(input('Enter an integer: '))
        except ValueError as e:
            b=1
        else:
            print(f'No exceptions were raised, so we can do this.')
    ''')
    try:
        b = 1.0/int(input('Enter an integer: '))
    except Exception as e:
        print(e)
    else:
        print(f'No exceptions were raised, so we can do this: ')
        print(f'''New value of b is {b}
''')

    print('''We can also use the "finally" clause to specify a block that will be executed regardless if an exception was raised or not. E.g.
        try:
            b = 1.0/int(input('Enter an integer: '))
        except Exception as e:
            b = 0
            print(e)
        else:
            print(f'No exceptions were raised, so we can do this.')
        finally:
            print(f'New value of b is {b}')
''')
    try:
        b = 1.0/int(input('Enter an integer: '))
    except Exception as e:
        b = 0
        print(e)
    else:
        print(f'No exceptions were raised, so we can do this.')
    finally:
        print(f'''New value of b is {b}
''')

    print('''If we want to, we can raise also our own exceptions, too using the raisae keyword. 
    For example, let's say that we want to raise an exception if the value provided by the user is Odd. E.g.
        if b % 2 == 1:
            raise ValueError("Invalid Odd Input")
''')

    try:
        b = 1.0/int(input('Enter an integer: '))
    except Exception as e:
        b = 0
        print(e)
    else:
        print(f'No exceptions were raised, so we can do this.')
    finally:
        if b % 2 == 1:
            raise ValueError("Invalid Odd Input")
        print(f'''{b} is even, so we can do this.
''')

    print('''And of course we can use exceptions within functions, too. E.g.
    def within_fun():
        try:
            return 1.0/int(input('Enter an integer: '))
        except Exception as e:
            return 0
        finally:
            print('That's all folks')
        print('And this won't ba called')
    print(within_fun())
''')
    print(f'The function returns {within_fun()}')

def within_fun():
    try:
        return 1.0/int(input('Enter an integer: '))
    except Exception as e:
        return 0
    finally:
        print('''That's all folks
''')
    print('''And this won't ba called''')