import pytest
import e1


def test_e1_exercise_1(capsys):
    e1.ex1()
    captured = capsys.readouterr()
    assert "Hello, world!\n" == captured.out

def test_e1_exercise_2(capsys):
    e1.ex2("Bob")
    captured = capsys.readouterr()
    assert "Hello, Bob!\n" == captured.out

    e1.ex2("John")
    captured = capsys.readouterr()
    assert "Hello, John!\n" == captured.out

def test_e1_exercise_3():
    assert e1.ex3(1, 2) == 3
    assert e1.ex3(8, 2) == 10
    assert e1.ex3(-4, 2) == -2
    assert e1.ex3(1, -2) == -1

def test_e1_exercise_4():
    assert e1.ex4()  == [1,2,3,4]


def test_e1_exercise_5():
    assert e1.ex5("Bob") is True
    assert e1.ex5("") is False
    assert e1.ex5(5) is False

def test_e1_exercise_6():
    assert e1.ex6(-2) == 0
    assert e1.ex6(0) == 1
    assert e1.ex6(1) == 1
    assert e1.ex6(2) == 2
    assert e1.ex6(3) == 3
    assert e1.ex6(4) == 5
    assert e1.ex6(5) == 8
    assert e1.ex6(6) == 13
    assert e1.ex6(100) == 573147844013817084101    

def test_e1_exercise_7():
    l = [1,2,3]
    e1.ex7(l, 4)
    assert l == [1,2,3,4]
    e1.ex7(l, "Bob")
    assert "Bob" in l

def test_e1_exercise_8():
    assert e1.ex8([]) is None
    assert e1.ex8([0]) == 0
    assert e1.ex8([2]) == 2
    assert e1.ex8([3,4]) == 3
    assert e1.ex8([5,6,7]) == 6
    assert e1.ex8([9,8,7,6,5,4,3,2,1]) == 5
    assert e1.ex8(list(range(5000))) == 2499

def test_e1_exercise_9():
    assert e1.ex9([1]) == [3]
    assert e1.ex9([1,2,3]) == [3,6,9]
    assert e1.ex9([]) == []
    assert e1.ex9(list(range(10))) == list(range(0,30,3))

def test_e1_exercise_10():
    assert e1.ex10([1,"a"]) == [3]
    assert e1.ex10([1,2,"a",3]) == [3,6,9]
    assert e1.ex10([]) == []
    assert e1.ex10(list(range(10))+["a"]) == list(range(0,30,3))

def test_e1_exercise_11():
    assert e1.ex11([1,"a"], lambda x: x*3) == [3]
    assert e1.ex11([1,2,"a",3], lambda x: x*3) == [3,6,9]
    assert e1.ex11([1,"a"], lambda x: x*5) == [5]
    assert e1.ex11([1,2,"a",3], lambda x: x*5) == [5,10,15]
    assert e1.ex11([], lambda x: x*3) == []
    assert e1.ex11(list(range(10))+["a"], lambda x: x*2) == list(range(0,20,2))
