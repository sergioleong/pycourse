import pytest
from os import path, listdir
import json
import e6

@pytest.fixture
def dummy_url():
    return "https://localhost/"

@pytest.fixture
def ok_response():
    return {"status":"ok","message":"All good!"}

@pytest.fixture
def error_response():
    return {"status":"error","message":"Something went wrong!"}

def test_e6_exercise_1(dummy_url, ok_response, error_response, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = 'OK'
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    assert e6.ex1(dummy_url) == 'OK'

def test_e6_exercise_2(dummy_url, ok_response, error_response, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = ok_response
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    assert  e6.ex2(dummy_url) == ok_response
    
def test_e6_exercise_3(dummy_url, ok_response, error_response, mocker):
    mock_response = mocker.Mock()
    mocker.patch('requests.post', return_value=mock_response)
    mock_response.raise_for_status.return_value = None

    mock_response.status_code = 200
    mock_response.json.return_value = ok_response
    assert  e6.ex3(dummy_url, ok_response) == (True, ok_response['message'])

    mock_response.status_code = 400
    mock_response.json.return_value = error_response
    assert  e6.ex3(dummy_url, error_response) == (False, error_response['message'])
