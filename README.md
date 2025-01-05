# [vc+]([https://www.github.com/Qarchue/vc_plus](https://github.com/Qarchue/vc_plus))

<p align="center">
    <a href="https://github.com/Qarchue/vc_plus"><img src="https://img.shields.io/github/repo-size/Qarchue/vc_plus"></a>
    <a href="https://github.com/Qarchue/vc_plus"><img src="https://img.shields.io/github/languages/top/Qarchue/vc_plus"></a>
    <a href="https://github.com/Qarchue/vc_plus/stargazers"><img src="https://img.shields.io/github/stars/Qarchue/vc_plus?style=socia"></a>
    <a href="https://discord.gg/w5CeZh3rNu"><img src="https://img.shields.io/discord/905865794683015208?style=flat-square&logo=Discord&logoColor=white&label=support&color=5865F2"></a>
</p>

> 歡迎將本專案所有或部分程式碼放入你自己的機器人中。

## 簡介

基於各個機器人下的 join to create voice channel 功能改進的專案

我認為原版功能不夠齊全，無法進行更細微的調整，所以寫了這個專案

功能比較

|**功能**|**vc+**|**其他機器人**|
|:-|:-:|:-:|
|頻道管理權限|✅|❌|
|自訂頻道名稱|✅|❌|
|設定語音刪除條件|✅|❌|
|多個語音創建頻道|❌|✅|
|自訂黑名單|✅|❌|



---





## 使用方式

將機器人邀請至伺服器後使用 `/設定創建頻道` 來設定語音創建頻道

`/語音條件設定` 來設定自己的語音頻道刪除條件

`/黑名單` 黑名單功能，目前只能夠新增或移除


---





## 使用教學

此使用教學部分照搬原神小幫手的教學

### 架設 discord 機器人

需要在此步驟創建機器人並取得 Bot token

<details><summary>>>> 點此查看完整內容 <<<</summary>

1. 到 [Discord Developer](https://discord.com/developers/applications "Discord Developer") 登入 Discord 帳號

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_1.png)

2. 點選「New Application」建立應用，輸入想要的名稱後按「Create」

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_2.png)

3. 在 Bot 頁面，按「Reset Token」來取得機器人的 Token

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_3.png)

4. 第3步驟做完之後在下面將「Presence Intent」「Server Members Intent」「Message Content Intent」的開關打開

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_4.png)

5. 在 General Information，取得機器人的 Application ID

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_8.png)

5. 在 OAuth2/URL Generator，分別勾選「bot」「applications.commands」「Send Messages」

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_5.png)

6. 開啟最底下產生的 URL 將機器人邀請至自己的伺服器

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_6.png)

</details>


### 電腦端

1. 下載最新版本的 [Python](https://www.python.org/downloads/)。

2. 從 GitHub 下載此程式檔並解壓縮成資料夾。

3. 在程式資料夾內開啟命令提示字元並安裝依賴 `python3 -m pip install -r requirements.txt` 。

4. 以文字編輯器開啟 `utility` 目錄下的 `config.py` 並依照程式中的註解編輯參數

5. 運行 `start.bat` 就能開始使用了。

---





## 設定

以文字編輯器開啟 `utility` 目錄下的 `config.py` 並編輯物件裡的參數  
刪掉註解的話應該長這樣：
```python
#...以上省略
class Config(BaseSettings):
    """機器人的配置"""

    main_server_id: int = 0
    application_id: int = 0
    bot_token: str = ""
    #以下省略...
```
`main_server_id`: 伺服器 ID，在discord內取得   
`application_id`: 機器人 Application ID，從 Discord Developer 網頁上取得   
`bot_token`: 機器人 Token，從 Discord Developer 網頁取得   

### 編輯完設定檔後記得儲存

---





## 專案資料夾結構

```
vc_plus/
    ├── cogs/
    │   ├── admin/            = 管理員命令
    │   ├── events_manage/        = discord 事件管理
    │   └── voice_creator/    = vc_plus 主要功能
    ├── data/             = 資料庫檔案    
    ├── database/         = SQLAlchemy ORM、資料庫操作相關的程式碼
    ├── utility/          = 一些本專案用到的設定、公用函式、Log、檔案操作...等程式碼
    ├── main.py           = 主程式
    ├── requirements.txt  = pip 依賴
    └── start.bat         = 執行檔
```

---





## 貢獻

程式架構修改自**原神小幫手**  
https://github.com/KT-Yeh/Genshin-Discord-Bot

程式撰寫: Qarchue


---





## 授權

此專案採用 MIT 授權，詳情請參閱 LICENSE 檔案。
