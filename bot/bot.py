from __future__ import annotations

import json
import logging
import os
from typing import TypedDict

import discord


class Message(TypedDict):
    message_id: int
    operation: str
    emoji_to_role_id: dict[str, int]


class Channel(TypedDict):
    channel_id: int
    messages: list[Message]


class Guild(TypedDict):
    guild_id: int
    channels: list[Channel]


class Config(TypedDict):
    discord_token: str
    guilds: list[Guild]


class ReactionToRoleClient(discord.Client):
    def __init__(
        self,
        *args,
        guilds: list[Guild],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.target_guilds = guilds

    async def on_ready(self):
        try:
            for guild in self.target_guilds:
                # Retrieve guild object
                guild_obj = self.get_guild(guild["guild_id"])
                for channel in guild["channels"]:
                    # Retrieve channel object
                    channel_obj = self.get_channel(channel["channel_id"])

                    for message in channel["messages"]:
                        await self._edit_role_on_emoji(
                            guild_obj,
                            channel_obj,
                            message["message_id"],
                            message["operation"],
                            message["emoji_to_role_id"],
                        )

        except Exception as err:
            logging.error(err)
        finally:
            await self.close()

    async def _edit_role_on_emoji(
        self,
        guild: discord.Guild,
        channel: discord.abc.GuildChannel,
        message_id: int,
        operation_method_name: str,
        emoji_to_role_id: dict[str, int],
    ) -> None:
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            role_id = emoji_to_role_id[reaction.emoji]
            role = guild.get_role(role_id)
            if not role:
                # Make sure the role still exists and is valid.
                return

            async for user in reaction.users():
                try:
                    operation = getattr(user, operation_method_name)
                    await operation(role)
                except discord.HTTPException as err:
                    logging.error(err)
                else:
                    await message.remove_reaction(reaction.emoji, user)

        for emoji in emoji_to_role_id:
            await message.add_reaction(emoji)


def load_config(config_file_name: str = "config.json") -> Config:
    raw_config_string = os.environ.get("CONFIG_JSON")
    if not raw_config_string:
        with open(config_file_name, "r") as input_file:
            raw_config_string = input_file.read()
    return json.loads(raw_config_string)


if __name__ == "__main__":
    config: Config = load_config()

    intents = discord.Intents.default()
    intents.members = True
    client = ReactionToRoleClient(intents=intents, guilds=config["guilds"])
    client.run(config["discord_token"])
