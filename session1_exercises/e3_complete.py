'''Exercise 1: Write a function that given an string t will return it in uppercases.
'''
def ex1(t :str)-> str:
    return t.upper()

'''Exercise 2: Write a function that given an string t will return it in lowercase.
'''
def ex2(t :str)-> str:
    return t.lower()

    
'''Exercise 3: Write a function that given an string t will return a new string where letters in even positions are uppercase and the rest lowercase.
    Example: 'Hello' -> 'HeLlO'
'''
def ex3(t :str)-> str:
    return ''.join([x.upper() if i%2==0 else x.lower() for i,x in enumerate(t)])

'''Exercise 4: Write a function that given an string t and a word w will tell us if w is contained in t.
This should be case insensitive.
'''
def ex4(t :str, w:str)-> int:
    return w.lower() in t.lower()

'''Exercise 5: Write a function that given an string t, it will tell us for each vowel, how many times it appears in the string.
Response should be a list of 5 values [#a, #e, #i, #o, #u]
    Example: 'Hello' -> [0,1,0,1,0]
'''
def ex5(t :str)-> int:
    t = t.lower()
    return [t.count('a'), t.count('e'), t.count('i'), t.count('o'), t.count('u')]