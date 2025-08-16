#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Storage management for the Telegram Vehicle Registration Bot
Handles JSON file-based persistence for users and configuration
"""

import json
import os
import threading
import time
from datetime import datetime
from config import USERS_FILE, CONFIG_FILE, DEFAULT_CONFIG

# Global storage variables
users = {}
config = {}
LOCK = threading.Lock()

def load_json(path, default):
    """Load JSON data from file with fallback to default"""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return default
    return default

def save_json(path, data):
    """Save JSON data to file with atomic write"""
    tmp = path + ".tmp"
    with LOCK:
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
        except Exception as e:
            print(f"Error saving {path}: {e}")
            if os.path.exists(tmp):
                os.remove(tmp)

def load_storage():
    """Initialize storage by loading users and config"""
    global users, config
    users = load_json(USERS_FILE, {})
    config = load_json(CONFIG_FILE, DEFAULT_CONFIG)

def save_state():
    """Save current state to files"""
    save_json(USERS_FILE, users)
    save_json(CONFIG_FILE, config)

def ensure_user(uid: int):
    """Ensure user exists in storage with default values"""
    uid_str = str(uid)
    if uid_str not in users:
        users[uid_str] = {
            "trials": int(config.get("FREE_TRIAL_DEFAULT", 3)),
            "credits": 0,
            "subscription": False,
            "joined_channel": False,
            "referrer_id": None,          # numeric ID as string (pending reward)
            "referral_credited": False,   # mark once credited
            "ref_count": 0,               # how many referred (info)
            "created": int(time.time()),
            "last_used": int(time.time()),
            "state": "main_menu",         # Track user state for conversation flow
            "waiting_for_vehicle": False  # Track if waiting for vehicle input
        }

def get_user(uid: int):
    """Get user data"""
    ensure_user(uid)
    return users[str(uid)]

def update_user(uid: int, updates: dict):
    """Update user data"""
    ensure_user(uid)
    users[str(uid)].update(updates)
    users[str(uid)]["last_used"] = int(time.time())

def today_str():
    """Get today's date as string"""
    return datetime.utcnow().strftime("%Y-%m-%d")

def global_free_active() -> bool:
    """Check if global free period is active"""
    d = config.get("GLOBAL_FREE_UNTIL", "").strip()
    if not d:
        return False
    try:
        return datetime.strptime(today_str(), "%Y-%m-%d") <= datetime.strptime(d, "%Y-%m-%d")
    except Exception:
        return False
