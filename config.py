#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for the Telegram Vehicle Registration Bot
Edit the values below according to your setup
"""

import os

# ---------- MAIN CONFIG ----------
# Get from environment variables with fallbacks
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8492353975:AAG_an_bIXjIB_Cflaygkec_Gs4zmBlPBvw")
SUBSCRIBE_USERNAME = os.getenv("SUBSCRIBE_USERNAME", "Hey_nigge")  # your username (without @)
VEHICLE_API_BASE = os.getenv("VEHICLE_API_BASE", "https://rc-info-ng.vercel.app/?rc=")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/+nmvmmqGNFtA5OWVl")
CHANNEL_CHAT_ID = os.getenv("CHANNEL_CHAT_ID", "")  # Disabled until proper channel ID is set
ADMIN_ID = int(os.getenv("ADMIN_ID", "7777680053"))  # Your Telegram user ID (Hey_nigge)
FREE_TRIAL_DEFAULT = int(os.getenv("FREE_TRIAL_DEFAULT", "3"))
GLOBAL_FREE_UNTIL = os.getenv("GLOBAL_FREE_UNTIL", "")  # "2025-09-30" format or empty string

# ---------- FILE PATHS ----------
USERS_FILE = "users.json"
CONFIG_FILE = "config.json"

# ---------- DEFAULT CONFIG VALUES ----------
DEFAULT_CONFIG = {
    "FREE_TRIAL_DEFAULT": FREE_TRIAL_DEFAULT,
    "GLOBAL_FREE_UNTIL": GLOBAL_FREE_UNTIL,
    "CHANNEL_LINK": CHANNEL_LINK,
    "CHANNEL_CHAT_ID": CHANNEL_CHAT_ID,
    "REF_CREDIT": 2,          # reward per qualified referral
    "REF_TARGET": 3           # info only (you can show it), not used for gating
}

# ---------- REGEX PATTERNS ----------
RC_PATTERN = r"[A-Z]{2}\d{1,2}[A-Z]{0,3}\d{3,4}"

# ---------- MESSAGE TEMPLATES ----------
WELCOME_MESSAGE = """👋 Welcome, *{name}*!

🔒 Bot locked. Please *join our channel* to continue."""

MAIN_MENU_MESSAGE = """🚗 *Vehicle Registration Bot*

Welcome to your vehicle information assistant! Choose an option below:

✨ *What would you like to do?*"""

VEHICLE_INPUT_MESSAGE = """🚘 *Vehicle Information*

Please enter your vehicle registration number:

*Example:* `UP65CM9494`, `DL01AB1234`, `MH12CD5678`

Send the RC number as a message."""

HELP_MESSAGE = """🛠 *How to use this bot*

🚘 *Check Vehicle:* Get complete vehicle details
💳 *Credits:* View your remaining credits  
🎁 *Refer & Earn:* Share and earn 2 credits per referral
📞 *Support:* Get help or contact admin

💡 Each vehicle check uses 1 credit. New users get 3 free credits!"""

CREDITS_MESSAGE = """💳 *Your Credit Balance*

🎟 *Free Trials:* `{trials}` remaining
💰 *Bonus Credits:* `{credits}`
📊 *Subscription:* {subscription_status}
🌟 *Global Free:* `{global_free}`
👥 *Successful Referrals:* `{ref_count}`

💡 *How to get more credits:*
• Refer friends (+2 credits each)
• Contact support: @{subscribe_username}"""

REFERRAL_MESSAGE = """🎁 *Refer & Earn Credits*

💰 *Earn 2 credits* for each friend who:
✅ Joins via your link
✅ Joins our channel

📲 *Your Referral Link:*
`{ref_link}`

👥 *Your Stats:*
• Successful Referrals: `{ref_count}`
• Credits Earned: `{total_earned}` credits

🔗 *Share this link* with friends and family!"""

SUPPORT_MESSAGE = """📞 *Support & Contact*

Need help or want to buy credits?

👨‍💼 *Contact Admin:* @{subscribe_username}

💡 *Common Questions:*
• How to get more credits?
• Bot not working?
• Feature requests?
• Business inquiries?

We're here to help! 🤝"""

INSUFFICIENT_CREDITS_MESSAGE = """⚠️ Your free trials are over.
Buy credits/subscription to continue."""

JOIN_REQUIRED_MESSAGE = """🔒 *Access Locked*

Please join our channel to use the bot."""

VEHICLE_USAGE_MESSAGE = """Usage: `/vehicle <RC_Number>`
Example: `/vehicle UP65CM9494`"""

INVALID_RC_MESSAGE = """❌ Invalid RC format. Example: `UP65CM9494`"""

FETCHING_MESSAGE = "⏳ Fetching vehicle info..."
