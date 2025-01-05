import asyncio
import random
import typing
from datetime import datetime, time, timedelta

import sqlalchemy
import discord
import enkanetwork
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
from discord import permissions
from database import Database, User, Server, UserServerData, ServerConfiguration, VoiceChannel, BlackList

from utility import SlashCommandLogger, LOG, config


from sqlalchemy.sql._typing import ColumnExpressionArgument


class VoiceCreatorCog(commands.Cog, name="語音創建器"):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        await self.voice_channel_check()



    async def voice_channel_check(self, whereclause: ColumnExpressionArgument[bool] | None = None):
        """遍歷所有在表內的語音頻道，並偵測是否達到刪除的條件，可指定頻道，如果條件為空則遍歷所有頻道"""
        try:
            voice_channel_datas = await Database.select_all(VoiceChannel, whereclause=whereclause)
            for voice_channel_data in voice_channel_datas:
                try:
                
                    guild = self.bot.get_guild(voice_channel_data.server_id)
                    LOG.Debug(f"取得伺服器{LOG.Server(guild)}")
                    
                    owner = guild.get_member(voice_channel_data.discord_id)
                    LOG.Debug(f"取得頻道擁有者{LOG.User(owner)}")
                    
                    voice_channel = guild.get_channel(voice_channel_data.channel_id)
                    LOG.Debug(f"取得語音頻道{LOG.Channel(voice_channel)}")

                    userserverdata = await Database.select_one(
                        UserServerData, 
                        sqlalchemy.and_(
                            UserServerData.discord_id.is_(voice_channel_data.discord_id), 
                            UserServerData.server_id.is_(voice_channel_data.server_id)
                        )
                    )

                    delete_rule = userserverdata.delete_rule
                    LOG.Debug(f"取得頻道刪除條件")

                except AttributeError:
                    LOG.Error(f"遍歷錯誤，直接刪除表")
                    await Database.delete_instance(voice_channel_data)
                
                else:
                    result = await self.voice_state_check(
                        guild=guild, 
                        owner=owner, 
                        voice_channel=voice_channel,
                        delete_rule=delete_rule
                    )

                    if result:
                        LOG.Debug(f"頻道符合刪除條件，刪除中...")
                        await voice_channel.delete(reason="符合設定之刪除條件")
                        userserverdata.voice_name = voice_channel.name

                        await Database.delete_instance(voice_channel_data)
                        await Database.insert_or_replace(userserverdata)

        except Exception as e:
            LOG.Except(f"{e}")



    async def voice_state_check(
            self, 
            guild: discord.Guild,
            owner: discord.Member,
            voice_channel: discord.VoiceChannel,
            delete_rule: int,
        ):
        try:
            # 0 語音沒人刪除
            # 1 擁有者不再該語音刪除
            # 2 擁有者不再任何語音刪除
            # 3 語音沒人且擁有者不在其他頻道刪除
            match delete_rule:
                case 0:
                    if len(voice_channel.members) == 0:
                        return True
                case 1:
                    if owner.voice is None:
                        return True
                    elif owner.voice.channel != voice_channel:
                        return True
                case 2:
                    if owner.voice is None:
                        return True
                    elif owner.voice.channel.guild != guild:
                        return True
                case 3:
                    if len(voice_channel.members) == 0:               
                        if owner.voice is None:
                            return True
                        elif owner.voice.channel.guild != guild:
                            return True

            return False
        except Exception as e:
            LOG.Error(f"偵測部分出錯{e}")





    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        
        

        try:
            guild = member.guild
            server_config = await Database.select_one(ServerConfiguration, ServerConfiguration.server_id.is_(guild.id))
            userserverdata = await Database.select_one(
                UserServerData, 
                sqlalchemy.and_(
                    UserServerData.discord_id.is_(member.id), 
                    UserServerData.server_id.is_(guild.id)
                )
            )

            guild = member.guild


            
            if after.channel is not None:
                voice_channel_datas = await Database.select_one(VoiceChannel, VoiceChannel.channel_id.is_(after.channel.id))
                if voice_channel_datas is not None:
                    voice_channel_datas: VoiceChannel
                    black_list = await Database.select_all(
                        BlackList, 
                        sqlalchemy.and_(
                            BlackList.server_id.is_(guild.id), 
                            BlackList.discord_id.is_(voice_channel_datas.discord_id)
                        )
                    )
                    bl = [row.user for row in black_list]
                    LOG.System(f"{bl}")
                    if member.id in bl:
                        await member.move_to(None)
            


            if (server_config.voice_creator_channel is not None) and (after.channel is not None) and (after.channel.id == server_config.voice_creator_channel):
                """如果是加入創建功能的語音頻道"""

                LOG.System(f"使用者: {LOG.User(member)}進入了創建功能頻道: {LOG.Channel(after.channel)}")

                voice_channel = await Database.select_one(VoiceChannel, sqlalchemy.and_(VoiceChannel.discord_id.is_(member.id), VoiceChannel.server_id.is_(guild.id)))

                if voice_channel is not None:
                    try:
                        channel = self.bot.get_channel(voice_channel.channel_id)
                        
                        LOG.System(f"查詢到頻道: {LOG.Channel(channel)} 移動中")
                        await member.move_to(channel)
                    except AttributeError:
                        """當移動時出問題"""
                        pass # 跳出，執行創建頻道

                    else:
                        """執行成功"""
                        if before.channel is not None:
                            """偵測移動前是否有頻道"""
                            await self.voice_channel_check(VoiceChannel.channel_id.is_(before.channel.id))
                            """偵測操作"""
                        return
                    

                """如果不存在語音頻道則創建"""
                LOG.System(f"無查詢到使用者是否擁有頻道，創建中")
                if userserverdata.voice_name is None:
                    userserverdata.voice_name = server_config.default_name.replace("{user_name}", member.display_name)
                

                # 設置權限覆寫，給特定成員賦予管理頻道的權限
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=True),
                    member: discord.PermissionOverwrite(manage_channels=True, move_members=True)
                }

                channel = await guild.create_voice_channel(
                    name=userserverdata.voice_name,
                    category=after.channel.category,
                    position=0,
                    overwrites=overwrites
                )


                voice_channel = VoiceChannel(discord_id=member.id, server_id=guild.id, channel_id=channel.id)
                await Database.insert_or_replace(voice_channel)
                await member.move_to(channel)                    

                if before.channel is not None:
                    await self.voice_channel_check(VoiceChannel.channel_id.is_(before.channel.id))
                    return
                

            else:
                conditions = []

                # 如果 before.channel 存在，則添加對應的查詢條件
                if before.channel is not None:
                    conditions.append(VoiceChannel.channel_id == before.channel.id)

                # 如果 after.channel 存在，則添加對應的查詢條件
                if after.channel is not None:
                    conditions.append(VoiceChannel.channel_id == after.channel.id)

                conditions.append(VoiceChannel.discord_id == member.id)
                # 使用 sqlalchemy.or_ 來合併查詢條件
                if conditions:
                    query_condition = sqlalchemy.or_(*conditions)
                    await self.voice_channel_check(query_condition)
                



        except Exception as e:
            LOG.Except(f"{e}")


        # if before.channel is None and after.channel:
        #     print(f"「{member.display_name}」加入「{after.channel.name}」語音頻道")
        # elif before.channel and after.channel is None:
        #     print(f"「{member.display_name}」離開「{before.channel.name}」語音頻道")
        # elif before.channel != after.channel:
        #     print(f"「{member.display_name}」移動「{before.channel.name} -> {after.channel.name}」語音頻道")




    @app_commands.command(name="語音條件設定", description="設定語音頻道刪除條件")
    @app_commands.rename(option="條件")
    @app_commands.choices(
        option=[
            Choice(name="當語音沒有人", value=0),
            Choice(name="當創建者離開語音",value=1,),
            Choice(name="當創建者離開任何語音", value=2),
            Choice(name="當創建者不再任何語音及語音沒有人", value=3),
        ]
    )
    @SlashCommandLogger
    async def slash_delete_rule(self, interaction: discord.Interaction, option: int):
        try:
            # 創建選項名稱與數值的映射
            option_name_map = {
                0: "當語音沒有人",
                1: "當創建者離開語音",
                2: "當創建者離開任何語音",
                3: "當創建者不再任何語音及語音沒有人",
            }
            data = await Database.select_one(UserServerData, sqlalchemy.and_(UserServerData.discord_id.is_(interaction.user.id), UserServerData.server_id.is_(interaction.guild.id)))
            data.delete_rule = option
            await Database.insert_or_replace(data)
            await interaction.response.send_message(content=f"已將條件設定為\"**{option_name_map[option]}**\"", ephemeral=True)
            await self.voice_channel_check(VoiceChannel.discord_id.is_(interaction.user.id))
        except Exception as e:
            await interaction.response.send_message(content=f"錯誤", ephemeral=True)






    @app_commands.command(name="設定創建頻道", description="選擇語音創建頻道")
    @app_commands.rename(voice_channel="頻道")
    @SlashCommandLogger
    async def slash_voice_creator(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel):
        if interaction.user.guild_permissions.administrator:
            try:
                 
                serverconfiguration = await Database.select_one(ServerConfiguration, ServerConfiguration.server_id.is_(interaction.guild_id))
                serverconfiguration.voice_creator_channel = voice_channel.id
                await Database.insert_or_replace(serverconfiguration)

                await interaction.response.send_message(content=f"已將頻道設定為\"**{voice_channel}**\"", ephemeral=True)
                
                member: discord.Member = None
                for member in voice_channel.members:
                    try:
                        await member.move_to(None)
                    except:
                        continue

            except Exception as e:
                await interaction.response.send_message(content=f"錯誤", ephemeral=True)        

        else:
            await interaction.response.send_message(content=f"你沒有這個權限", ephemeral=True)





    @app_commands.command(name="黑名單", description="增加或減少黑名單")
    @app_commands.rename(member="使用者")
    @SlashCommandLogger
    async def slash_bl(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.user.guild_permissions.administrator:
            try:
                guild = member.guild

                user = interaction.user

                bl = await Database.select_one(
                    BlackList, 
                    sqlalchemy.and_(
                        BlackList.server_id.is_(guild.id),
                        BlackList.discord_id.is_(user.id),
                        BlackList.user.is_(member.id)
                    )
                )
                if bl is None:
                    bl = BlackList(server_id=guild.id, discord_id=user.id, user=member.id)
                    await Database.insert_or_replace(bl)

                else:
                    await Database.delete_instance(bl)

            except Exception as e:
                await interaction.response.send_message(content=f"錯誤", ephemeral=True)

        else:
            await interaction.response.send_message(content=f"你沒有這個權限", ephemeral=True)



async def setup(client: commands.Bot):
    await client.add_cog(VoiceCreatorCog(client))








