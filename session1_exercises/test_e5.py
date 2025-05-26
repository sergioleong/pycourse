import pytest
from os import path, listdir
import json
import e5_complete as e5

@pytest.fixture
def json_example():
    with open(path.join(path.dirname(__file__), 'files', 'test.json'), 'r') as f:
        return json.load(f)

def test_e5_exercise_1(json_example):
    assert e5.ex1('test.json') == json_example

    
def test_e5_exercise_2(json_example):
    assert e5.ex2('test.json', 'year') == json_example['year']
    assert e5.ex2('test.json', 'people') == json_example['people']
    assert e5.ex2('test.json', 'month') == None
    
def test_e5_exercise_3(json_example):
    json1 = json_example.copy()
    json1['year'] = 2020
    assert e5.ex3('test.json', 'year', 2020) == json1
    json2 = json_example.copy()
    json2['month'] = 'JAN'
    assert e5.ex3('test.json', 'month', 'JAN') == json2

def test_e5_exercise_4(tmp_path, json_example):
    filename = tmp_path / 'e4_test.json'
    e5.ex4(filename, json_example)
    assert path.exists(filename)
    assert path.isfile(filename)
    with open(filename, 'r') as file:
       new_content = json.load(file)
    assert new_content == json_example