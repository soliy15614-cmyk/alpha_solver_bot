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
    # 1. கமாண்ட் லைன் ஆர்கியுமென்ட்ஸ் சரிபார்த்தல் (HTML பைல் பெயர் உள்ளதா என)
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "USAGE: python3 anti.py <html_file_name>"}))
        return

    html_file = sys.argv[1]

    # 2. குறிப்பிட்ட HTML கோப்பு கம்ப்யூட்டரில் உள்ளதா எனச் சரிபார்த்தல்
    if not os.path.exists(html_file):
        print(json.dumps({"success": False, "error": f"FILE_NOT_FOUND: {html_file}"}))
        return

    # 3. alpha.session கோப்பு உள்ளதா என்று சரிபார்த்தல்
    if not os.path.exists(f"{SESSION_NAME}.session"):
        print(json.dumps({"success": False, "error": "TG_SESSION_NOT_FOUND"}))
        return

    # 4. டெலிகிராம் கிளையன்ட் தொடங்குதல்
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    try:
        # HTML கோப்பை /antibot என்ற கேப்ஷனுடன் (Caption) பாட்டிற்கு அப்லோட் செய்தல்
        await client.send_file(
            BOT_USERNAME, 
            html_file, 
            caption="/antibot"
        )
        
        token_found = False
        attempts = 0
        
        # பதில் வரும் வரை அல்லது 5 நிமிடம் முடியும் வரை காத்திருக்கும் லூப்
        while not token_found and attempts < 30:
            await asyncio.sleep(10)
            attempts += 1
            
            # பாட்டின் கடைசி மெசேஜை எடுத்தல்
            async for message in client.iter_messages(BOT_USERNAME, limit=1):
                if message.text and not message.text.startswith('/'):
                    bot_response = message.text.strip()
                    
                    # பாட் இன்னும் சால்வ் செய்யவில்லை (NOT READY) என்றால், தொடர்ந்து காத்திருக்கவும்
                    if "CAPTCHA_NOT_READY" in bot_response:
                        continue
                    
                    try:
                        # பதில் JSON ஆக இருந்தால், அதை அப்படியே பிரிண்ட் செய்யும்
                        parsed_json = json.loads(bot_response)
                        if "token" in parsed_json or "success" in parsed_json:
                            print(json.dumps(parsed_json))
                            token_found = True
                    except ValueError:
                        # பாட் வெறும் ஸ்ட்ரிங் டோக்கன் மட்டும் தந்தால், JSON ஆக மாற்றி பிரிண்ட் செய்யும்
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

