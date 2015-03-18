from pyshape import pyshape



def test_read_yaml():
    assert isinstance(pyshape.template_fields('data/valid_shape.yml'), list)


def test_read_config():
    pass 
