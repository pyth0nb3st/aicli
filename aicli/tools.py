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
