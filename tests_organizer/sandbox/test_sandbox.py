import functools

import pytest

### Those are fake tests to understand or illustrate the behavior of some pytest functions

@pytest.fixture( params= ['Single value'] )
def one_value(request):
    return request.param

@pytest.fixture( params= ['Tuple value one', 'Tuple value two'] )
def two_values(request):
    return request.param

@pytest.fixture( params= ['Dict value one', 'Dict value two', 'Dict value three'] )
def three_values(request):
    return request.param

def ready_parser_parameters():
    from _pytest.mark import MarkGenerator
    generator = MarkGenerator()
    one_fixture = pytest.lazy_fixture('one_value')
    two_fixture = pytest.lazy_fixture('two_values')
    three_fixture = pytest.lazy_fixture('three_values')
    return generator.parametrize('one, two, three', [(one_fixture, two_fixture, three_fixture)] )

@ready_parser_parameters()
def test_print(one, two, three):
    print one + ' ' + two + ' ' + three


