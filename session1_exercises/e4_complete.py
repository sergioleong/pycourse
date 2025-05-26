'''Exercise 1: List all files under the files directory. Return a list with their full paths.
'''
def ex1()-> list():
    from os import path, listdir
    files_dir = path.join(path.dirname(__file__), 'files')
    return [path.join(files_dir, f) for f in listdir(files_dir) if path.isfile(path.join(files_dir, f))]

'''Exercise 2: List all json files under the files directory. Return a list with their full paths.
'''
def ex2()-> list():
    files = ex1()  # Reuse ex1 to get all files
    return [f for f in files if f.endswith('.json')]

'''Exercise 3: List all json and txt files under the files directory. Return a list with their full paths.
'''
def ex3()-> list():
    files = ex1()  # Reuse ex1 to get all files
    return [f for f in files if f.endswith('.json') or f.endswith('.txt')]

'''Exercise 4: Read file f from the files directory and return its content as a string.
Return None if the file does not exist.
'''
def ex4(f : str)-> str:
    from os import path, listdir
    files_dir = path.join(path.dirname(__file__), 'files')
    file_path = path.join(files_dir, f)
    if not path.isfile(file_path):
        return None
    with open(file_path, 'r') as file:
        return file.read()

'''Exercise 5: Read file f from the files directory and return its formated content as a string.
The formated content should replace all ocurrences of {name} with the value of the variable name.
Return None if the file does not exist.
'''
def ex5(f : str, name : str)-> str:
    txt = ex4(f)
    if txt is None:
        return None 
    return txt.format(name=name)
    
'''Exercise 6: Read file f from the files directory and return its formated content as a string.
The formated content should replace all ocurrences of the keys in the dictionary vals with their corresponding values.
E.g. if vals= {'name': 'John', 'age': 30}, the content should replace {name} with John and {age} with 30.
Return None if the file does not exist.
'''
def ex6(f : str, vals : dict)-> str:
    txt = ex4(f)
    if txt is None:
        return None 
    return txt.format_map(vals)

'''Exercise 7: Create or overwrite file "file_path" and write the variable "content" to it.
'''
def ex7(file_path : str, content : str) -> None:
    with open(file_path, 'w') as file:
        file.write(content)