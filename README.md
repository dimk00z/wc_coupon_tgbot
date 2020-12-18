# Woocommerce coupon bot

## Description

This is small app for creating coupons on woocommerce site with telegram

.env must have these parameters:
```
TELEGRAM_BOT_TOKEN=
TELEGRAM_USERS_ID=id,id2...
WC_USER_KEY=
WC_SECRET_KEY=
WC_URL=

```
`cp tgbot.service /etc/systemd/system` - copy service file
` systemctl start tgbot` - start service