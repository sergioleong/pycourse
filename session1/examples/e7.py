from os import listdir, path, walk, getcwd
import sys

def main(argv):
    # Navigation
    print(f'''When working with files, we may want to find the path of an specific file or folder.
For this we can use path.abspath() to get the absolute path from a relative path.
If we want to know where our current file is located, we can use path.abspath() with __file__ as argument.
    {path.abspath(__file__)}
Similar, if we want to know the folder where that file is located, we can use path.dirname() with __file__ as argument.
    {path.dirname(path.abspath(__file__))}

We can easily check if a given path is a directory or a file:

    If it's a file:
        path.isfile(path.abspath(__file__)) -> {path.isfile(path.abspath(__file__))}   
    If it's a directory:
        path.isdir(path.dirname(path.abspath(__file__))) -> {path.isdir(path.dirname(path.abspath(__file__)))}

    We may also want to know the current execution path. that is provided by getcwd function in sys module
    {path.abspath(getcwd())}

    Or we may want to know the path for our main script, for that we can get the path from sys.argv[0] as we commented before, as that gets the main script.
    {path.abspath(path.dirname(sys.argv[0]))}
''')


    # As all examples are in the same folder as this script, we can use that value 
    folder = path.dirname(path.abspath(__file__))
    print(f'''Lets list all example files from the {folder} directory
For that we can use the function listdir from the os module, which returns a list of strings with all file names inside the folder
As we want them sorted, we can use the function sorted to sort our list of files by name and do some checks on the filenames to print only the example text
''')
    
    for f in sorted(listdir(folder)):
        if f.startswith("e") and not f.endswith(".py"):
            print(f'\t{folder}/{f}')

    print()
    print(f'''In this case, we have all the files from our examples in the same folder, but the same could have been divided between different subdirectories.
    In that case, we could use the function walk from the os module to list all files and directories inside a folder.
    The function walk returns a tuple with the root directory name, all subdirectories and all files inside that folder.
    The topdown parameter determines if results will be returned from the root directory or from the branches first.
    In this case, we are using the topdown parameter as True to list all files and directories from the root directory.
    ''')
    for (root,dirs,files) in walk(folder, topdown=True):
        print("Directory path: %s"%root)
        print("Directory Names: %s"%dirs)
        print("Files Names: %s"%files)
        print()

    
    # Files
    file_path = path.join(folder,"txt_e7.txt")
    print(f'''Now let's create a new file in the folder and write some text inside it.
As before, we are going to use the folder {folder} for our file and name the file txt_e7.txt.
To get the file path, we will use the function path.join from the os module. The function join takes two arguments: the folder and the name of the file.
path.join(folder,"txt_e7.txt") --> {file_path}
''')

    print(f'''To open the file we will use the function open. 
This function open takes two arguments: the file path and the mode.
The main modes are:
 - r - read only
 - w - write only (it creates the file if it doesn't exist and replaces its content if it does exist)
 - a - append (it creates the file if it doesn't exist and adds content at the end of the file
We can also specify if we are working with text or binary files within the mode parameter
 - t - text (default)
 - b - binary
E.g. To read a binary file we can use rb

For text modes, we can also provide the encoding parameter, which specifies the encoding of the file.
E.g. To read a UTF-8 encoded file we can use utf-8
''')

    f = open(file_path,"w", encoding="utf-8")
    print(f'''Now let's create our new file:
        f = open(file_path,"w", encoding="utf-8") --> {f}
    ''')

    print(f'''To write to a file we will use the function write. 
This function takes one argument: the content of the file.
E.g. To write "Hello World" to our new file we can use:
    f.write("Hello World") -> {f.write("Hello World"+str(chr(10)))}
We can also write multiple lines at once by using a list of strings and passing it as an argument to the function write.
E.g. To write "Hello World" and "Goodbye World" to our new file we can use:
    f.writelines(["How are you?", "Goodbye World"]) -> {f.writelines(["How are you?"+str(chr(10)), "Goodbye World"])}
''')

    print(f'''Finally, it's important to close our file after we have finished writing to it.
E.g. To close our new file we can use:
    f.close() -> {f.close()}
''')

    print(f'''Now we can read back the content of our file.
For that, we will use again the open function, now with the read mode (r).
Instead of opening and then closing the file after we are done with it, we are going to use the with statement. 
This is a way to automatically close the file when we are done with it:
    with open(file_path, "r", encoding="utf-8") as f:
        do something with f

Then, we are going to read the content of our file into a variable called text.
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
''')
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # f will be closed here automatically

    print(f'''Now text contains the content of our file:
>>>
{text}
<<<
''')

    print(f'''Instead of reading the full content of the file at once, we could for example read it line by line to add the line number to them before printing for example..
We can do that using a for loop.
    i = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            print(f'{{i:03d\}}:{{line.strip()}})
            i += 1
''')
    i = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            print(f'{i:03d}: {line.strip()}')
            i += 1
