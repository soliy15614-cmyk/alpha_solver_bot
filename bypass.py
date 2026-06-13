#!/usr/bin/env python3
import sys
import time
import asyncio
from telethon import TelegramClient, events

# ============================================================
# TELEGRAM APP CONFIGURATION
# ============================================================
API_ID = 28752231
API_HASH = "ec1c1f2c30e2f1855c3edee7e348480b"
TARGET_BOT = "alpha_solver_bot"

# ============================================================
# CORE BYPASS FUNCTION
# ============================================================
async def get_bypassed_link(shortlink_url):
    """
    Sends the link to the Telegram bot and monitors both new and edited 
    messages to extract the final destination URL without strict timeouts.
    """
    client = TelegramClient('psycho_bypass_session', API_ID, API_HASH)
    await client.start()

    try:
        bot_entity = await client.get_input_entity(TARGET_BOT)
    except Exception as e:
        print(f"\n\033[91m[!] Telegram Bot Error: {e}\033[0m")
        await client.disconnect()
        return None

    # Send command to the bot
    command = f"/bypass {shortlink_url}"
    await client.send_message(bot_entity, command)

    bypassed_url = None
    is_failed = False
    stop_event = asyncio.Event()

    async def check_message(event):
        nonlocal bypassed_url, is_failed
        response_text = event.message.message

        # 1. Detect Bypass Interruption Error
        if "Shortlink Bypass Engine Interrupted!" in response_text:
            print("\n\033[91m[!] Bot Alert: ❌ Shortlink Bypass Engine Interrupted!\033[0m")
            is_failed = True
            stop_event.set()

        # 2. Detect Mandatory Channel Join Advertisement
        elif "must join our channel" in response_text or "https://t.me/A_ToolsX" in response_text:
            print("\n\033[93m[!] Bot Alert: 🚀 Channel Join Requirement Prompted!\033[0m")
            is_failed = True
            stop_event.set()

        # 3. Detect and Extract Successful Destination URL (Handles incoming Edits and New Messages)
        elif "Destination:" in response_text:
            lines = response_text.split('\n')
            for line in lines:
                if "Destination:" in line:
                    bypassed_url = line.split("Destination:")[-1].strip()
                    break
            stop_event.set()

    # Register handlers for both New Messages and Edits from the target bot
    client.add_event_handler(check_message, events.NewMessage(chats=TARGET_BOT))
    client.add_event_handler(check_message, events.MessageEdited(chats=TARGET_BOT))

    # Keep waiting indefinitely until either a success or fail condition flips the stop_event
    await stop_event.wait()

    await client.disconnect()

    if is_failed:
        return "SKIP_LINK"
    return bypassed_url

def bypass_url_sync(shortlink_url):
    """Synchronous wrapper to call get_bypassed_link directly from shortlink.py"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(get_bypassed_link(shortlink_url))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_link = sys.argv[1]
        print(f"\033[96m[~] Testing Bypass for:\033[0m {test_link}")
        res = bypass_url_sync(test_link)
        print(f"Result: {res}")
    else:
        print("Usage: python3 bypass.py <shortlink_url>")

