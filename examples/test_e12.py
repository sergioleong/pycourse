import pytest
from examples.e12 import is_even, divide, is_valid_username

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

def test_calculate_failure():
    #This one should fail -- 3 is not even
    assert is_even(3)

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

def test_divide_zero_denominator_error():
    #This one should fail -- division by zero is a ZeroDivisionError/ValueError
    with pytest.raises(TypeError):
        divide(3, 0)

def test_divide_non_integer_arguments_error():
    with pytest.raises(TypeError):
        divide('a', 'b')

def test_divide_aproximate_result():
    assert divide(1, 3) == pytest.approx(0.333333333333)

def test_divide_aproximate_result():
    #This one should fail -- Not enough precision on comparisson
    assert divide(1, 3) == pytest.approx(0.3333)

@pytest.mark.parametrize("a, b, expected", [
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

@pytest.mark.parametrize("a, b, expected", [
    (1,1, 1.001),
    (1,2,0.50001),
    (3,4,0.75001),
    (-1,3,-0.333334),
    (2806, 4,701.502),
    (51.845454, -32.963888888888887, -1.5727),
])
def test_division_multiplecases_fails(a, b, expected):
    """Test divide with various valid inputs."""
    # This test should fail -- incorrect approximation
    assert divide(a,b) == pytest.approx(expected)



@pytest.fixture
def valid_usernames():
    return ['joe25', 'bob99', '_sally_']

@pytest.fixture
def invalid_usernames():
    return ['joe', 'bob', 'sally']

def test_valid_users(valid_usernames):
    for username in valid_usernames:
        assert is_valid_username(username)

def test_invalid_users(invalid_usernames):
    for username in invalid_usernames:
        assert is_valid_username(username)
        
@pytest.mark.parametrize("username", [
    'joe25', 'bob99', '_sally_',
    'joe', 'bob', 'sally'
])
def test_valid_users_params(username, valid_usernames):
    """Test username in valid users list"""
    assert username in valid_usernames
