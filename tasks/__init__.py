from invoke import task


@task
def test(c):
    c.run('pytest')

    print('---- pylint:')
    c.run('pylint yamiconfig')

    print('---- mypy:')
    c.run('mypy yamiconfig')