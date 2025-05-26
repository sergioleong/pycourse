import pytest
from os import path, listdir
import e4_complete as e4

@pytest.fixture
def files_path():
    files_dir = path.join(path.dirname(__file__), 'files')
    return [path.join(files_dir, f) for f in listdir(files_dir) if path.isfile(path.join(files_dir, f))]

@pytest.fixture
def txt_example():
    with open(path.join(path.dirname(__file__), 'files', 'test.txt'), 'r') as f:
        return f.read()

@pytest.fixture
def txt2_example():
    with open(path.join(path.dirname(__file__), 'files', 'test2.txt'), 'r') as f:
        return f.read()

def test_e4_exercise_1(files_path):
    assert set(e4.ex1()) == set(files_path)

def test_e4_exercise_2(files_path):
    assert set(e4.ex2()) == set([f for f in files_path if f.endswith('.json')])

def test_e4_exercise_3(files_path):
    assert set(e4.ex3()) == set([f for f in files_path if f.endswith('.json') or f.endswith('.txt')])

def test_e4_exercise_4(txt_example):
    assert e4.ex4('test.txt') == txt_example
    assert e4.ex4('test_false.txt') is None

def test_e4_exercise_5(txt_example):
    assert e4.ex5('test.txt', '') == txt_example.format(name='')
    assert e4.ex5('test.txt', 'John') == txt_example.format(name='John')
    assert e4.ex5('test_false.txt', 'John') is None
    assert e4.ex5('test.txt', 'Jane') == txt_example.format(name='Jane')   
    with pytest.raises(KeyError):
        e4.ex5('test2.txt', 'John')

def test_e4_exercise_6(txt_example, txt2_example):
    assert e4.ex6('test.txt', {'name': 'John'}) == txt_example.format(name='John')
    assert e4.ex6('test_false.txt', {'name': 'John'}) is None
    assert e4.ex6('test.txt', {'name': 'Jane'}) == txt_example.format(name='Jane')
    assert e4.ex6('test.txt', {'name': 'Jane', 'age': 30}) == txt_example.format(name='Jane')
    assert e4.ex6('test2.txt', {'name': 'Jane', 'age': 30}) == txt2_example.format(name='Jane', age=30  )
    with pytest.raises(KeyError):
        e4.ex6('test2.txt', {'name': 'Jane'})


def test_e4_exercise_7(tmp_path):
    filename = tmp_path / 'e7_test.txt'
    content = 'Hello, world!'
    e4.ex7(filename, content)
    assert path.exists(filename)
    assert path.isfile(filename)
    with open(filename, 'r') as file:
       new_content= file.read()
    assert new_content == content

    content = 'Hello, world! Now with extra content!!'
    e4.ex7(filename, content)
    assert path.exists(filename)
    assert path.isfile(filename)
    with open(filename, 'r') as file:
       new_content= file.read()
    assert new_content == content
