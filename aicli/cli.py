import os
import time
from functools import partial

import click
import rich
from GeneralAgent import Agent

from aicli.conf import settings
from aicli.role import SYSTEM_PROMPT
from aicli.tools import run_command, install_package


def output_callback(token: str, filename: str, sep: str, print_token: bool):
    token = token or sep
    with open(filename, "a") as f:
        f.write(token)
    if print_token:
        print(token, end="", flush=True)


def output_callback_factory(filename: str, sep="\n=======\n", print_token=True):
    return partial(output_callback, filename=filename, sep=sep, print_token=print_token)


def get_general_agent(
    token="",
    base_url="",
    role="",
    token_limit=16000,
    model="gpt-4o-mini",
    functions=[],
    output_callback_filename="",
    workspace=None,
):
    kwargs = {
        "model": model,
        "token_limit": token_limit,
        "api_key": token or os.getenv("API_KEY"),
        "base_url": base_url or os.getenv("BASE_URL"),
    }

    if role:
        kwargs["role"] = role

    if output_callback_filename:
        kwargs["output_callback"] = output_callback_factory(
            output_callback_filename
        )

    if functions:
        kwargs["functions"] = functions

    if workspace:
        kwargs["workspace"] = workspace

    return Agent(**kwargs)


def setup_agent(token_limit=16000, model="gpt-4o-mini", no_context=False):
    """Create and return a general agent with the given token."""
    settings.output_callback_path.parent.mkdir(exist_ok=True, parents=True)
    workspace = None if no_context else settings.workspace_path.as_posix()
    return get_general_agent(
        model=model,
        token_limit=token_limit,
        role=SYSTEM_PROMPT,
        functions=[run_command, install_package],
        output_callback_filename=settings.output_callback_path.as_posix(),
        workspace=workspace,
    )


@click.command()
@click.argument("query", required=False)
@click.option("-m", "--model", default="grok-2-1212")
@click.option("-l", "--token-limit", default=64000)
@click.option("-a", "--archive", is_flag=True)
@click.option("-ao", "--archive-output", is_flag=True)
@click.option(
    "-nc",
    "--no-context",
    is_flag=True,
    help="Single question mode without multi-turn context",
)
@click.option(
    "-sp",
    "--show-path",
    is_flag=True,
    help="Print all the folders for the current workspace",
)
def cli(query, model, token_limit, archive, archive_output, no_context, show_path):
    """CLI command to handle user query and interact with the agent."""
    if show_path:
        if settings.output_callback_path.exists():
            click.echo(f"Chat history path: {settings.output_callback_path}")
        if settings.workspace_path.exists():
            click.echo(f"Workspace path: {settings.output_callback_path}")
        archive_path = settings.workspace_path.parent / "archive/"
        if archive_path.exists():
            for file in archive_path.iterdir():
                if settings.workspace_path.name in file.as_posix():
                    click.echo(f"Archived path: {file}")
        return

    if archive:
        try:
            name = settings.workspace_path.name
            readable_time = int(time.time())
            target_path = (
                settings.workspace_path.parent / f"archive/{name}_{readable_time}"
            )
            target_path.mkdir(exist_ok=True, parents=True)
            settings.workspace_path.rename(target_path)
            click.echo(f"move {settings.workspace_path} to {target_path}")
        except Exception as err:
            click.echo(f"error occurred: {err}")


    if archive_output:
        try:
            name = settings.output_callback_path.stem
            readable_time = int(time.time())
            target_path = (
                settings.output_callback_path.parent
                / f"archive/{name}_{readable_time}.md"
            )
            target_path.parent.mkdir(exist_ok=True, parents=True)
            settings.output_callback_path.rename(target_path)
            click.echo(f"move {settings.output_callback_path} to {target_path}")
        except Exception as err:
            click.echo(f"error occurred: {err}")

    if archive or archive_output:
        return

    if not query:
        print(">>> :")
        query = input()

    agent: Agent = setup_agent(
        token_limit=token_limit, model=model, no_context=no_context
    )

    result = agent.user_input(query)

    print("\n" * 3)
    if len(str(result).split()) < 4000:
        rich.print(result)
    else:
        rich.print(result[:4000])


if __name__ == "__main__":
    cli()
