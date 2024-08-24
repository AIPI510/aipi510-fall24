def test_length(d):
    '''checks that only 1 flower is being returned'''
    assert len(d) == 1

def test_type(d):
    '''checks that petal length is decimal value'''
    assert isinstance(d[0], float)