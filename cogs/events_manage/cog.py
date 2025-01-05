import sqlalchemy
import discord

from discord.ext import commands

from database import Database, User, Server, UserServerData, ServerConfiguration

from utility import LOG, config


class EventManageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot




    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild

        server = await Database.select_one(Server, Server.server_id.is_(guild.id))

        server_config = await  Database.select_one(ServerConfiguration, ServerConfiguration.server_id.is_(guild.id))
        
        
        user = await Database.select_one(User, User.discord_id.is_(member.id))
        if user is None:
            user = User(member.id)
            user.name = member.name

            LOG.System(f"新增資料: {LOG.User(member)}")
            await Database.insert_or_replace(user)

        userserverdata = await Database.select_one(
            UserServerData, 
            sqlalchemy.and_(
                UserServerData.discord_id.is_(member.id), 
                UserServerData.server_id.is_(guild.id)
            )
        )
        
        if userserverdata is None:
            userserverdata = UserServerData(discord_id=member.id, server_id=guild.id, user=user, server=server)
            
            userserverdata.voice_name = None
            userserverdata.delete_rule = 3
            LOG.System(f"新增使用者伺服器資料{LOG.Server(guild)}裡的{LOG.User(member)}")
            await Database.insert_or_replace(userserverdata)


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        pass




    @commands.Cog.listener()
    async def on_ready(self):


        for guild in self.bot.guilds:
            server = await Database.select_one(Server, Server.server_id.is_(guild.id))
            if server is None:
                LOG.Event(f"被新增至伺服器: {LOG.Server(guild)}")
                server = Server(guild.id)
                server.name = guild.name

                LOG.System(f"新增資料: {LOG.Server(guild)}")
                await Database.insert_or_replace(server)
                try:
                    server_config = ServerConfiguration(guild.id)
                    
                    server_config.default_name = "{user_name}的語音頻道"
                    server_config.server = server
                    LOG.System(f"新增設定資料: {LOG.Server(guild)}")
                    await Database.insert_or_replace(server_config)
                except Exception as e:
                    LOG.System(f"錯誤{e}")



            for member in guild.members:
                user = await Database.select_one(User, User.discord_id.is_(member.id))
                if user is None:
                    user = User(member.id)
                    user.name = member.name

                    LOG.System(f"新增資料: {LOG.User(member)}")
                    await Database.insert_or_replace(user)

                
                userserverdata = await Database.select_one(
                    UserServerData, 
                    sqlalchemy.and_(
                        UserServerData.discord_id.is_(member.id), 
                        UserServerData.server_id.is_(guild.id)
                    )
                )
                
                if userserverdata is None:
                    userserverdata = UserServerData(discord_id=member.id, server_id=guild.id, user=user, server=server)
                    
                    userserverdata.voice_name = None
                    userserverdata.delete_rule = 3
                    LOG.System(f"新增使用者伺服器資料{LOG.Server(guild)}裡的{LOG.User(member)}")
                    await Database.insert_or_replace(userserverdata)







    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild | None):
        
        server = await Database.select_one(Server, Server.server_id.is_(guild.id))
        if server is None:
            LOG.Event(f"被新增至伺服器: {LOG.Server(guild)}")
            server = Server(guild.id)
            server.name = guild.name

            LOG.System(f"新增資料: {LOG.Server(guild)}")
            await Database.insert_or_replace(server)
            try:
                server_config = ServerConfiguration(guild.id)
                server_config.voice_creator_channel = None
                server_config.default_name = "{user_name}的語音頻道"
                server_config.server = server
                LOG.System(f"新增設定資料: {LOG.Server(guild)}")
                await Database.insert_or_replace(server_config)
            except Exception as e:
                LOG.System(f"錯誤{e}")



        for member in guild.members:
            user = await Database.select_one(User, User.discord_id.is_(member.id))
            if user is None:
                user = User(member.id)
                user.name = member.name

                LOG.System(f"新增資料: {LOG.User(member)}")
                await Database.insert_or_replace(user)

            
            userserverdata = await Database.select_one(
                UserServerData, 
                sqlalchemy.and_(
                    UserServerData.discord_id.is_(member.id), 
                    UserServerData.server_id.is_(guild.id)
                )
            )
            
            if userserverdata is None:
                userserverdata = UserServerData(discord_id=member.id, server_id=guild.id, user=user, server=server)
                
                userserverdata.voice_name = None
                userserverdata.delete_rule = 3
                LOG.System(f"新增使用者伺服器資料{LOG.Server(guild)}裡的{LOG.User(member)}")
                await Database.insert_or_replace(userserverdata)




                    
            
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild | None):
        LOG.Event(f"被移除自伺服器: {LOG.Server(guild)}")



    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if before.name != after.name:
            server = await Database.select_one(Server, Server.server_id.is_(before.id))
            server.name = after.name
            LOG.System(f"伺服器: {LOG.Server(before)} 將名稱改成 {LOG.Server(after)}")
            await Database.insert_or_replace(server)








async def setup(client: commands.Bot):
    await client.add_cog(EventManageCog(client))
