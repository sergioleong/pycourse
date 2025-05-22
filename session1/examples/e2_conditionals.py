# ***Conditionals***

values = [True, False, 0, 1, 0.0, 1.1, "a", "", [1, 2, 3], [], None]

for v in values:
    if v:
        print(f'Value "{v}" is True')
    else:
        print(f'Value "{v}" is not True')
    if v is None:
        print(f'*Value "{v}" is None')

print()
values = [
    [True, True],
    [True, False],
    [False, False],
]
for v in values:
    print(f"{v[0]} AND {v[1]} is {v[0] and v[1]}")
print("-----------")
for v in values:
    print(f"{v[0]} OR {v[1]} is {v[0] or v[1]}")

print()

# ***Loops***

print("This will print a list of 10 elements")
for i in range(10):
    print(f"   {i}")

i = 1
j = 1
print("This will print the fibonatchi series until 50")
while j < 50:
    print(f"   {i} + {j} --> {i+j}")
    t = i + j
    i = j
    j = t
