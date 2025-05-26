import pytest
import e3_complete as e3


def test_e3_exercise_1():
    assert e3.ex1('Hello World') == 'HELLO WORLD'

def test_e3_exercise_2():
    assert e3.ex2('Hello World') == 'hello world'

def test_e3_exercise_3():
    assert e3.ex3('Hello World') == 'HeLlO WoRlD'

def test_e3_exercise_4():
    assert e3.ex4('Hello World', 'World')
    assert e3.ex4('Hello World', 'world')
    assert e3.ex4('Hello World', 'car') == False

def test_e3_exercise_5():
    assert e3.ex5('Hello World') == [0,1,0,2,0]
    assert e3.ex5('AAaadjhjhjk222eeeEiiOOuuuUUd--591') == [4, 4, 2, 2, 5]