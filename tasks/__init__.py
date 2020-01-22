from invoke import task


@task
def test(c):
    c.run('pytest')
    c.run('pylint yamiconfig')
