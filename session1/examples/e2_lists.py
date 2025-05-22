# Working with lists
print("Working with lists:")

mylist = []
print(f"mylist is empty after creation: {mylist}")
print(f"mylist now has lenght: {len(mylist)}")
print(f"is mylist empty?: {not mylist}")

mylist.append(1)
mylist.append(2)
mylist.append(3)
mylist.append("a")
mylist.append("b")
mylist.append("c")
mylist.append(["b", 2])
print(f"mylist now has few elements in it: {mylist}")
print(f"mylist now has lenght: {len(mylist)}")
print(f"is mylist empty?: {not mylist}")

e = mylist.pop()
print(f'we have removed the last element "{e}": {mylist}')
print(f"mylist now has lenght: {len(mylist)}")

e = mylist.pop(2)
print(f'we have removed the 3th element "{e}": {mylist}')
print(f"mylist now has lenght: {len(mylist)}")

print(f'mylist contains "c"? : {"c" in mylist}')
print(f'Lets remove element "c"')
mylist.remove("c")
print(f'mylist contains "c"? : {"c" in mylist}')


print(f'the first element in mylist is 0 : "{mylist[0]}"')
print(f'the last element in mylist is -1 : "{mylist[-1]}"')
print(f'and the second to last element in mylist is -2 : "{mylist[-2]}"')
print(
    f'this is a sublist with all elements without the extremes (1,-1) :  "{mylist[1:-1]}"'
)
print(
    f'you will get an empty sublist if the same incide is used (1,1) : "{mylist[1:1]}"'
)
print(f'also if second indice is lower than the first (1,0) : "{mylist[1:0]}"')
print(f'also if second indice is lower than the first (1,0) : "{mylist[1:0]}"')
print(
    f'this is a sublist with all elements after the second one (2,) :  "{mylist[2:]}"'
)

print(f'mylist + mylist : "{mylist+mylist}"')
