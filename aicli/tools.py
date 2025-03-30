import subprocess


def run_command(command: str):
    """
    Execute the given command line instruction.

    Args:
        command (str): The command line instruction to be executed.

    Returns:
        str: The standard output result of the command execution.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def install_package(package_name: str):
    """
    Install the specified Python package using pip.

    Args:
        package_name (str): The name of the package to be installed.

    Returns:
        str: The standard output result of the installation process.
    """
    command = f'pip install {package_name}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def web_search(
    query: str,
    topic="general",
    search_depth="basic",
    max_results=5,
    time_range="day"
):
    """
    Perform a web search using the Tavily API.

    This function uses the TavilyClient to search the web based on the provided parameters.
    It returns the search results as obtained from the API.

    Args:
        query (str): The search query to be used for the web search.
        topic (str, optional): The topic of the search. Defaults to "general", can also be "news", "finance".
        search_depth (str, optional): The depth of the search. Can be "basic" or "advanced". Defaults to "basic".
        max_results (int, optional): The maximum number of search results to return. Defaults to 5.
        time_range (str, optional): The time range for the search results. Can be None, "day", "week", "month", "year". Defaults to "day".

    Returns:
        dict: The response from the Tavily API containing the search results.

        {
            "query": str,
            "follow_up_questions": null,
            "answer": null,
            "images": [],
            "results": [
                {
                "url": str,
                "title": str,
                "content": str,
                "score": float,
                "raw_content": null
                },
                ...
            ],
            "response_time": float
        }

    Raises:
        Exception: If there's an error in the API call or if the API key is not set correctly.
    """
    import os
    from tavily import TavilyClient
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(
        query=query,
        topic=topic,
        search_depth=search_depth,
        max_results=max_results,
        time_range=time_range
    )
    return response