# AICLI

An AI-based command-line assistant tool.

## Installation

### Install with PYPI

```sh
pip install aicli-gent
```

### Install with Source

1. Clone this repository:

```sh
git clone https://github.com/callmexss/aicli.git
cd aicli
```

2. Install dependencies:

```sh
pip install -e .
```

3. Set environment variables:

Copy the `.env.example` file to `.env` and fill in the necessary environment variables:
```sh
cp .env.example .env
```
Then edit the `.env` file and fill in your API key and other settings.

## Usage

After installation, you can directly use the `aicli` command in the command line:

```sh
aicli query
```

For example:

```sh
aicli list files in current directory
aicli "help me install nvm"
```
