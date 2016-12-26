LINE ID:@xxo4608z




SETUP:

Secret Data

You MUST setup the following variables.

SECRET_KEY 

django secret key. You can generate using Django secret key generator

LINE_CHANNEL_SECRET

LINE_CHANNEL_ACCESS_TOKEN

There are two way to set these variables

1. Set these variables in line_echobot/line_echobot/settings_secret.py(Exactly the same name)

2. Add these variables to environment variables. (settings_secret.py is loaded first)

HTTPS Server

You'll need a https server.

Heroku can serve this for you.

All the needed settings for heroku are set in this repo.

Otherwise, you can also build your own https server.

Set Webhook URL

Set webhook url on your LINE Developers page to https://"your domain name"/echobot/callback/



usage:

請輸入:天氣  台灣各縣市地點名稱 今天或明天 等關鍵字

例如:明天高雄天氣如何
