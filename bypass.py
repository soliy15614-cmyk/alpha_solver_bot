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
    டெலிகிராம் பாட்டிற்கு லிங்கை அனுப்பி, பைபாஸ் செய்யப்பட்ட
    யூஆர்எல்-ஐ பெற்றுத் தரும். பிழைகள் அல்லது விளம்பரங்கள் வந்தால்
    None என ரிட்டர்ன் செய்து தவிர்க்கும்.
    """
    client = TelegramClient('psycho_bypass_session', API_ID, API_HASH)
    await client.start()
    
    try:
        bot_entity = await client.get_input_entity(TARGET_BOT)
    except Exception as e:
        print(f"\n\033[91m[!] Telegram Bot Error: {e}\033[0m")
        await client.disconnect()
        return None

    # பாட்டிற்கு கட்டளையை அனுப்புதல்
    command = f"/bypass {shortlink_url}"
    await client.send_message(bot_entity, command)
    
    bypassed_url = None
    is_failed = False
    loop_timeout = time.time() + 45  # அதிகபட்சம் 45 நொடிகள் காத்திருக்கும்
    
    @client.on(events.NewMessage(chats=TARGET_BOT))
    async def handler(event):
        nonlocal bypassed_url, is_failed
        response_text = event.message.message
        
        # 1. பைபாஸ் இன்டரப்ட் பிழையைக் கண்டறிதல்
        if "Shortlink Bypass Engine Interrupted!" in response_text:
            print("\n\033[91m[!] Bot Alert: ❌ Shortlink Bypass Engine Interrupted!\033[0m")
            is_failed = True
            event.disconnect()
            
        # 2. சேனல் ஜாயின் விளம்பர அறிவிப்பைக் கண்டறிதல்
        elif "must join our channel" in response_text or "https://t.me/A_ToolsX" in response_text:
            print("\n\033[93m[!] Bot Alert: 🚀 Channel Join Requirement Prompted!\033[0m")
            is_failed = True
            event.disconnect()

        # 3. வெற்றிகரமான Destination யூஆர்எல்-ஐ பிரித்தல்
        elif "Destination:" in response_text:
            lines = response_text.split('\n')
            for line in lines:
                if "Destination:" in line:
                    bypassed_url = line.split("Destination:")[-1].strip()
                    break
            event.disconnect()

    # பதில் கிடைக்கும் வரை அல்லது டைம்அவுட் ஆகும் வரை காத்திருக்கும் லூப்
    while bypassed_url is None and not is_failed and time.time() < loop_timeout:
        await asyncio.sleep(0.5)
        
    await client.disconnect()
    
    if is_failed:
        return "SKIP_LINK"  # இந்த லிங்க்கை தவிர்க்க வேண்டும் என்பதற்கான சிக்னல்
    return bypassed_url

def bypass_url_sync(shortlink_url):
    """shortlink.py-ல் இருந்து நேரடியாக அழைக்க உதவும் செயல்பாடு"""
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

