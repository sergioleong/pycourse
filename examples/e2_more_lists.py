# Lists Comprehension
# Still working with lists

a = [1,2,3]

print(f'''Until now we have been working with lists in a simple way, were we have either manually defined them or added the parameters with append method. E.g.:
    a = [1,2,3] 
    -> {a}
''')

b = list(range(10))
print(f'''But what if we wan to create for example a list of numbers from 0 to 9? We can do that converting a range object into a list instead of manually defining it. E.g.
    b = list(range(10)) 
    -> {b}
''')

c =[x*x for x in b]
print(f'''Ok, but that's is still quite simple, so now what if we want to do the same, but with the squares of those numbers from the previous list? We can do that using what is called list comprehension. E.g.
    c = [x*x for x in b] 
    -> {c}
''')

d =[(x,x*x) for x in b]
print(f'''We don't need to limit ourself to simple types also, but we could for example return a list of tuples both with the original value and the square. E.g.
    d = [(x,x*x) for x in b] 
    -> {d}
''')

e =[(x,x*x) for x in b if x%3 != 0]
print(f'''We can also add some conditions to our list comprehension, e.g. we want only the numbers that are not divisible by three.
    e = [(x,x*x) for x in b if x%3 != 0] 
    -> {e}
''')

f = [(x,"Odd" if x%2 != 0 else "Even") for x in b]
print(f'''Conditionals and other functions can be also used on the generated values, e.g. we want the odd numbers to be represented as "Odd" and even ones as "Even". E.g.
    f = [(x,"Odd" if x%2 != 0 else "Even") for x in b] 
    -> {f}
''')


h = [(x,y,x*y) for x in range(4) for y in range(5)]
print(f'''We can also perform a nested loop inside a list comprehension. E.g.
    h = [(x,y,x*y) for x in range(4) for y in range(5)] 
    -> {h}
''')


matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
g = [num for row in matrix for num in row]
print(f'''And these nested loops can be dependent on each other. E.g.
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    g = [cell for row in matrix for cell in row] -> {g}
This example is equivalent to:
    g = []
    for row in matrix:
        for cell in row:
            g.append(cell)
''')

print(f'''Of course we can also use these new lists like any other list.
    print(g[0]) -> {g[0]}
    print(g[-1]) -> {g[-1]}
    print(g[2:5]) -> {g[2:5]}
    print(len(g)) -> {len(g)}
''')
