def main(argv):
    if argv:
        new_val = argv[0]
    else:
        new_val = 'Donut'

    txt = 'This is a single-line string, delimited by single-quotes \'<text>\''
    print(txt)

    txt = "This is a single line string, delimited by double-quotes \"<text>\""
    print(txt)

    txt = '''>>>
This is a multi-line string
It can be delimited by trhree single-quotes \'\'\'<text>\'\'\'' or by three double-quotes """<text>"""
<<<'''
    print(txt)

    a = "Hello"
    b = 'World'
    print(f'''>>>
Two strings can be concatenated with the + operator:
    "{a}" + "{b}"
retults in:
    "{a+b}"
<<<''')

    txt = 'One Ring to rule them all, One Ring to find them, One Ring to bring them all and in the darkness bind them.'

    print(f'''>>>
We can get the length of a string with len():
    {len(txt)}
We can transform a string to uppercase with the .upper() method:
    "{txt.upper()}"
And we can transform it to lowercase with the .lower() method:
    "{txt.lower()}"
And we can capitalize with the .capitalize() method:
    "{txt.lower().capitalize()}"
And mucho more.
<<<''')

    keyword = "ring"
    print(f'''>>>
We can also use "in" to check if a substring exists:
    "{keyword} exists: {keyword in txt}"
We can also use the .find() method returns the index of the first occurence of a substring in a string.
    "{keyword} is at position {txt.find(keyword)}"
Mmmm... this didn't work quite right, thats the position of bring. Let's try again all in lowercase:
    "{keyword} is at position {txt.lower().find(keyword)}"

We can use .replace() to replace a substring in a string:
    "{txt.replace('Ring', new_val)}"
And we can also use .count() to count the number of occurences of a substring in a string.
    "{keyword.capitalize()} occurs {txt.count(keyword.capitalize())} times"
<<<''')

    print(f'''>>>
We can split a string into a list of words with the .split() method:
    "{txt.split(' ')}"
And we can split them on different values, like spaces and commas:
    "{txt.split(',')}"
>>>
<<<''')

    print(f'''>>>
We can merge multiple values into a unique string also with the .join() method:
    "{', '.join(['Apple', 'Banana', 'Orange'])}"
And we can remove all spaces at the beginning and at the end of  a string using the .strip() method:
    "{'               WAAAAAAAAAAAA           '.strip()}"
>>>
<<<''')

    print(f'''>>>
Like with strings, we can get substrings using indexing. 
    "{txt[:20]}..."
We can also use negative indexes to count from the end of a string.
    "...{txt[-20:]}"
<<<''')


    print('''>>>
A little late to say this but you can also do cool stuff like format the text with your variables.
We have been doing it all this time with f-strings (f"text {variable} text").
>>>''')

    template = 'This text is a template where {keyword} will be replaced with the value provided.'
    keyword = "Wololo"
    print(f'''>>>
But we can also use .format() method if we want to provide the formating more dinamically:
    "{template.format(keyword=new_val)}"
<<<<''')