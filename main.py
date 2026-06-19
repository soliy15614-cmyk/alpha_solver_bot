#!/usr/bin/env python3
import os
import sys
import time
import subprocess

class PsychoUI:
    def __init__(self, typing_speed=0.003):
        self.speed = typing_speed
        self.pri = "\u001b[38;5;147m"
        self.sec = "\u001b[38;5;123m"
        self.gray = "\u001b[38;5;243m"
        self.green = "\u001b[38;5;120m"
        self.red = "\u001b[38;5;204m"
        self.yellow = "\u001b[38;5;223m"
        self.reset = "\u001b[0m"

    def type_text(self, text, color=""):
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.speed)

    def show_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.pri}")
        print(r"   ___  ____ _   _ ____ _  _ ____    ___  ____ ___ ")
        print(r"   |__] |___  \_/  |    |__| |  |    |__] |  |  |  ")
        print(r"   |    ____  |    |___ |  | |__|    |__] |__|  |  ")
        print(f"{self.reset}")
        print(f" {self.gray}├{'─' * 56}┤{self.reset}")
        print(f" {self.gray}│{self.reset}  TEL    {self.gray}:{self.reset} @PSYCHOBOT1     {self.gray}│{self.reset}  DEV    {self.gray}:{self.reset} @ALPHAPYTHON12  {self.gray}│{self.reset}")
        print(f" {self.gray}│{self.reset}  STATUS {self.gray}:{self.reset} {self.green}ONLINE{self.reset}          {self.gray}│{self.reset}  TYPE   {self.gray}:{self.reset} LAUNCHER         {self.gray}│{self.reset}")
        print(f" {self.gray}├{'─' * 56}┤{self.reset}\n")

    def info(self, message):
        self.type_text(f"  {self.gray}• {self.reset}{message}")

    def warning(self, message):
        self.type_text(f"  {self.yellow}! {self.reset}{message}")

    def error(self, message):
        self.type_text(f"  {self.red}× {self.reset}{message}")

    def success(self, message):
        self.type_text(f"  {self.green}✓ {self.reset}{message}")


bot = PsychoUI(typing_speed=0.002)


def launch_bot(script_name):
    bot.show_banner()
    bot.info(f"Launching {script_name}...")
    time.sleep(1)
    try:
        subprocess.run([sys.executable, script_name])
    except KeyboardInterrupt:
        print(f'\n\u001b[33;1m[STOPPED] Returned to main launcher.\u001b[0m')
        time.sleep(1.5)
    except Exception as e:
        bot.error(f"Failed to launch {script_name}: {e}")
        time.sleep(2)


def main_menu():
    while True:
        bot.show_banner()
        print(f"  [1] ALPHA SOLVER")
        print(f"  [2] BOT VIP")
        print(f"  [3] BOT FREE")
        print(f"  [4] Exit\n")
        
        choice = input("  Select option [1-4]: ").strip()
        
        if choice == "1":
            bot.show_banner()
            bot.warning("ALPHA SOLVER is currently not available on this server.")
            bot.info("Please check back later or contact @PSYCHOBOT1")
            time.sleep(3)
        
        elif choice == "2":
            bot.show_banner()
            bot.warning("BOT VIP is currently not available on this server.")
            bot.info("Please check back later or contact @PSYCHOBOT1")
            time.sleep(3)
        
        elif choice == "3":
            free_menu()
        
        elif choice == "4":
            bot.show_banner()
            bot.info("Thank you for using PSYCHO BOT Launcher!")
            time.sleep(1)
            sys.exit(0)
        
        else:
            bot.error("Invalid choice!")
            time.sleep(1)


def free_menu():
    while True:
        bot.show_banner()
        print(f"  {bot.gray}── BOT FREE ──────────────────────────{bot.reset}\n")
        print(f"  [1] earncryptowrs")
        print(f"  [2] Back to Main Menu\n")
        
        choice = input("  Select option [1-2]: ").strip()
        
        if choice == "1":
            if os.path.exists("bot.py"):
                launch_bot("bot.py")
            else:
                bot.show_banner()
                bot.error("bot.py not found in current directory!")
                time.sleep(2)
        
        elif choice == "2":
            return
        
        else:
            bot.error("Invalid choice!")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        bot.show_banner()
        bot.info("Launcher terminated by operator.")
        time.sleep(1)
        sys.exit(0)
