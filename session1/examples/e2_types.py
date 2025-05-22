# Let's create a list of values
values = [
    None,
    False,
    True,
    1,
    1.1,
    "hello",
    b"hello",
    (1, 2),
    [1, 2],
    {1, 2},
    {1: 1, 2: 2},
    {"a": 1, "b": 2},
    range(10),
]

# For each value, let's see it's given type
for v in values:
    print(f"The type of {v} is {type(v)}")
print("")
