[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Github Actions](https://github.com/Lee-W/discord_reaction_to_role_bot/actions/workflows/python-check.yaml/badge.svg)](https://github.com/Lee-W/discord_reaction_to_role_bot/actions/workflows/python-check.yaml)

# Discord reaction to role bot

Discord bot that can edit members' roles based on their reactions to a message

The bot is designed to exit once all operations are completed, allowing us to run it like a terminal command rather than keeping a bot server running.

## Getting Started

### Prerequisites
* [Python](https://www.python.org/downloads/)

### Configuration

This tool can retrieve configuration settings from either an environment variable called "CONFIG_JSON" or a configuration file named "config.json".

* from the environment variable

```sh
export CONFIG_JSON='
{
    "discord_token": "<Your token>",
    "guilds": [
        {
            "guild_id": <Your guild ID>,
            "channels": [
                {
                    "channel_id": <Your channel ID>,,
                    "messages": [
                        {
                            "message_id": <Your message ID>,
                            "operation": "add_roles",
                            "emoji_to_role_id": {
                                "💯": <Role ID>,
                                "👍": <Role ID>
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

'
```

* from "config.json"

```json
{
    "discord_token": "<Your token>",
    "guilds": [
        {
            "guild_id": <Your guild ID>,
            "channels": [
                {
                    "channel_id": <Your channel ID>,,
                    "messages": [
                        {
                            "message_id": <Your message ID>,
                            "operation": "add_roles",
                            "emoji_to_role_id": {
                                "💯": <Role ID>,
                                "👍": <Role ID>
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

```

#### Columns
* `discord_token` (str): discord token for the bot
* `guilds` (list[GuildMetadata]): metadata of the guilds that contain the message for members to react to
    * `guild_id` (int): discord guild id
    * `channel` (list[ChannelMetadata]): metadata of the channels that contain the message for members to react to
        * `channel_id` (int): discord channel_id
        * `messages`: (list[MessageMetadata]): metadata of the messages for members to react to
            * `message_id` (int): discord message id
            * `operation` (str): currently only supports `add_roles`, `remove_roles`
            * `emoji_to_role_id` (dict[str, int]): the mapping from emoji to the id of the role to operate

### Usage

```sh
# Step 1: Install required dependency
pipenv install

# Step 2: Set up configuration as the previous section describe

# Step 3: Run the bot
pipenv run python bot/bot.py
```

## Contributing
See [Contributing](contributing.md)

## Authors
Wei Lee <weilee.rx@gmail.com>


Created from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/1.7.0) version 1.7.0
