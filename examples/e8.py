from os import path
import sys
import json

def main(argv):
    #Defining the variables for the example files
    folder = path.dirname(path.abspath(__file__))
    file_path1 = path.join(folder,"json_e8_1.json")
    file_path2 = path.join(folder,"json_e8_2.json")


    print(f'''In this example, we will see how to work with json files. For that, first let's define some variables like in previous eample:
    Current folder : folder = path.dirname(path.abspath(__file__)) -> {folder}
    Source File : file_path1 = path.join(folder,"json_e8_1.json") -> {file_path1}
    Destination File : file_path2 = path.join(folder,"json_e8_2.json") -> {file_path2}
    ''')


    #Reading the json files and printing them to console
    print(f'''We can read a json file using the `json` module. For that we will use the `load()` function from the `json` module. This function takes a file object and returns a python dictionary.
    Let's read our first example file: {file_path1}
    ''')
    
    with open(file_path1, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f'''And done, as easy as that. Now we can use the content of the file as any other python dictionary. For example, let's print the parameter example_name "{data["example_name"]}"
    ''')

    print(f'''This json file contains a list of pokemon with an id, name and type in the "pokemons" key. Now let's get all pokemons from that list with fire type creating a new list "fire_pokemon" with the filtered ones.
    ''')
    fire_pokemon = []
    for pokemon in data["pokemons"]:
        if "fire" in pokemon["type"]:
            fire_pokemon.append(pokemon)
    print(len(fire_pokemon))
    
    print(f'''Now we can save our new list to a json file with the name {file_path2}.
For that, like before we are going to first open our file, in this case as write only mode, and use this time the json.dump method to save our new list.    
''')
    with open(file_path2, "w", encoding="utf-8") as f:
        json.dump({"example_name": "fire_pokemon", "pokemons": fire_pokemon}, f)

    print(f'''And that's all, JSON files in python are very easy to use and we can do a lot of things with them. 
    But we are also not limited to file operations, but we can work also directly on strings if correctly formated.
''')

    json_string = '[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]'
    
    print(f'''Let's consider this string:
    {json_string}
We can use the function loads from the json module to convert it into a list of values.
    {json.loads(json_string)}
''')
    prime_numbers = json.loads(json_string)
    
    print(f'''We can also use the function dumps from the json module to convert our list back into a string, which is very useful for file operations or when reading data from online services, as we will see next.
    {json.dumps(prime_numbers)}
''')
    