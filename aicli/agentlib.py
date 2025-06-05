import os
from functools import partial
from pathlib import Path

from GeneralAgent import Agent

from aicli.conf import settings
from aicli.role import SYSTEM_PROMPT

HOME = Path.home().expanduser()
WORKSPACE_ROOT = HOME / ".workspaces"


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
        kwargs["output_callback"] = output_callback_factory(output_callback_filename)

    if functions:
        kwargs["functions"] = functions

    if workspace:
        kwargs["workspace"] = workspace

    return Agent(**kwargs)


def setup_agent(
    token_limit=16000, model="gpt-4o-mini", no_context=False, functions=None
):
    """Return a GeneralAgent instance configured with local settings.

    Parameters
    ----------
    token_limit : int, optional
        Maximum number of tokens that the agent can keep in context.
    model : str, optional
        Name of the model to use when interacting with the API.
    no_context : bool, optional
        When ``True`` the agent does not use a workspace for context.
    functions : list, optional
        Additional functions that can be called by the agent.

    Notes
    -----
    The API token and base URL are read from the ``API_KEY`` and
    ``BASE_URL`` environment variables.
    """
    settings.output_callback_path.parent.mkdir(exist_ok=True, parents=True)
    workspace = None if no_context else settings.workspace_path.as_posix()
    return get_general_agent(
        model=model,
        token_limit=token_limit,
        role=SYSTEM_PROMPT,
        functions=functions,
        output_callback_filename=settings.output_callback_path.as_posix(),
        workspace=workspace,
    )
