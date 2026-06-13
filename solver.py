#!/usr/bin/env python3
import asyncio
import base64
import json
import re
import sys
from typing import Optional
from telethon import TelegramClient, events

# ═══════════════════════════════════════════════════════════
# TELEGRAM CONFIGURATION
# ═══════════════════════════════════════════════════════════
API_ID = 28752231
API_HASH = "ec1c1f2c30e2f1855c3edee7e348480b"
TARGET_BOT = "alpha_solver_bot"

R = '\033[91m'
Y = '\033[93m'
E = '\033[0m'

async def ask_telegram_solver(captcha_data: dict) -> Optional[dict]:
    try:
        json_str = json.dumps(captcha_data, indent=2)
        b64_encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        command = f"/aruble {b64_encoded}"

        client = TelegramClient('arable_userbot', API_ID, API_HASH)
        await client.start()

        bot_peer = await client.get_input_entity(TARGET_BOT)
        future_result = asyncio.get_running_loop().create_future()

        # மெசேஜ் ஹேண்ட்லர்
        @client.on(events.NewMessage(chats=bot_peer, incoming=True))
        async def handler_new(event):
            text = event.raw_text
            # சேனலில் ஜாயின் செய்யச் சொல்லி விளம்பரம் வந்தால்
            if "must join our channel" in text or "t.me/" in text:
                if not future_result.done():
                    future_result.set_result("RETRY_REQUIRED")
            elif "🔑" in text or "❌" in text:
                if not future_result.done(): 
                    future_result.set_result(text)

        @client.on(events.MessageEdited(chats=bot_peer, incoming=True))
        async def handler_edit(event):
            text = event.raw_text
            if "🔑" in text or "❌" in text:
                if not future_result.done(): 
                    future_result.set_result(text)

        # மெசேஜ் அனுப்புதல்
        await client.send_message(bot_peer, command)

        try:
            final_text = await asyncio.wait_for(future_result, timeout=45)
            
            # விளம்பரம் வந்தால் மீண்டும் ஒருமுறை முயற்சி செய்தல்
            if final_text == "RETRY_REQUIRED":
                await asyncio.sleep(3)
                # ஹேண்ட்லர்களை ரிசெட் செய்துவிட்டு மீண்டும் அனுப்புதல்
                await client.send_message(bot_peer, command)
                # மீண்டும் 30 நொடிகள் காத்திருத்தல்
                final_text = await asyncio.wait_for(future_result, timeout=30)

            if "🔑" in final_text:
                match = re.search(r'🔑\s*([A-Za-z0-9+/=]+)', final_text)
                if match:
                    encoded_ans = match.group(1)
                    decoded_ans_str = base64.b64decode(encoded_ans).decode('utf-8')
                    parsed_ans = json.loads(decoded_ans_str)
                    await client.disconnect()
                    return parsed_ans
        except asyncio.TimeoutError:
            pass
        
        await client.disconnect()
    except Exception:
        pass
    return None

def sync_solve_captcha(captcha_data: dict) -> Optional[dict]:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(ask_telegram_solver(captcha_data))

