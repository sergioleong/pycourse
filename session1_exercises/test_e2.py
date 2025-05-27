import pytest
import e2


def test_e2_exercise_1():
    assert e2.ex1() == 'Hello World'

def test_e2_exercise_2():
    assert e2.ex2('.env2') == 'Hello World2'

    
def test_e2_exercise_3():
    assert e2.ex3('.env2', 'HELLO') == 'Hello World2'
    assert e2.ex3('.env2', 'WORLD') == 'Mars'
    assert e2.ex3('.env2', 'x') is None
    assert e2.ex3('.env', 'x') is None
    assert e2.ex3('.env', 'HELLO') == 'Hello World'
    assert e2.ex3('.env', 'WORLD') == 'Mars'

def test_e2_exercise_4():
    assert e2.ex4('.env2', 'HELLO') == 'Hello World2'
    assert e2.ex4('.env2', 'WORLD') == 'Mars'
    assert e2.ex4('.env2', 'x') is None
    assert e2.ex4('.env', 'x') is None
    assert e2.ex4('.env', 'HELLO') == 'Hello World'
    assert e2.ex4('.env', 'WORLD') is None