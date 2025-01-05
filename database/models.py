import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List

class Base(MappedAsDataclass, DeclarativeBase):
    """資料庫 Table 基礎類別，繼承自 sqlalchemy `MappedAsDataclass`, `DeclarativeBase`"""

    type_annotation_map = {dict[str, str]: sqlalchemy.JSON}


class UserServerData(Base):
    """使用者伺服器資料庫 Table"""

    __tablename__ = "user_server_data"



    discord_id: Mapped[int] = mapped_column(ForeignKey("users.discord_id"), primary_key=True)
    """使用者 ID"""

    server_id: Mapped[int] = mapped_column(ForeignKey("servers.server_id"), primary_key=True)
    """伺服器 ID"""

    user: Mapped["User"] = relationship("User", back_populates="user_servers", lazy="select")
    """與使用者的關聯"""

    server: Mapped["Server"] = relationship("Server", back_populates="server_users", lazy="select")
    """與伺服器的關聯"""

    delete_rule: Mapped[int] = mapped_column(default=None, nullable=True)

    voice_name: Mapped[str | None] = mapped_column(default=None, nullable=True)

class BlackList(Base):
    """黑名單"""

    __tablename__ = "black_list"


    server_id: Mapped[int] = mapped_column(ForeignKey("servers.server_id"), primary_key=True)
    """伺服器 ID"""

    discord_id: Mapped[int] = mapped_column(ForeignKey("users.discord_id"), primary_key=True)
    """使用者 ID"""

    user: Mapped[int] = mapped_column(nullable=False)



class VoiceChannel(Base):
    """使用者伺服器資料庫 Table"""

    __tablename__ = "voice_channel"



    discord_id: Mapped[int] = mapped_column(ForeignKey("users.discord_id"), primary_key=True)
    """使用者 ID"""

    server_id: Mapped[int] = mapped_column(ForeignKey("servers.server_id"), primary_key=True)
    """伺服器 ID"""

    channel_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)




class ServerConfiguration(Base):
    __tablename__ = 'server_configuration'

    server_id: Mapped[int] = mapped_column(ForeignKey("servers.server_id"), primary_key=True)
    """伺服器 ID"""

    voice_creator_channel: Mapped[int] = mapped_column(default=None, nullable=True)


    default_name: Mapped[str] = mapped_column(default=None, nullable=True)

    # Relationship with Server
    server = relationship("Server", back_populates="configuration")


class Server(Base):
    """伺服器資料庫 Table"""

    __tablename__ = "servers"

    server_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    """伺服器ID"""

    configuration = relationship("ServerConfiguration", back_populates="server", uselist=False)


    server_users: Mapped[List["UserServerData"]] = relationship(back_populates="server", default_factory=list)
    """與使用者伺服器資料的關聯"""


    name: Mapped[str | None] = mapped_column(default=None)
    """伺服器名稱"""





class User(Base):
    """使用者資料庫 Table"""

    __tablename__ = "users"


    discord_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    """使用者 Discord ID"""


    user_servers: Mapped[List["UserServerData"]] = relationship(back_populates="user", default_factory=list)
    """與伺服器資料的關聯"""

    name: Mapped[str | None] = mapped_column(default=None)
    """使用者名稱"""



