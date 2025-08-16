#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions for the Telegram Vehicle Registration Bot
"""

import re
import requests
import json
from functools import wraps
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext
from config import *
from storage import get_user, update_user, save_state, config, global_free_active

# Initialize bot instance
bot = Bot(token=TELEGRAM_TOKEN)

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return int(user_id) == int(ADMIN_ID)

def is_valid_rc(rc: str) -> bool:
    """Validate RC number format"""
    rc = rc.strip().upper()
    return bool(re.fullmatch(RC_PATTERN, rc))

def check_channel_joined(user_id: int) -> bool:
    """Check if user has joined the required channel"""
    chat_id = config.get("CHANNEL_CHAT_ID", CHANNEL_CHAT_ID)
    if not chat_id or chat_id == "@your_public_channel_username_or_-100XXXXXXXXXX":
        # Misconfigured; skip enforcing to avoid hard lock
        return True
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

def require_join(func):
    """Decorator to require channel membership"""
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        joined = check_channel_joined(user.id)
        update_user(user.id, {"joined_channel": joined})
        save_state()
        
        if not joined:
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Channel", url=config.get("CHANNEL_LINK", CHANNEL_LINK))],
                [InlineKeyboardButton("🔄 I've Joined", callback_data="recheck_join")]
            ])
            update.effective_message.reply_text(
                JOIN_REQUIRED_MESSAGE,
                reply_markup=kb, 
                parse_mode=ParseMode.MARKDOWN
            )
            return
        return func(update, context, *args, **kwargs)
    return wrapper

def main_menu_kb():
    """Generate main menu keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚘 Check Vehicle Information", callback_data="check_vehicle")],
        [InlineKeyboardButton("💳 My Credits", callback_data="check_credits"),
         InlineKeyboardButton("🎁 Refer & Earn", callback_data="referral")],
        [InlineKeyboardButton("📞 Support", callback_data="support"),
         InlineKeyboardButton("❓ Help", callback_data="help")]
    ])

def back_to_menu_kb():
    """Generate back to menu keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
    ])

def try_grant_referral_credit(new_user_id: int):
    """Try to grant referral credit if conditions are met"""
    user_data = get_user(new_user_id)
    
    if user_data.get("referrer_id") and not user_data.get("referral_credited"):
        if check_channel_joined(new_user_id):
            ref_id = str(user_data["referrer_id"])
            ref_user = get_user(int(ref_id))
            
            # Grant credit to referrer
            ref_user["credits"] += int(config.get("REF_CREDIT", 2))
            ref_user["ref_count"] += 1
            
            # Mark as credited
            user_data["referral_credited"] = True
            
            update_user(int(ref_id), ref_user)
            update_user(new_user_id, user_data)
            save_state()
            
            # Notify referrer
            try:
                bot.send_message(
                    chat_id=int(ref_id),
                    text=f"🎉 Referral bonus added: +{config.get('REF_CREDIT', 2)} credit(s). Thanks!"
                )
            except Exception:
                pass

def pretty_vehicle_text(data: dict) -> str:
    """Format vehicle data for display"""
    lines = []
    
    def field(label, key):
        val = data.get(key)
        if val in (None, "", "NA"):
            val = "N/A"
        # Replace @NGYT777GG with @hey_nigge
        if isinstance(val, str) and "@NGYT777GG" in val:
            val = val.replace("@NGYT777GG", "@hey_nigge")
        lines.append(f"*{label}:* `{val}`")

    title = "🚗 *Vehicle Details*"
    field("RC Number", "rc_number")
    field("Owner", "owner_name")
    field("Owner Serial", "owner_serial_no")
    field("Father Name", "father_name")
    field("Maker", "model_name")
    field("Model", "maker_model")
    field("Class", "vehicle_class")
    field("Fuel", "fuel_type")
    field("Fuel Norms", "fuel_norms")
    field("Registration", "registration_date")
    field("Insurance Co.", "insurance_company")
    field("Insurance Upto", "insurance_upto")
    field("Fitness Upto", "fitness_upto")
    field("Tax Upto", "tax_upto")
    field("PUC Upto", "puc_upto")
    field("Financier", "financier_name")
    field("RTO", "rto")
    field("Address", "address")
    field("City", "city")
    field("Phone", "phone")
    field("Owner TG", "owner")
    
    return f"{title}\n" + "\n".join(lines)

def fetch_vehicle_data(rc: str) -> dict:
    """Fetch vehicle data from API"""
    try:
        url = f"{VEHICLE_API_BASE}{rc}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                # Try to repair malformed JSON
                raw = response.text.strip()
                if not raw.startswith("{"):
                    raw = "{" + raw
                if not raw.endswith("}"):
                    raw = raw + "}"
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return {"rc_number": rc, "error": "Invalid API response format"}
        else:
            return {"rc_number": rc, "error": f"API returned status {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"rc_number": rc, "error": "API request timeout"}
    except requests.exceptions.RequestException as e:
        return {"rc_number": rc, "error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"rc_number": rc, "error": f"Unexpected error: {str(e)}"}
