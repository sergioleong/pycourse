'''Exercise 1: Read json file f from the files directory and return its content.
Return None if the file does not exist.
'''
def ex1(f : str)-> str:
    from os import path, listdir
    import json
    files_dir = path.join(path.dirname(__file__), 'files')
    file_path = path.join(files_dir, f)
    if not path.isfile(file_path):
        return None
    with open(file_path, 'r') as file:
        return json.load(file)

'''Exercise 2: Read json file f from the files directory and return the value of the key k.
Return None if the file does not exist or the key is missing.
'''
def ex2(f : str, k : str)-> str:
    data = ex1(f)
    if data is None or k not in data:
        return None
    return data[k]

'''Exercise 3: Read json file f from the files directory and add value v to key k and return the new content.
Return None if the file does not exist.
'''
def ex3(f : str, k : str, v: str)-> str:
    data = ex1(f)
    data[k] = v
    return  data

    
'''Exercise 4: Create or overwrite file "file_path" and write the json object "data" to it.
'''
def ex4(file_path : str, content : dict) -> None:
    import json
    with open(file_path, 'w') as file:
        json.dump(content, file)