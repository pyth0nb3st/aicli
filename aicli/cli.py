import click

from aicli.agent import agent


@click.command()
@click.argument("query", nargs=-1)
def cli(query):
    """AI CLI assistant"""
    query_str = " ".join(query)
    # result = agent.run(query_str, display=True, verbose=True)
    result = agent.user_input(query_str)
    click.echo(result)


if __name__ == "__main__":
    cli()
