from __future__ import annotations

import json
import logging
import os
from typing import TypedDict

import discord


class Config(TypedDict):
    discord_token: str
    guild_id: int
    channel_id: int
    add_role_message_id: int
    remove_role_message_id: int
    emoji_to_role_id: dict[str, int]


class ReactionToRoleClient(discord.Client):
    def __init__(
        self,
        *args,
        guild_id: int,
        channel_id: int,
        emoji_to_role_id: dict[str, int],
        add_role_message_id: int | None = None,
        remove_role_message_id: int | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.add_role_message_id = add_role_message_id
        self.remove_role_message_id = remove_role_message_id
        self.channel_id = channel_id
        self.emoji_to_role_id = emoji_to_role_id
        self.guild_id = guild_id

    async def on_ready(self):
        try:
            # Retrieve guild object
            self.target_guild = self.get_guild(self.guild_id)

            # Retrieve channel object
            channel = self.get_channel(self.channel_id)

            # add role on emoji
            if self.add_role_message_id:
                await self._edit_role_on_emoji(
                    channel, self.add_role_message_id, "add_roles"
                )

            # remove role on emoji
            if self.remove_role_message_id:
                await self._edit_role_on_emoji(
                    channel, self.remove_role_message_id, "remove_roles"
                )
        except Exception as err:
            logging.error(err)
        finally:
            await self.close()

    async def _edit_role_on_emoji(
        self,
        channel: discord.abc.GuildChannel,
        message_id: int,
        operation_method_name: str,
    ) -> None:
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            role_id = self.emoji_to_role_id[reaction.emoji]
            role = self.target_guild.get_role(role_id)
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
    client = ReactionToRoleClient(
        intents=intents,
        channel_id=config["channel_id"],
        add_role_message_id=config["add_role_message_id"],
        remove_role_message_id=config["remove_role_message_id"],
        emoji_to_role_id=config["emoji_to_role_id"],
        guild_id=config["guild_id"],
    )
    client.run(config["discord_token"])
