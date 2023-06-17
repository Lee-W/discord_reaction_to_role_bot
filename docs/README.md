[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Github Actions](https://github.com/Lee-W/discord_reaction_to_role_bot/actions/workflows/python-check.yaml/badge.svg)](https://github.com/Lee-W/discord_reaction_to_role_bot/actions/workflows/python-check.yaml)

# Discord reaction to role bot

Discord bot for editing members' roles based on their reactions to a given message

## Getting Started

### Prerequisites
* [Python](https://www.python.org/downloads/)

### Configuration

This bot takes configuration from either environment variable "CONFIG_JSON" of configuration file "config.json".

* from the environment variable

```sh
export CONFIG_JSON='
{
    "discord_token": "<Your token>",
    "server_name": "<Your server name>",
    "channel_id": 123,
    "add_role_message_id": 456,
    "remove_role_message_id": 789,
    "emoji_to_role_id": {
        "💯": 321,
        "👍": 654
    }
}
'
```

* from "config.json"

```json
{
    "discord_token": "<Your token>",
    "server_name": "<Your server name>",
    "channel_id": 123,
    "add_role_message_id": 456,
    "remove_role_message_id": 789,
    "emoji_to_role_id": {
        "💯": 321,
        "👍": 654
    }
}
```

#### Columns
* discord_token: discord token for the bot
    * type: string
* server_name: discord server name. If not given, we'll use the first server found.
    * type: string (optional)
* channel_id: discord channel id
    * type: integer
* add_role_message_id: the id of the message that the members react to for retrieving new roles. if not given, then we'll not add roles to members
    * type: integer (optional)
* remove_role_message_id: the id of the message that the members react to for removing their existing roles. if not given, then we'll not remove roles from members
    * type: integer (optional)
* emoji_to_role_id
    * type: dict[str, int]




### Usage

```sh
pipenv install
pipenv run python bot/bot.py
```

## Contributing
See [Contributing](contributing.md)

## Authors
Wei Lee <weilee.rx@gmail.com>


Created from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/1.6.0) version 1.6.0
