import functools

import pytest

### Those are fake tests to understand or illustrate the behavior of some pytest functions
# These tests do all the same thing: they take three set of parameters and combine them in all the existing combination (aka: 6)
# The decorator present the advantage of being reusable
# The direct fixture use is the most simple one

@pytest.fixture( params= ['Single value'] )
def one_value(request):
    return request.param

@pytest.fixture( params= ['Tuple value one', 'Tuple value two'] )
def two_values(request):
    return request.param

@pytest.fixture( params= ['Dict value one', 'Dict value two', 'Dict value three'] )
def three_values(request):
    return request.param

def parameters_as_decorator():
    from _pytest.mark import MarkGenerator
    generator = MarkGenerator()
    one_fixture = pytest.lazy_fixture('one_value')
    two_fixture = pytest.lazy_fixture('two_values')
    three_fixture = pytest.lazy_fixture('three_values')
    return generator.parametrize('one, two, three', [(one_fixture, two_fixture, three_fixture)] )


@pytest.mark.parametrize('one, two, three', [(pytest.lazy_fixture('one_value'), pytest.lazy_fixture('two_values'), pytest.lazy_fixture('three_values'))])
def test_print(one, two, three):
    # Will run 6 times
    print one + ' ' + two + ' ' + three

@pytest.mark.parametrize('one', [pytest.lazy_fixture('one_value')])
@pytest.mark.parametrize('two', [pytest.lazy_fixture('two_values')])
@pytest.mark.parametrize('three', [pytest.lazy_fixture('three_values')])
def test_print_stack_parameters(one, two, three):
    # Will run 6 times
    print one + ' ' + two + ' ' + three

@parameters_as_decorator()
def test_print_decorator(one, two, three):
    # Will run 6 times
    print one + ' ' + two + ' ' + three

def test_print_fixtures(one_value, two_values, three_values):
    # Will run 6 times
    print one_value + ' ' + two_values + ' ' + three_values