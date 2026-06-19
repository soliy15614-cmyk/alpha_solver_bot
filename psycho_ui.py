import os
import sys
import time

class PsychoUI:
    def __init__(self, typing_speed=0.003):
        self.speed = typing_speed
        self.success_history = []
        
        # Soft Premium Palette
        self.pri = "\u001b[38;5;147m"      
        self.sec = "\u001b[38;5;123m"      
        self.gray = "\u001b[38;5;243m"     
        self.green = "\u001b[38;5;120m"    
        self.red = "\u001b[38;5;204m"      
        self.yellow = "\u001b[38;5;223m"   
        self.reset = "\u001b[0m"
        
        self.brand = "PSYCHO BOT"
        self.author = "VENUJAN"
        self.web = "GIT"
        self.version = "2.0.6"

    def type_text(self, text, color=""):
        """Ultra-fast fluid text generation"""
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.speed)

    def show_banner(self, faucet_name="Multi-Coin Bot"):
        """Clears screen and prints banner with stacked success history"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 'PSYCHO BOT' Slim Line-Art Banner
        print(f"{self.pri}")
        print(r"   ___  ____ _   _ ____ _  _ ____    ___  ____ ___ ")
        print(r"   |__] |___  \_/  |    |__| |  |    |__] |  |  |  ")
        print(r"   |    ____  |    |___ |  | |__|    |__] |__|  |  ")
        print(f"{self.reset}")
        
        # Grid Dashboard
        print(f" {self.gray}┌────────────────────────────────────────────────────────┐{self.reset}")
        print(f" {self.gray}│ {self.reset}Engine   {self.gray}» {self.reset}{faucet_name:<18} {self.gray}│ {self.reset}Version  {self.gray}» {self.sec}{self.version:<10} {self.gray}│{self.reset}")
        print(f" {self.gray}│ {self.reset}Coder    {self.gray}» {self.reset}{self.author:<18} {self.gray}│ {self.reset}Network  {self.gray}» {self.sec}{self.web:<10} {self.gray}│{self.reset}")
        print(f" {self.gray}└────────────────────────────────────────────────────────┘{self.reset}\n")

        # சரிசெய்யப்பட்ட லாக் அடுக்கு அமைப்பு (இப்போது show_banner பங்க்ஷனுக்குள் உள்ளது)
        if self.success_history:
            for past_success in self.success_history:
                print(f" {self.green}[SUCCESS]{self.reset} {past_success}")
                print(f" {self.gray}=================================================={self.reset}")
            print()

    def info(self, message):
        self.type_text(f"  {self.gray}• {self.reset}{message}")

    def warning(self, message):
        self.type_text(f"  {self.yellow}! {self.reset}{message}")

    def error(self, message):
        self.type_text(f"  {self.red}× {self.reset}{message}")

    def success(self, message, faucet_name="Multi-Coin Bot"):
        """Saves message, flushes background log clutter and expands stack"""
        self.success_history.append(message)
        self.show_banner(faucet_name)

    def inline_status(self, text, color="\u001b[38;5;223m"):
        """Temporary inline updates that get overwritten"""
        sys.stdout.write(f"\r  {color}→ {self.reset}{text}")
        sys.stdout.flush()

    def clear_inline(self):
        sys.stdout.write("\r" + " " * 65 + "\r")
        sys.stdout.flush()

    def countdown(self, seconds):
        """Micro-metric modern progress countdown bar"""
        bar_length = 20
        for i in range(seconds + 1):
            percent = (i / seconds) * 100
            filled = int(bar_length * i // seconds)
            bar = '■' * filled + '□' * (bar_length - filled)
            sys.stdout.write(f"\r  {self.yellow}⏳ {self.reset}Interval Control [{self.sec}{bar}{self.reset}] {percent:.0f}%")
            sys.stdout.flush()
            if i < seconds:
                time.sleep(1)
        sys.stdout.write("\r" + " " * 65 + "\r")
        sys.stdout.flush()

