from __future__ import annotations

import json
import logging
import os
from typing import TypedDict

import discord


class MessageMetadata(TypedDict):
    """The metadata of the discord message that memberes should reaction on"""

    message_id: int
    operation: str
    emoji_to_role_id: dict[str, int]


class ChannelMetadata(TypedDict):
    """The metadata of discord channel that contains the message to react"""

    channel_id: int
    messages: list[MessageMetadata]


class GuildMetadata(TypedDict):
    """The metadata of discord guild that contains the channel to react"""

    guild_id: int
    channels: list[ChannelMetadata]


class Config(TypedDict):
    """The configuration dictionary to run the ReactionToRoleClient"""

    discord_token: str
    guilds: list[GuildMetadata]


class ReactionToRoleClient(discord.Client):
    def __init__(
        self,
        *args,
        guilds: list[GuildMetadata],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.reaction_guilds = guilds

    async def on_ready(self):
        try:
            for guild_metadata in self.reaction_guilds:
                # Retrieve guild object
                guild = self.get_guild(guild_metadata["guild_id"])
                for channel_metadata in guild_metadata["channels"]:
                    # Retrieve channel object
                    channel = self.get_channel(channel_metadata["channel_id"])

                    for message_metadata in channel_metadata["messages"]:
                        await self._edit_role_on_emoji(
                            guild,
                            channel,
                            message_metadata["message_id"],
                            message_metadata["operation"],
                            message_metadata["emoji_to_role_id"],
                        )

        except Exception as err:
            logging.error(err)
        finally:
            await self.close()

    async def _edit_role_on_emoji(
        self,
        guild: discord.Guild,
        channel: discord.TextChannel,
        message_id: int,
        operation_method_name: str,
        emoji_to_role_id: dict[str, int],
    ) -> None:
        if operation_method_name not in ("add_roles", "remove_roles"):
            logging.error(f"{operation_method_name} is not supported")
            return

        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            try:
                role_id = emoji_to_role_id[str(reaction.emoji)]
            except KeyError:
                # irreverent emoji
                continue

            role = guild.get_role(role_id)
            if not role:
                # Make sure the role still exists and is valid.
                return

            async for user in reaction.users():
                if user == self.user:
                    continue

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
