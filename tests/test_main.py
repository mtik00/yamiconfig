import pytest
from yamiconfig import Configuration
from yamiconfig.schema import Schema, SchemaError


@pytest.fixture(scope='session')
def temp_dir(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data')
    return fn


def test_basic(temp_dir):
    p1 = temp_dir.join("config-basic.yaml")
    p1.write('''
test1: 2
test3: 4
    ''')

    c = Configuration(str(p1))

    assert c['test1'] == 2
    assert c['test3'] == 4


def test_user(temp_dir):
    '''Ensure user config files overwrite default'''
    default = temp_dir.join("config-default.yaml")
    default.write('''
test1: 2
test3: 4
    ''')

    user = temp_dir.join("config-user.yaml")
    user.write('''
test3: 5
    ''')

    c = Configuration(
        default_config_file=str(default),
        user_config_files=[str(user)])

    assert c['test1'] == 2
    assert c['test3'] == 5


def test_validate(temp_dir):
    p1 = temp_dir.join("config-basic.yaml")
    p1.write('''
test1: 2
test3: 4
    ''')

    valid = Schema({
        'test1': int,
        'test3': int
    })

    c = Configuration(str(p1), valid_schema=valid)

    assert c['test1'] == 2
    assert c['test3'] == 4


def test_invalid_schema(temp_dir):
    p1 = temp_dir.join("config-basic.yaml")
    p1.write('''
test1: 2
test3: 4
    ''')

    valid = Schema({
        'test1': int,
        'test3': str
    })

    with pytest.raises(SchemaError):
        Configuration(str(p1), valid_schema=valid)


def test_exceptions():
    with pytest.raises(TypeError):
        Configuration()


def main():
    test_basic()


if __name__ == '__main__':
    main()