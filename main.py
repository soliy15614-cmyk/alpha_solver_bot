#!/usr/bin/env python3
"""
PSYCHO BOT LAUNCHER - Premium Multi-Bot Launcher v3.0
Minimalist Yet Stunning Design
"""

import os
import sys
import time
import subprocess
import random
import threading
from datetime import datetime

# ============================================================
# PSYCHO UI - Minimalist Premium Framework v3.0
# ============================================================
class PsychoUI:
    def __init__(self):
        # Refined Premium Color Palette
        self.c = {
            'reset':     "\033[0m",
            'bold':      "\033[1m",
            'dim':       "\033[2m",
            'italic':    "\033[3m",
            'underline': "\033[4m",
            'blink':     "\033[5m",
            
            # Primary Colors
            'white':     "\033[97m",
            'black':     "\033[30m",
            
            # Accent Colors
            'purple':    "\033[38;5;99m",
            'lavender':  "\033[38;5;147m",
            'cyan':      "\033[38;5;51m",
            'teal':      "\033[38;5;43m",
            'green':     "\033[38;5;48m",
            'mint':      "\033[38;5;121m",
            'yellow':    "\033[38;5;228m",
            'gold':      "\033[38;5;220m",
            'orange':    "\033[38;5;208m",
            'red':       "\033[38;5;203m",
            'pink':      "\033[38;5;206m",
            'coral':     "\033[38;5;209m",
            
            # Dark Shades
            'dark':      "\033[38;5;236m",
            'gray':      "\033[38;5;243m",
            'silver':    "\033[38;5;249m",
            
            # Background
            'bg_dark':   "\033[48;5;234m",
            'bg_purple': "\033[48;5;55m",
        }

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def cursor_hide(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def cursor_show(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def goto(self, x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def write(self, text, color=None, bold=False, italic=False, end="\n"):
        style = ""
        if bold: style += self.c['bold']
        if italic: style += self.c['italic']
        if color: style += color
        sys.stdout.write(f"{style}{text}{self.c['reset']}{end}")
        sys.stdout.flush()

    def typewrite(self, text, color=None, speed=0.0008):
        """Smooth typewriter effect"""
        style = color if color else self.c['silver']
        for char in text:
            sys.stdout.write(f"{style}{char}{self.c['reset']}")
            sys.stdout.flush()
            time.sleep(speed)

    def loading_ripple(self, duration=2.0, message="Loading"):
        """Ripple loading animation"""
        chars = ["◌", "◍", "●", "◍"]
        start = time.time()
        i = 0
        while time.time() - start < duration:
            sys.stdout.write(f"\r  {self.c['lavender']}{chars[i % len(chars)]} {self.c['silver']}{message}{' .' * (i % 4)}  {self.c['reset']}")
            sys.stdout.flush()
            time.sleep(0.12)
            i += 1
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

    def spinner(self, duration=1.5, message="Processing", color=None):
        """Elegant spinner animation"""
        if not color: color = self.c['lavender']
        frames = ["◜", "◠", "◝", "◞", "◡", "◟"]
        start = time.time()
        i = 0
        while time.time() - start < duration:
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r  {color}{frame} {self.c['silver']}{message}{self.c['reset']}")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
        sys.stdout.write("\r" + " " * 70 + "\r")
        sys.stdout.flush()

    def progress_pulse(self, duration=2.0, message="Loading"):
        """Pulsing progress bar"""
        width = 40
        start = time.time()
        while time.time() - start < duration:
            elapsed = time.time() - start
            progress = min(elapsed / duration, 1.0)
            filled = int(width * progress)
            
            # Gradient effect
            bar = ""
            for j in range(width):
                if j < filled:
                    ratio = j / width
                    if ratio < 0.5:
                        bar += f"{self.c['purple']}█{self.c['reset']}"
                    elif ratio < 0.8:
                        bar += f"{self.c['lavender']}█{self.c['reset']}"
                    else:
                        bar += f"{self.c['cyan']}█{self.c['reset']}"
                else:
                    bar += f"{self.c['dark']}░{self.c['reset']}"
            
            perc = int(progress * 100)
            sys.stdout.write(f"\r  {self.c['silver']}{message}  {bar}  {self.c['gold']}{perc}%{self.c['reset']}")
            sys.stdout.flush()
            time.sleep(0.05)
        print()

    def glow_line(self, width=54, color1=None, color2=None):
        """Single glowing line"""
        if not color1: color1 = self.c['purple']
        if not color2: color2 = self.c['lavender']
        line = ""
        for i in range(width):
            line += f"{color1 if i % 2 == 0 else color2}─"
        return f"{line}{self.c['reset']}"

    def double_glow(self, width=54):
        """Double line with gradient"""
        top = ""
        bottom = ""
        for i in range(width):
            if i < width//3:
                top += f"{self.c['purple']}═"
                bottom += f"{self.c['purple']}═"
            elif i < 2*width//3:
                top += f"{self.c['lavender']}═"
                bottom += f"{self.c['lavender']}═"
            else:
                top += f"{self.c['cyan']}═"
                bottom += f"{self.c['cyan']}═"
        return f"{top}{self.c['reset']}", f"{bottom}{self.c['reset']}"

    def show_banner(self):
        self.clear()
        
        # Top spacing
        print()
        
        # Gradient border top
        top_border, _ = self.double_glow(56)
        print(f"  {top_border}")
        
        # PSYCHO BOT ASCII Art - Clean and Sharp
        lines = [
            "██████╗ ███████╗██╗   ██╗ ██████╗██╗  ██╗ ██████╗",
            "██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██║  ██║██╔═══██╗",
            "██████╔╝███████╗ ╚████╔╝ ██║     ███████║██║   ██║",
            "██╔═══╝ ╚════██║  ╚██╔╝  ██║     ██╔══██║██║   ██║",
            "██║     ███████║   ██║   ╚██████╗██║  ██║╚██████╔╝",
            "╚═╝     ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝ ╚═════╝"
        ]
        
        # Color gradient for each line
        line_colors = [
            self.c['purple'], self.c['lavender'], self.c['cyan'],
            self.c['cyan'], self.c['lavender'], self.c['purple']
        ]
        
        for line, color in zip(lines, line_colors):
            # Subtle shadow effect
            sys.stdout.write(f"  {self.c['dim']}{self.c['dark']}{line}{self.c['reset']}")
            time.sleep(0.015)
            sys.stdout.write(f"\r  {color}{self.c['bold']}{line}{self.c['reset']}\n")
            time.sleep(0.01)
        
        # Info bar - Clean minimal
        print(f"  {self.c['dark']}{'─'*56}{self.c['reset']}")
        
        now = datetime.now().strftime("%H:%M")
        date = datetime.now().strftime("%d.%m.%Y")
        
        info = f" {self.c['silver']}⌚ {now}  {self.c['dark']}│  {self.c['silver']}📅 {date}  {self.c['dark']}│  {self.c['lavender']}v3.0  {self.c['dark']}│  {self.c['green']}● online"
        sys.stdout.write(f"  {info}{self.c['reset']}\n")
        
        dev_info = f" {self.c['silver']}dev{self.c['dark']}@{self.c['lavender']}alphapython12  {self.c['dark']}│  {self.c['silver']}ch{self.c['dark']}@{self.c['cyan']}psychobot1"
        sys.stdout.write(f"  {dev_info}{self.c['reset']}\n")
        
        print(f"  {self.c['dark']}{'─'*56}{self.c['reset']}")
        print()

    def show_mini_banner(self, title, subtitle=""):
        """Minimal header for sub-menus"""
        top, bottom = self.double_glow(54)
        print(f"\n  {top}")
        sys.stdout.write(f"  {self.c['bold']}{self.c['lavender']}  {title}{self.c['reset']}")
        if subtitle:
            sys.stdout.write(f"  {self.c['dim']}{self.c['dark']}─ {subtitle}")
        print()
        print(f"  {bottom}\n")

    def menu_option(self, key, label, color=None, highlight=False):
        """Single clean menu option"""
        if not color: color = self.c['silver']
        
        if highlight:
            sys.stdout.write(f"  {self.c['purple']}▸{self.c['reset']} {self.c['bold']}{color}[{key}]{self.c['reset']}  {self.c['bold']}{color}{label}{self.c['reset']}")
        else:
            sys.stdout.write(f"  {self.c['dim']} {self.c['dark']}▸{self.c['reset']} {self.c['lavender']}[{key}]{self.c['reset']}  {color}{label}{self.c['reset']}")
        print()

    def separator(self, char="·", count=54):
        """Subtle separator"""
        line = char * count
        print(f"  {self.c['dark']}{line}{self.c['reset']}")

    def show_alpha_solver_online(self):
        """Special display for ALPHA SOLVER - Online Only"""
        self.clear()
        self.show_banner()
        
        top, bottom = self.double_glow(54)
        print(f"  {top}")
        
        # Animated ONLINE status
        print(f"  {self.c['bold']}{self.c['purple']}  🔐 ALPHA SOLVER{self.c['reset']}")
        print(f"  {self.c['dark']}{'─'*54}{self.c['reset']}")
        
        # Pulsing ONLINE text
        for _ in range(3):
            sys.stdout.write(f"\r  {self.c['green']}  ● {self.c['bold']}{self.c['green']}ONLINE ONLY{self.c['reset']}  ")
            sys.stdout.flush()
            time.sleep(0.4)
            sys.stdout.write(f"\r  {self.c['dark']}  ● ONLINE ONLY{self.c['reset']}  ")
            sys.stdout.flush()
            time.sleep(0.4)
        
        sys.stdout.write(f"\r  {self.c['green']}  ● {self.c['bold']}{self.c['green']}ONLINE ONLY{self.c['reset']}     {self.c['dark']}(Server Active){self.c['reset']}\n")
        
        print(f"  {self.c['dark']}{'─'*54}{self.c['reset']}")
        print(f"\n  {self.c['silver']}  This solver runs exclusively on our server.{self.c['reset']}")
        print(f"  {self.c['silver']}  Direct access required. No local execution.{self.c['reset']}")
        print(f"\n  {self.c['dark']}{'─'*54}{self.c['reset']}")
        print(f"  {self.c['lavender']}  Contact » {self.c['cyan']}@PSYCHOBOT1{self.c['reset']}")
        print(f"  {self.c['lavender']}  Status  » {self.c['green']}Active & Running{self.c['reset']}")
        print(f"  {bottom}\n")
        
        self.separator()
        input(f"  {self.c['silver']}  Press Enter to return...{self.c['reset']}")

    def show_vip_status(self):
        """Special display for BOT VIP - Online Only"""
        self.clear()
        self.show_banner()
        
        top, bottom = self.double_glow(54)
        print(f"  {top}")
        print(f"  {self.c['bold']}{self.c['gold']}  👑 BOT VIP{self.c['reset']}")
        print(f"  {self.c['dark']}{'─'*54}{self.c['reset']}")
        
        for _ in range(2):
            sys.stdout.write(f"\r  {self.c['gold']}  ◆ {self.c['bold']}{self.c['gold']}PREMIUM ACCESS ONLY{self.c['reset']}  ")
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write(f"\r  {self.c['dark']}  ◆ PREMIUM ACCESS ONLY{self.c['reset']}  ")
            sys.stdout.flush()
            time.sleep(0.3)
        
        sys.stdout.write(f"\r  {self.c['gold']}  ◆ {self.c['bold']}{self.c['gold']}PREMIUM ACCESS ONLY{self.c['reset']}\n")
        
        print(f"  {self.c['dark']}{'─'*54}{self.c['reset']}")
        print(f"\n  {self.c['silver']}  Exclusive bots for premium members.{self.c['reset']}")
        print(f"  {self.c['silver']}  Upgrade required for access.{self.c['reset']}")
        print(f"\n  {self.c['dark']}{'─'*54}{self.c['reset']}")
        print(f"  {self.c['lavender']}  Contact » {self.c['cyan']}@PSYCHOBOT1{self.c['reset']}")
        print(f"  {self.c['gold']}  Type    » Premium{self.c['reset']}")
        print(f"  {bottom}\n")
        
        self.separator()
        input(f"  {self.c['silver']}  Press Enter to return...{self.c['reset']}")


# Create global UI instance
ui = PsychoUI()
c = ui.c


# ============================================================
# BOT LAUNCHER FUNCTIONS
# ============================================================

def launch_bot(script_name, display_name, emoji=""):
    """Launch a bot with beautiful animations"""
    ui.clear()
    ui.show_banner()
    ui.show_mini_banner(f"{emoji} Launching {display_name}", "Initializing engine")
    
    ui.spinner(0.8, "Checking files", c['lavender'])
    
    if not os.path.exists(script_name):
        ui.clear()
        ui.show_banner()
        ui.show_mini_banner("File Not Found", script_name)
        sys.stdout.write(f"  {c['red']}  ✘ '{script_name}' missing{c['reset']}\n")
        sys.stdout.write(f"  {c['silver']}  Place file in current directory{c['reset']}\n")
        ui.separator()
        time.sleep(2.5)
        return
    
    ui.progress_pulse(1.5, "Loading modules")
    sys.stdout.write(f"  {c['green']}  ✔ Ready{c['reset']}\n")
    time.sleep(0.5)
    
    try:
        subprocess.run([sys.executable, script_name])
    except KeyboardInterrupt:
        print(f'\n  {c["yellow"]}  ◈ Stopped - Returned to launcher{c["reset"]}')
        time.sleep(1.5)
    except Exception as e:
        ui.clear()
        ui.show_banner()
        sys.stdout.write(f"  {c['red']}  ✘ Error: {e}{c['reset']}\n")
        time.sleep(2.5)


def launch_earncrypto():
    launch_bot("bot.py", "EarnCryptoWrs", "")

def launch_coinpayu():
    launch_bot("coin.py", "CoinPayuFree", "")

def launch_altcryp():
    launch_bot("altcryp.py", "Altcryp", "")

def launch_mixcrypto():
    launch_bot("mix.py", "Mix-Crypto-BTC", "")

def launch_claimcoin():
    launch_bot("cc.py", "ClaimCoin.in", "")

def launch_tfaucet():
    launch_bot("tf.py", "TFaucet", "")

def launch_taraking():
    launch_bot("tk.py", "TaraKing", "")


# ============================================================
# MENU SYSTEM
# ============================================================

def main_menu():
    while True:
        ui.show_banner()
        
        # Menu with clean typography
        sys.stdout.write(f"  {c['bold']}{c['lavender']}  ▸ MAIN MENU{c['reset']}\n")
        ui.separator()
        
        options = [
            ("1", "ALPHA SOLVER",  c['purple'], True),
            ("2", "BOT VIP",       c['gold']),
            ("3", "BOT FREE",      c['cyan']),
            ("4", "EXIT",          c['red']),
        ]
        
        for key, label, color, *highlight in options:
            h = highlight[0] if highlight else False
            ui.menu_option(key, label, color, h)
        
        ui.separator()
        
        choice = input(f"  {c['lavender']}  select {c['dark']}»{c['reset']} ").strip()
        
        if choice == '1':
            ui.show_alpha_solver_online()
        elif choice == '2':
            ui.show_vip_status()
        elif choice == '3':
            free_menu()
        elif choice == '4':
            ui.clear()
            ui.show_banner()
            ui.show_mini_banner("Goodbye", "See you soon")
            ui.spinner(1.0, "Shutting down", c['lavender'])
            sys.stdout.write(f"  {c['silver']}  Launcher closed{c['reset']}\n\n")
            time.sleep(0.5)
            sys.exit(0)
        else:
            sys.stdout.write(f"  {c['red']}  Invalid choice{c['reset']}\n")
            time.sleep(0.8)


def free_menu():
    while True:
        ui.show_banner()
        
        sys.stdout.write(f"  {c['bold']}{c['cyan']}  ▸ BOT FREE{c['reset']}\n")
        ui.separator()
        
        bot_options = [
            ("1", "EarnCryptoWrs",    c['mint']),
            ("2", "CoinPayuFree",     c['teal']),
            ("3", "Altcryp",          c['cyan']),
            ("4", "Mix Crypto BTC",   c['lavender']),
            ("5", "ClaimCoin.in",     c['pink']),
            ("6", "TFaucet",          c['orange']),
            ("7", "TaraKing",         c['coral']),
            ("8", "« Back",           c['gray']),
        ]
        
        for key, label, color in bot_options:
            ui.menu_option(key, label, color)
        
        ui.separator()
        
        choice = input(f"  {c['cyan']}  select {c['dark']}»{c['reset']} ").strip()
        
        actions = {
            '1': launch_earncrypto,
            '2': launch_coinpayu,
            '3': launch_altcryp,
            '4': launch_mixcrypto,
            '5': launch_claimcoin,
            '6': launch_tfaucet,
            '7': launch_taraking,
            '8': lambda: None,
        }
        
        if choice in actions:
            if choice == '8':
                return
            actions[choice]()
        else:
            sys.stdout.write(f"  {c['red']}  Invalid choice{c['reset']}\n")
            time.sleep(0.8)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    try:
        ui.cursor_hide()
        main_menu()
    except KeyboardInterrupt:
        ui.clear()
        ui.show_banner()
        sys.stdout.write(f"  {c['silver']}  Interrupted by user{c['reset']}\n\n")
        time.sleep(0.8)
        sys.exit(0)
    finally:
        ui.cursor_show()
