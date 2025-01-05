from datetime import datetime

from pydantic_settings import BaseSettings
import json
from pathlib import Path



class Config(BaseSettings):
    """機器人的配置"""

    main_server_id: int = 0  # 範例，把0改成: 1283298446570968165
    """伺服器 ID"""                     # (假的伺服器 ID ，示範用)
    application_id: int = 0  # 範例，把0改成: 1246979890831816573  # (假的 Application ID ，示範用)
    """機器人 Application ID，從 Discord Developer 網頁上取得"""
    bot_token: str = ""  # 範例: "MTI4O0NNTU34NDYFvmdMA.G2kW0E.eGub5Gvc-T1Dv129TA532919TA4jgHfuL7-XR5T667KU"
    """機器人 Token，從 Discord Developer 網頁取得"""             # (這當然是假token，外洩token的後果是很嚴重的)




    expired_user_days: int = 180
    """過期使用者天數，會刪除超過此天數未使用任何指令的使用者"""

    slash_cmd_cooldown: float = 5.0
    """使用者重複呼叫部分斜線指令的冷卻時間（單位：秒）"""
    discord_view_long_timeout: float = 1800
    """Discord 長時間互動介面（例：下拉選單） 的逾時時間（單位：秒）"""
    discord_view_short_timeout: float = 60
    """Discord 短時間互動介面（例：確認、選擇按鈕）的逾時時間（單位：秒）"""

    sentry_sdk_dsn: str | None = None
    """Sentry DSN 位址設定"""
    prometheus_server_port: int | None = None
    """Prometheus server 監聽的 Port，若為 None 表示不啟動 server"""



    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()  # type: ignore
