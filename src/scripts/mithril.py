import click


@click.group()
def mithril():
    pass


@mithril.command()
def helloworld():
    click.echo('Hello World')
