import pytest
from os import path, listdir
import json
from e7 import Animal, Dog

def test_e7_exercise_1():
    animal = Animal("Tama", 1)
    assert isinstance(animal, Animal)

def test_e7_exercise_2():
    animal = Animal("Tama", 1)
    assert isinstance(animal, Animal)
    assert str(animal) == "Animal(name: Tama, age: 1)"

def test_e7_exercise_3():
    animal = Animal("Tama", 1)
    assert isinstance(animal, Animal)
    assert animal.getName() == "Tama"
    assert animal.getAge() == 1

def test_e7_exercise_4():
    animal = Animal("Tama", 1)
    assert isinstance(animal, Animal)
    assert animal.getAge() == 1
    animal.increaseAge()
    assert animal.getAge() == 2

def test_e7_exercise_5():
    dog = Dog("Kuro", 3, "Great Dane")
    assert isinstance(dog, Animal)
    assert isinstance(dog, Dog)
    assert dog.getName() == "Kuro"
    assert dog.getAge() == 3
    assert dog.getBreed() == "Great Dane"

def test_e7_exercise_6():
    dog = Dog("Kuro", 3, "Great Dane")
    assert isinstance(dog, Animal)
    assert isinstance(dog, Dog)
    assert dog.getName() == "Kuro"
    assert dog.getAge() == 3
    assert dog.getBreed() == "Great Dane"
    assert str(dog) == "Dog(name: Kuro, breed: Great Dane, age: 3)"
    assert dog.speak() == "Woof!"
