import pytest
import os
from examples.e12 import is_even, divide, is_valid_username, getUrl, create_file, read_file, hello


def test_calculate_even_number_true():
    assert is_even(2)
    assert is_even(2806)
    assert is_even(-4)

def test_calculate_odd_number_false():
    assert not is_even(1)
    assert not is_even(2805)
    assert not is_even(-5)

def test_calculate_string_error():
    with pytest.raises(TypeError):
        is_even('hello')

def test_calculate_float_error():
    with pytest.raises(TypeError):
        is_even(1.0)
    with pytest.raises(TypeError):
        is_even(1.1)

def test_calculate_zero_error():
    with pytest.raises(ValueError):
        is_even(0)

def test_approx():
    assert 1/3 == pytest.approx(0.33333333333333)

@pytest.mark.xfail(reason="This test is made upt to fail")
def test_calculate_failure():
    #This one should fail -- 3 is not even
    assert is_even(3)
@pytest.mark.xfail(reason="This marked to fail but wont")
def test_calculate_false_failure():
    assert is_even(2)
    
@pytest.mark.skip(reason="We want to skip this test")
def test_skip():
    assert False

@pytest.mark.skipif(os.getenv("TEST_VAR", '') == '', reason="Does not run if TEST_VAR is not set")
def test_env_var():
    assert os.getenv("TEST_VAR", None) == "OK"

def test_divide_positive_numbers():
    result = divide(4, 2)
    assert result == 2

def test_divide_negative_numbers():
    result = divide(-10, -5)
    assert result == 2  

def test_divide_zero_denominator_error():
    with pytest.raises(ValueError) :
        divide(3, 0)
        
def test_divide_zero_denominator_error():
    with pytest.raises(ZeroDivisionError):
        divide(3, 0)

@pytest.mark.xfail(reason="This test is made upt to fail")
def test_divide_zero_denominator_error():
    #This one should fail -- division by zero is a ZeroDivisionError/ValueError
    with pytest.raises(TypeError):
        divide(3, 0)

def test_divide_non_integer_arguments_error():
    with pytest.raises(TypeError):
        divide('a', 'b')

def test_divide_aproximate_result():
    assert divide(1, 3) == pytest.approx(0.333333333333)

@pytest.mark.xfail(reason="This test is made upt to fail")
def test_divide_aproximate_result():
    #This one should fail -- Not enough precision on comparisson
    assert divide(1, 3) == pytest.approx(0.3333)

#@pytest.mark.parametrize("a, b, expected", [
@pytest.mark.parametrize(["a", "b", "expected"], [
    (1,1, 1),
    (1,2,0.5),
    (3,4,0.75),
    (-1,3,-0.333333333333),
    (2806, 4,701.5),
    (51.845454, -32.963888888888887, -1.572795436083256),
])
def test_division_multiplecases(a, b, expected):
    """Test divide with various valid inputs."""
    assert divide(a,b) == pytest.approx(expected)


@pytest.mark.parametrize(["a", "b", "expected"], [
    (1,1, 1.001),
    (1,2,0.50001),
    (3,4,0.75001),
    (-1,3,-0.333334),
    (2806, 4,701.502),
    (51.845454, -32.963888888888887, -1.5727),
])
@pytest.mark.xfail(reason="This test is made upt to fail")
def test_division_multiplecases_fails(a, b, expected):
    """Test divide with various valid inputs."""
    # This test should fail -- incorrect approximation
    assert divide(a,b) == pytest.approx(expected)



@pytest.fixture
def valid_usernames():
    return ['joe_25', 'bob-99', '_sally_']

@pytest.fixture
def invalid_usernames():
    return ['joe', 'bob', 'sally']

def test_valid_users(valid_usernames):
    for username in valid_usernames:
        assert is_valid_username(username) == True


def test_invalid_users(invalid_usernames):
    for username in invalid_usernames:
        assert is_valid_username(username) == False
        
@pytest.mark.parametrize("username", [
    'joe_25', 'bob-99', '_sally_'
])
def test_valid_users_params(username, valid_usernames):
    """Test username in valid users list"""
    assert username in valid_usernames
    
@pytest.mark.parametrize("username", [
    'joe', 'bob', 'sally'
])
@pytest.mark.xfail(reason="This test is made upt to fail")
def test_valid_users_params_fail(username, valid_usernames):
    """Test username in valid users list"""
    assert username in valid_usernames

def test_hello(capsys):
    hello("world")
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"
    assert captured.err == ""


def test_file(tmp_path):
    filename = tmp_path / 'test.txt'
    content = 'Hello, world!'
    create_file(filename, content)
    assert os.path.exists(filename)
    assert os.path.isfile(filename)
    new_content = read_file(filename)
    assert new_content == content


    
def test_url_online():
    url = 'https://jsonplaceholder.typicode.com/todos/1'
    response = getUrl(url)
    assert response['userId'] == 1

def test_url_mock(mocker):
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"userId": 2, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    url = 'https://jsonplaceholder.typicode.com/todos/1'
    response = getUrl(url)
    assert response['userId'] == 2

@pytest.mark.xfail(reason="This test is made upt to fail")
def test_url_mock_fail(mocker):
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"userId": 2, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    url = 'https://jsonplaceholder.typicode.com/todos/1'
    response = getUrl(url)
    assert response['userId'] == 1

