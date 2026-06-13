#!/usr/bin/env python3
import os
import sys
import json
import time

# ============================================================
# COLOR SYSTEM & CONFIG
# ============================================================
G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
C = '\033[96m'
D = '\033[90m'
E = '\033[0m'

CONFIG_FILE = "config_data.json"

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def human_type(text, delay=0.03):
    """மனிதன் டைப் செய்வது போன்ற உணர்வை தரும் அனிமேஷன்"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def draw_banner():
    print(f"""{C}
    ╔════════════════════════════════════════════╗
    ║                 psycho bot                 ║
    ║════════════════════════════════════════════║
    ║  [+] web       =>      aruble.net          ║
    ║  [+] channel   =>      @psychobot1         ║
    ║  [+] dev       =>      @alphapython12      ║
    ║  [+] message   =>      welcome             ║
    ║ ═══════════════════════════════════════════║
    ║      >>>>>> this is not for sale <<<<<<    ║
    ╚════════════════════════════════════════════╝{E}""")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"user_agent": "", "email": "", "password": ""}

def save_config(data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

# ============================================================
# SUB-MENU: WORK INITIALIZATION
# ============================================================
def start_work_menu():
    config = load_config()
    # தரவுகள் உள்ளதா என்பதை சரிபார்த்தல்
    if not config.get("user_agent") or not config.get("email") or not config.get("password"):
        clear_screen()
        draw_banner()
        print(f"{R}[!] Error: Please set User-Agent and Credentials first!{E}")
        input(f"\n{G}Press Enter to return to main menu...{E}")
        return

    while True:
        clear_screen()
        draw_banner()
        print(f" [1] 𝐅𝐀𝐔𝐂𝐄𝐓 𝐂𝐋𝐀𝐈𝐌")
        print(f" [2] 𝐒𝐇𝐎𝐑𝐓𝐋𝐈𝐍𝐊 𝐁𝐘𝐏𝐀𝐒𝐒")
        print(f" [3] 𝐄𝐗𝐈𝐓\n")
        
        try:
            choice = input(f"{C} ╰┈➤ {E}").strip()
            
            if choice == "1":
                # faucet.py கோப்பை இயக்குகிறது
                try:
                    import faucet
                    faucet.run_faucet()
                except ImportError:
                    print(f"\n{R}[!] Error: faucet.py file not found!{E}")
                    input(f"\n{G}Press Enter to continue...{E}")
                except KeyboardInterrupt:
                    pass # Faucet இலிருந்து Ctrl+C அழுத்தினால் மீண்டும் இந்த மெனுவிற்கே வரும்
                    
            elif choice == "2":
                # shortlink.py கோப்பை இயக்குகிறது
                try:
                    import shortlink
                    shortlink.run_shortlink()
                except ImportError:
                    print(f"\n{R}[!] Error: shortlink.py file not found!{E}")
                    input(f"\n{G}Press Enter to continue...{E}")
                except KeyboardInterrupt:
                    pass
                    
            elif choice == "3":
                break
            else:
                print(f"{R}[!] Invalid option!{E}")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{Y}[!] Returning to main configuration menu...{E}")
            time.sleep(1.5)
            break

# ============================================================
# MAIN MENU LOOP
# ============================================================
def main():
    while True:
        clear_screen()
        draw_banner()
        print(f" [1] set useragent ")
        print(f" [2] set email & password ")
        print(f" [3] start work \n")
        
        try:
            choice = input(f"{C} ╰┈➤ {E}").strip()
            config = load_config()
            
            if choice == "1":
                clear_screen()
                draw_banner()
                current_ua = config.get("user_agent", "")
                if current_ua:
                    print(f"{D}Current UA: {current_ua[:50]}...{E}\n")
                
                ua_input = input(f"{C}enter useragent => {E}").strip()
                if ua_input:
                    config["user_agent"] = ua_input
                    save_config(config)
                    print()
                    human_type(f"{G}[INFO] DATA SAVED SUCCESSFUL{E}")
                else:
                    print(f"\n{R}[!] Cancelled. Value cannot be empty.{E}")
                
                input(f"\n{G}press enter . . . .{E}")
                
            elif choice == "2":
                clear_screen()
                draw_banner()
                current_email = config.get("email", "")
                if current_email:
                    print(f"{D}Current Email: {current_email}{E}\n")
                    
                email_input = input(f"{C}email => {E}").strip()
                password_input = input(f"{C}password => {E}").strip()
                
                if email_input and password_input:
                    config["email"] = email_input
                    config["password"] = password_input
                    save_config(config)
                    print()
                    human_type(f"{G}[INFO] DATA SAVED SUCCESSFUL{E}")
                else:
                    print(f"\n{R}[!] Cancelled. Fields cannot be empty.{E}")
                    
                input(f"\n{G}press enter . . . .{E}")
                
            elif choice == "3":
                start_work_menu()
                
            else:
                print(f"{R}[!] Invalid option!{E}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            clear_screen()
            draw_banner()
            print(f"\n{R}[!] Script Stopped by User. Goodbye!{E}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()

