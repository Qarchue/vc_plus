import asyncio
import random
import typing
from datetime import datetime, time, timedelta

import discord
import enkanetwork
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks

from utility import SlashCommandLogger, config


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.presence_string: list[str] = ["測試"]
        self.change_presence.start()


    async def cog_unload(self) -> None:
        self.change_presence.cancel()




    # /status指令：顯示機器人相關狀態
    @commands.has_permissions(administrator=True)
    @app_commands.command(name="status", description="顯示機器人狀態")
    @app_commands.choices(
        option=[
            Choice(name="機器人連線延遲", value="BOT_LATENCY"),
            Choice(name="已連接伺服器數量", value="SERVER_COUNT"),
            Choice(name="已連接伺服器名稱", value="SERVER_NAMES"),
        ]
    )
    @SlashCommandLogger
    async def slash_status(self, interaction: discord.Interaction, option: str):
        match option:
            case "BOT_LATENCY":
                await interaction.response.send_message(f"延遲：{round(self.bot.latency*1000)} 毫秒")
            case "SERVER_COUNT":
                await interaction.response.send_message(f"已連接 {len(self.bot.guilds)} 個伺服器")
            case "SERVER_NAMES":
                await interaction.response.defer()
                names = [guild.name for guild in self.bot.guilds]
                for i in range(0, len(self.bot.guilds), 100):
                    msg = "、".join(names[i : i + 100])
                    embed = discord.Embed(title=f"已連接伺服器名稱({i + 1})", description=msg)
                    await interaction.followup.send(embed=embed)
    

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="system", description="使用系統命令(更改機器人狀態、執行任務...)")
    @app_commands.rename(option="選項", param="參數")
    @app_commands.choices(
        option=[
            Choice(name="自訂機器人狀態", value="CHANGE_PRESENCE"),
        ]
    )
    @SlashCommandLogger
    async def slash_system(
        self, interaction: discord.Interaction, option: str, param: typing.Optional[str] = None
    ):
        await interaction.response.defer()
        match option:
            case "CHANGE_PRESENCE":  # 更改機器人狀態
                if param is not None:
                    self.presence_string = param.split(",")
                    await interaction.edit_original_response(
                        content=f"Presence list已變更為：{self.presence_string}"
                    )





    # ======== Loop Task ========

    # 每一定時間更改機器人狀態
    @tasks.loop(minutes=1)
    async def change_presence(self):
        length = len(self.presence_string)
        n = random.randint(0, length)
        if n < length:
            await self.bot.change_presence(activity=discord.Game(self.presence_string[n]))
        elif n == length:
            await self.bot.change_presence(activity=discord.Game(f"{len(self.bot.guilds)} 個伺服器"))

    @change_presence.before_loop
    async def before_change_presence(self):
        await self.bot.wait_until_ready()



async def setup(client: commands.Bot):
    await client.add_cog(Admin(client), guild=discord.Object(id=config.main_server_id))