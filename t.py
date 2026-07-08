import sys
import os
import json
import asyncio
from telethon import TelegramClient

API_ID = 32744606
API_HASH = 'f58682565ec84dcd4e529a33246f07aa'
SESSION_NAME = 'alpha'
BOT_USERNAME = '@alpha_solver_bot'

async def main():
    # 1. கமாண்ட் லைன் ஆர்கியுமென்ட்ஸ் சரிபார்த்தல்
    if len(sys.argv) < 3:
        print(json.dumps({"success": False, "error": "USAGE: python3 turnstile.py <url> <sitekey>"}))
        return

    url = sys.argv[1]
    sitekey = sys.argv[2]

    # 2. alpha.session கோப்பு உள்ளதா என்று சரிபார்த்தல்
    if not os.path.exists(f"{SESSION_NAME}.session"):
        print(json.dumps({"success": False, "error": "TG_SESSION_NOT_FOUND"}))
        return

    # 3. டெலிகிராம் கிளையன்ட் தொடங்குதல்
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    try:
        command = f"/turnstile {url} {sitekey}"
        
        # பின்னணியில் பாட்டிற்கு மெசேஜ் அனுப்புகிறது
        await client.send_message(BOT_USERNAME, command)
        
        token_found = False
        attempts = 0
        
        # டோக்கன் கிடைக்கும் வரை அல்லது 5 நிமிடம் முடியும் வரை லூப் ஓடும்
        while not token_found and attempts < 30:
            await asyncio.sleep(10)
            attempts += 1
            
            # பாட்டின் கடைசி மெசேஜை எடுத்தல்
            async for message in client.iter_messages(BOT_USERNAME, limit=1):
                if message.text and not message.text.startswith('/'):
                    bot_response = message.text.strip()
                    
                    # பாட் இன்னும் சால்வ் செய்யவில்லை (NOT READY) என்றால், பிரிண்ட் செய்யாமல் லூப்பை தொடரவும்
                    if "CAPTCHA_NOT_READY" in bot_response:
                        continue
                    
                    try:
                        # பதில் JSON ஆக இருந்து, அதில் 'token' இருந்தால் மட்டுமே பிரிண்ட் செய்யும்
                        parsed_json = json.loads(bot_response)
                        if "token" in parsed_json or "success" in parsed_json:
                            print(json.dumps(parsed_json))
                            token_found = True
                    except ValueError:
                        # பாட் வெறும் ஸ்ட்ரிங் டோக்கன் மட்டும் தந்தால்
                        success_msg = {
                            "success": "true",
                            "token": bot_response
                        }
                        print(json.dumps(success_msg))
                        token_found = True
                        
                    if token_found:
                        break
                    
        if not token_found:
            print(json.dumps({"success": False, "error": "TIMEOUT_WAITING_FOR_TOKEN"}))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

