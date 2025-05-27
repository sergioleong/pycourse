class Animal:
    '''Exercise 1: Write the __init__ method for the Animal class.
    It should take two arguments, name and age.
    '''
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    '''Exercise 2: Override the __str__ method to return a string representation of the animal.
    The string should be in the format "Animal(name: <name>, age: <age>)".
    '''
    def __str__(self) -> str:
        return f"Animal(name: {self.name}, age: {self.age})"

    '''Exercise 3: Write a method getName that returns the name of the animal and a method getAge that returns the age of the animal.
    '''
    def getName(self) -> str:
        return self.name

    def getAge(self) -> int:
        return self.age

    '''Exercise 4: Write a method increaseAge that increases the age of the animal by 1.'''
    def increaseAge(self) -> None:
        self.age += 1

    def speak(self) -> str:
        return "..."

'''Exercise 5: Update the Dog class to inherit from the Animal class.
The Dog class should have an additional attribute breed.
Add also a method getBreed that returns the breed of the dog.
'''
class Dog(Animal):
    def __init__(self, name:str, age: int, breed:str):
        super().__init__(name, age)
        self.breed = breed
    def getBreed(self) -> str:
        return self.breed

    '''Exercise 6: Override methods:
    - the __str__ method in the Dog class to return a string representation of the dog.
        "Dog(name: <name>, breed: <breed>, age: <age>)".
    - the speak method in the Dog class to return "Woof!".'''
    def __str__(self) -> str:
        return f"Dog(name: {self.name}, breed: {self.breed}, age: {self.age})"
    def speak(self):
        return "Woof!"