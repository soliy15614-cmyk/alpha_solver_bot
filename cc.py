#!/usr/bin/env python3
"""
ClaimCoin Bot - Complete Automation Script (Fixed)
"""

import os
import sys
import time
import json
import re
import random
import requests
from bs4 import BeautifulSoup
from html import unescape

# ============================================================
# PSYCHO UI - Premium UI Framework
# ============================================================
class PsychoUI:
    def __init__(self, typing_speed=0.002):
        self.speed = typing_speed
        self.success_history = []
        self.max_history = 999999
        self.show_success = True
        
        # Premium Color Palette
        self.pri = "\033[38;5;147m"
        self.sec = "\033[38;5;123m"
        self.gray = "\033[38;5;243m"
        self.green = "\033[38;5;120m"
        self.red = "\033[38;5;204m"
        self.yellow = "\033[38;5;223m"
        self.gold = "\033[38;5;220m"
        self.pink = "\033[38;5;212m"
        self.orange = "\033[38;5;214m"
        self.purple = "\033[38;5;135m"
        self.reset = "\033[0m"
        
        self.brand = "PSYCHO BOT"
        self.author = "VENUJAN"
        self.web = "GIT"
        self.version = "3.0.0"

    def type_text(self, text, color="", delay=0.001):
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    def show_banner(self, faucet_name="ClaimCoin"):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        colors = ['\033[38;5;147m', '\033[38;5;123m', '\033[38;5;220m']
        banner_lines = [
            r"   ██████╗ ███████╗██╗   ██╗ ██████╗██╗  ██╗ ██████╗",
            r"   ██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██║  ██║██╔═══██╗",
            r"   ██████╔╝███████╗ ╚████╔╝ ██║     ███████║██║   ██║",
            r"   ██╔═══╝ ╚════██║  ╚██╔╝  ██║     ██╔══██║██║   ██║",
            r"   ██║     ███████║   ██║   ╚██████╗██║  ██║╚██████╔╝",
            r"   ╚═╝     ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝ ╚═════╝ "
        ]
        
        for line in banner_lines:
            print(f"{colors[0]}{line}{self.reset}")
            time.sleep(0.02)
        
        print()
        
        print(f" {self.gray}┌──────────────────────────────────────────────────────────────┐{self.reset}")
        print(f" {self.gray}│ {self.reset}Engine   {self.gray}» {self.gold}{faucet_name:<20} {self.gray}│ {self.reset}Version  {self.gray}» {self.sec}{self.version:<10} {self.gray}│{self.reset}")
        print(f" {self.gray}│ {self.reset}Coder    {self.gray}» {self.pink}{self.author:<20} {self.gray}│ {self.reset}Network  {self.gray}» {self.sec}{self.web:<10} {self.gray}│{self.reset}")
        print(f" {self.gray}└──────────────────────────────────────────────────────────────┘{self.reset}\n")

        if self.show_success and self.success_history:
            for past_success in self.success_history:
                print(f" {self.green}[SUCCESS]{self.reset} {past_success}")
                print(f" {self.gray}────────────────────────────────────────────────────────────{self.reset}")
            print()

    def info(self, message):
        self.type_text(f"  {self.gray}• {self.reset}{message}", self.gray, 0.001)

    def warning(self, message):
        self.type_text(f"  {self.yellow}! {self.reset}{message}", self.yellow, 0.002)

    def error(self, message):
        self.type_text(f"  {self.red}× {self.reset}{message}", self.red, 0.002)

    def success(self, message, faucet_name="ClaimCoin"):
        self.success_history.append(message)
        self.show_success = True
        self.show_banner(faucet_name)
    
    def show_menu_banner(self, faucet_name="ClaimCoin"):
        self.show_success = False
        self.show_banner(faucet_name)
    
    def show_work_banner(self, faucet_name="ClaimCoin"):
        self.show_success = True
        self.show_banner(faucet_name)

    def inline_status(self, text, color="\033[38;5;223m"):
        max_len = 80
        if len(text) > max_len:
            text = text[:max_len-3] + "..."
        sys.stdout.write(f"\r  {color}→ {self.reset}{text}")
        sys.stdout.flush()

    def clear_inline(self):
        sys.stdout.write("\r" + " " * 90 + "\r")
        sys.stdout.flush()

    def countdown(self, seconds, label="Interval Control"):
        if seconds <= 0:
            return
        
        bar_length = 30
        for i in range(seconds + 1):
            percent = (i / seconds) * 100
            filled = int(bar_length * i // seconds)
            bar = '■' * filled + '□' * (bar_length - filled)
            sys.stdout.write(f"\r  {self.yellow}⏳ {self.reset}{label} [{self.sec}{bar}{self.reset}] {self.gold}{percent:.0f}%{self.reset}")
            sys.stdout.flush()
            if i < seconds:
                time.sleep(1)
        sys.stdout.write("\r" + " " * 90 + "\r")
        sys.stdout.flush()

bot = PsychoUI(typing_speed=0.002)

# ============================================================
# COLOR CODES FOR MENU
# ============================================================
C = {
    'header': '\033[38;5;147m',
    'menu': '\033[38;5;123m',
    'green': '\033[38;5;120m',
    'red': '\033[38;5;204m',
    'yellow': '\033[38;5;223m',
    'gray': '\033[38;5;243m',
    'gold': '\033[38;5;220m',
    'pink': '\033[38;5;212m',
    'orange': '\033[38;5;214m',
    'purple': '\033[38;5;135m',
    'reset': '\033[0m'
}

# ============================================================
# CONFIGURATION
# ============================================================
DOMAIN = "https://claimcoin.in"
LOGIN_URL = f"{DOMAIN}/login"
LOGIN_ACTION = f"{DOMAIN}/auth/login"
DASHBOARD_URL = f"{DOMAIN}/dashboard"
FAUCET_URL = f"{DOMAIN}/faucet"
FAUCET_VERIFY = f"{DOMAIN}/faucet/verify"

RECAPTCHA_SITEKEY = "6LdnVw4qAAAAAFPMxvegAK9JcBflI-0tb8YKMxZU"
RECAPTCHA_API = "https://bypassallshortlinks.space/rv3.php"
ANTIBOT_API = "https://bypassallshortlinks.space/api.php"

SESSION_FILE = "claimcoin_session.json"
CONFIG_FILE = "claimcoin_config.json"
ANTIBOT_KEY = "X1iRqWL1pv1bpvHRfvqeXxQqYhcERDti"

# ============================================================
# SESSION & CONFIG
# ============================================================
def save_session(cookies_dict, user_agent):
    data = {"cookies": cookies_dict, "user_agent": user_agent, "saved_at": time.time()}
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)
        return True
    except Exception:
        return False

def load_session():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception:
        pass

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "email": "",
        "password": "",
        "antibot_key": "",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

def get_input_with_default(prompt, default=""):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    value = input(prompt).strip()
    return value if value else default

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================================
# RECAPTCHA V3 SOLVER
# ============================================================
def solve_recaptcha_v3(sitekey, pageurl):
    """Solve reCAPTCHA v3 using bypassallshortlinks API"""
    bot.inline_status("Solving reCAPTCHA v3...")
    
    try:
        payload = {
            "site_key": sitekey,
            "site_url": pageurl
        }
        
        resp = requests.post(RECAPTCHA_API, json=payload, timeout=30)
        result = resp.json()
        
        if result and result.get("token"):
            token = result.get("token")
            bot.clear_inline()
            bot.info("reCAPTCHA v3 solved")
            return token
        else:
            bot.warning("Failed to solve reCAPTCHA v3")
            return None
            
    except Exception as e:
        bot.warning(f"reCAPTCHA error: {str(e)}")
        return None

# ============================================================
# ANTI-BOT SOLVER - ROBUST VERSION (CoinPayu Logic)
# ============================================================
def solve_antibot(html, antibot_key):
    """
    Solve anti-bot images using bypassallshortlinks API
    Robust extraction with multiple fallback methods
    """
    bot.inline_status("Solving Anti-Bot...")
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # STEP 1: Find main instruction image
        main_base64 = None
        
        # Try alert-warning div first
        alert = soup.find('div', class_='alert-warning')
        if not alert:
            alert = soup.find('p', class_='alert-warning')
        if not alert:
            alert = soup.find('div', id='atb-instruction')
        
        if alert:
            main_img = alert.find('img')
            if main_img and 'src' in main_img.attrs:
                src = main_img['src']
                if 'base64,' in src:
                    main_base64 = src.split('base64,')[1]
                    bot.inline_status(f"Main image found: {len(main_base64)} chars")
        
        if not main_base64:
            # Try any img with base64
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if 'base64,' in src:
                    main_base64 = src.split('base64,')[1]
                    break
        
        if not main_base64:
            bot.error("Main instruction image not found")
            return None
        
        # STEP 2: Find ablinks script
        script_tag = None
        for script in soup.find_all('script'):
            if script.string and 'ablinks' in script.string:
                script_tag = script
                break
        
        if not script_tag:
            bot.error("ablinks script not found")
            return None
        
        script_text = script_tag.string
        bot.inline_status(f"Script found: {len(script_text)} chars")
        
        # STEP 3: Extract rel values and base64 images
        rels = []
        images = []
        
        # Method 1: Standard double quotes
        pattern1 = re.findall(
            r'rel\s*=\s*["\'](\d+)["\'].*?src\s*=\s*["\']data:image/png;base64,([^"\']+)["\']',
            script_text, 
            re.DOTALL
        )
        
        # Method 2: Escaped quotes (JavaScript string)
        pattern2 = re.findall(
            r'rel\s*=\s*\\"(\d+)\\".*?src\s*=\s*\\"data:image/png;base64,([^\\]+)\\',
            script_text, 
            re.DOTALL
        )
        
        # Method 3: HTML entity encoded quotes
        pattern3 = re.findall(
            r'rel\s*=\s*&quot;(\d+)&quot;.*?src\s*=\s*&quot;data:image/png;base64,([^&]+)&quot;',
            script_text, 
            re.DOTALL
        )
        
        # Method 4: Separate extraction (rel and image individually)
        if not pattern1 and not pattern2 and not pattern3:
            bot.inline_status("Using separate extraction...")
            all_rels = re.findall(r'rel\s*=\s*["\']?(\d+)["\']?', script_text)
            all_images = re.findall(r'data:image/png;base64,([^"\'\s\\]+)', script_text)
            
            # Clean escaped characters from images
            all_images = [img.replace('\\', '') for img in all_images]
            
            bot.inline_status(f"Separate: {len(all_rels)} rels, {len(all_images)} images")
            
            if all_rels and all_images:
                # Filter out instruction image if it appears in options
                filtered_images = []
                for img in all_images:
                    if len(img) > 50 and img[:30] != main_base64[:30]:
                        filtered_images.append(img)
                
                if len(filtered_images) >= len(all_rels):
                    images = filtered_images[:len(all_rels)]
                    rels = all_rels
                elif len(all_images) >= len(all_rels):
                    images = all_images[-len(all_rels):]
                    rels = all_rels
                elif len(all_rels) == len(all_images):
                    rels = all_rels
                    images = all_images
        
        # Process pattern results
        if pattern1:
            rels = [p[0] for p in pattern1]
            images = [p[1] for p in pattern1]
        elif pattern2:
            rels = [p[0] for p in pattern2]
            images = [p[1].replace('\\', '') for p in pattern2]
        elif pattern3:
            rels = [p[0] for p in pattern3]
            images = [p[1] for p in pattern3]
        
        bot.inline_status(f"Extracted: {len(rels)} rels, {len(images)} images")
        
        # STEP 4: Validate
        if len(rels) < 2 or len(images) < 2:
            bot.error(f"Not enough options (rels:{len(rels)}, images:{len(images)})")
            return None
        
        # Equalize lengths
        min_len = min(len(rels), len(images))
        rels = rels[:min_len]
        images = images[:min_len]
        
        # STEP 5: Build API payload
        options = {}
        rel_mapping = {}
        
        for i, (rel, img_data) in enumerate(zip(rels, images), start=1):
            options[str(i)] = img_data
            rel_mapping[str(i)] = rel
        
        api_payload = {
            'api_key': antibot_key,
            'action': 'antibot',
            'main': main_base64,
            'options': options
        }
        
        # STEP 6: Call API
        bot.inline_status("Calling AntiBot API...")
        resp = requests.post(ANTIBOT_API, json=api_payload, timeout=30)
        task_resp = resp.text.strip()
        bot.inline_status(f"API response: {task_resp[:60]}")
        
        order_string = None
        
        # Handle task-based response
        if "id" in task_resp.lower() or task_resp.isdigit():
            task_id = re.sub(r'[^0-9]', '', task_resp)
            if task_id:
                poll_url = f"https://bypassallshortlinks.space/res.php?id={task_id}&key={antibot_key}&action=get"
                for attempt in range(30):
                    time.sleep(3)
                    try:
                        poll_resp = requests.get(poll_url, timeout=10)
                        poll_result = poll_resp.text.strip()
                        bot.inline_status(f"Poll {attempt+1}/30: {poll_result[:50]}")
                        
                        if "NOTREADY" in poll_result.upper():
                            continue
                        elif "ERROR" in poll_result.upper():
                            if "UNSOLVABLE" in poll_result.upper():
                                break
                            continue
                        elif poll_result and ',' in poll_result:
                            order_string = poll_result
                            break
                    except Exception:
                        continue
        else:
            if ',' in task_resp:
                order_string = task_resp
        
        bot.clear_inline()
        
        # STEP 7: Process result
        if order_string and ',' in order_string:
            indices = [x.strip() for x in order_string.split(',')]
            final_order = []
            for idx in indices:
                if idx in rel_mapping:
                    final_order.append(rel_mapping[idx])
            
            if len(final_order) == len(rels):
                result = " " + " ".join(final_order)
                bot.info(f"AntiBot solved: {result}")
                return result
            else:
                bot.warning(f"API returned {len(final_order)} values, expected {len(rels)}")
        
        # STEP 8: Fallback - numerical sort
        bot.warning("API didn't return valid order, using numerical sort")
        sorted_rels = sorted(rels, key=lambda x: int(x))
        result = " " + " ".join(sorted_rels)
        bot.info(f"Fallback order: {result}")
        return result
        
    except Exception as e:
        bot.error(f"AntiBot error: {str(e)}")
        return None

# ============================================================
# MAIN BOT
# ============================================================
class ClaimCoinBot:
    def __init__(self, config):
        self.config = config
        self.email = config.get("email", "")
        self.password = config.get("password", "")
        self.antibot_key = config.get("antibot_key", "")
        self.user_agent = config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        saved = load_session()
        if saved and saved.get("user_agent"):
            self.user_agent = saved["user_agent"]
            for name, value in saved["cookies"].items():
                self.session.cookies.set(name, value, domain="claimcoin.in")
        
        self.logged_in = False
        self.balance = 0
        self.username = ""
        self.total_claimed = 0
        
    def _headers(self, extra=None):
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': DOMAIN,
        }
        if extra:
            headers.update(extra)
        return headers
    
    def _get_csrf(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            csrf = soup.find('input', {'name': 'csrf_token_name'})
            if csrf and csrf.get('value'):
                return csrf.get('value')
            csrf = soup.find('input', {'id': 'token'})
            if csrf and csrf.get('value'):
                return csrf.get('value')
            return None
        except Exception:
            return None
    
    def _get_balance(self, html):
        try:
            match = re.search(r'<h2>([\d,]+)\s*CCP</h2>', html)
            if match:
                return float(match.group(1).replace(',', ''))
            return 0
        except Exception:
            return 0
    
    def _get_username(self, html):
        try:
            match = re.search(r'key="t-henry">([^<]+)</span>', html)
            if match:
                return match.group(1).strip()
            return None
        except Exception:
            return None
    
    def _get_timer(self, html):
        try:
            match = re.search(r'class="badge bg-primary counter" wait="(\d+)"', html)
            if match:
                return int(match.group(1))
            return 0
        except Exception:
            return 0
    
    def _get_swal_message(self, html):
        try:
            match = re.search(r"Swal\.fire\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)", html)
            if match:
                return {"title": match.group(1), "text": match.group(2), "icon": match.group(3)}
            return None
        except Exception:
            return None
    
    def is_logged_in(self):
        try:
            resp = self.session.get(DASHBOARD_URL, headers=self._headers(), timeout=10)
            if resp.status_code == 200:
                if '<title>Dashboard' in resp.text:
                    self.logged_in = True
                    self.balance = self._get_balance(resp.text)
                    self.username = self._get_username(resp.text)
                    return True
            return False
        except Exception:
            return False
    
    def login(self):
        bot.info("Logging in...")
        
        try:
            resp = self.session.get(LOGIN_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                bot.error("Failed to load login page")
                return False
            
            html = resp.text
            csrf = self._get_csrf(html)
            if not csrf:
                bot.error("CSRF token not found")
                return False
            
            bot.info(f"CSRF Token: {csrf}")
            
            payload = {
                'csrf_token_name': csrf,
                'email': self.email,
                'password': self.password
            }
            
            time.sleep(random.uniform(1, 2))
            
            resp = self.session.post(
                LOGIN_ACTION,
                data=payload,
                headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}),
                timeout=30,
                allow_redirects=True
            )
            
            if '<title>Dashboard' in resp.text or '/dashboard' in resp.url:
                cookies = self.session.cookies.get_dict()
                save_session(cookies, self.user_agent)
                self.logged_in = True
                self.balance = self._get_balance(resp.text)
                self.username = self._get_username(resp.text)
                bot.success(f"Login Success! User: {self.username}", "ClaimCoin")
                bot.info(f"Balance: {self.balance} CCP")
                return True
            
            error_match = re.search(r'<div class="alert alert-danger">([^<]+)</div>', resp.text)
            if error_match:
                bot.error(f"Login failed: {error_match.group(1)}")
            else:
                bot.error("Login failed")
            
            return False
            
        except Exception as e:
            bot.error(f"Login error: {str(e)}")
            return False
    
    def ensure_logged_in(self):
        if self.is_logged_in():
            return True
        return self.login()
    
    def claim_faucet(self):
        try:
            resp = self.session.get(FAUCET_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                bot.warning("Failed to load faucet page")
                return False
            
            html = resp.text
            
            if 'READY' not in html:
                wait_time = self._get_timer(html)
                if wait_time > 0:
                    bot.info(f"Faucet cooldown: {wait_time}s")
                    bot.countdown(wait_time + 2, "Faucet Timer")
                    return self.claim_faucet()
                else:
                    bot.warning("Faucet not ready")
                    return False
            
            csrf = self._get_csrf(html)
            if not csrf:
                bot.warning("CSRF token not found")
                return False
            
            bot.info(f"CSRF Token: {csrf}")
            
            # Solve AntiBot using robust solver
            antibot = solve_antibot(html, self.antibot_key)
            if not antibot:
                bot.warning("Failed to solve AntiBot")
                return False
            
            # Solve reCAPTCHA v3
            recaptcha_token = solve_recaptcha_v3(RECAPTCHA_SITEKEY, FAUCET_URL)
            if not recaptcha_token:
                return False
            
            payload = {
                'captcha': 'recaptchav3',
                'recaptchav3': recaptcha_token,
                'antibotlinks': antibot,
                'csrf_token_name': csrf
            }
            
            time.sleep(random.uniform(1, 2))
            
            resp = self.session.post(
                FAUCET_VERIFY,
                data=payload,
                headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}),
                timeout=30,
                allow_redirects=True
            )
            
            swal = self._get_swal_message(resp.text)
            if swal and swal['icon'] == 'success':
                self.total_claimed += 1
                bot.success(f"Good job! {swal['text']}", "ClaimCoin")
                self.balance = self._get_balance(resp.text)
                return True
            
            wait_time = self._get_timer(resp.text)
            if wait_time > 0:
                bot.info(f"Next claim in: {wait_time}s")
                return "cooldown"
            
            error_match = re.search(r'<div class="alert alert-danger">([^<]+)</div>', resp.text)
            if error_match:
                bot.warning(f"Claim failed: {error_match.group(1)}")
            else:
                bot.warning("Claim failed")
            
            return False
            
        except Exception as e:
            bot.warning(f"Faucet error: {str(e)}")
            return False
    
    def run(self):
        bot.show_work_banner("ClaimCoin")
        
        if not self.email or not self.password:
            bot.error("Email and Password are required!")
            input("\nPress Enter to continue...")
            return
        
        if not self.antibot_key:
            bot.error("AntiBot API Key is required!")
            bot.info("Please set AntiBot API Key in settings.")
            input("\nPress Enter to continue...")
            return
        
        if not self.ensure_logged_in():
            bot.error("Login failed!")
            input("\nPress Enter to continue...")
            return
        
        bot.info(f"Balance: {self.balance} CCP")
        bot.info(f"User: {self.username}")
        
        cycle = 0
        
        while True:
            cycle += 1
            bot.info(f"--- Cycle {cycle} ---")
            bot.info(f"Total claims: {self.total_claimed}")
            
            if not self.is_logged_in():
                bot.info("Session expired. Re-logging...")
                if not self.login():
                    bot.error("Re-login failed!")
                    input("\nPress Enter to continue...")
                    break
            
            result = self.claim_faucet()
            
            if result == "cooldown":
                continue
            elif result == True:
                continue
            else:
                bot.info("Retrying in 30s...")
                bot.countdown(30, "Retry")

# ============================================================
# MENU FUNCTIONS
# ============================================================
def print_header(text):
    print(f"{C['header']}{'═'*55}{C['reset']}")
    print(f"{C['header']}  {text}{C['reset']}")
    print(f"{C['header']}{'═'*55}{C['reset']}")

def print_menu_option(key, value):
    print(f"  {C['menu']}▶ [{key}]{C['reset']} {value}")

def print_info(text):
    print(f"  {C['gray']}• {C['reset']}{text}")

def print_success(text):
    print(f"  {C['green']}✔ {C['reset']}{text}")

def print_error(text):
    print(f"  {C['red']}✘ {C['reset']}{text}")

def print_warning(text):
    print(f"  {C['yellow']}⚠ {C['reset']}{text}")

def print_instruction(text):
    print(f"  {C['orange']}ℹ {C['reset']}{text}")

def get_menu_choice(prompt, options):
    print(f"\n{C['gold']}{prompt}{C['reset']}")
    print(f"{C['gray']}{'─'*55}{C['reset']}")
    for key, value in options.items():
        print_menu_option(key, value)
    print(f"{C['gray']}{'─'*55}{C['reset']}")
    while True:
        choice = input(f"{C['menu']}Select option: {C['reset']}").strip()
        if choice in options:
            return choice
        print_error("Invalid option. Please try again.")

def show_main_menu():
    clear_screen()
    bot.show_menu_banner("ClaimCoin")
    print_header("ClaimCoin Bot")
    
    menu_options = {
        '1': 'Set User Agent',
        '2': 'Set Account (Email & Password)',
        '3': 'Set BAS_API_KEY [ONLY FOR ANTI BOT]',
        '4': 'Start work',
        '5': 'Exit'
    }
    return get_menu_choice("Main Menu:", menu_options)

def set_account_menu(config):
    clear_screen()
    bot.show_menu_banner("ClaimCoin")
    print_header("Set Account")
    print_instruction("Enter your ClaimCoin email and password.")
    print()
    
    email = get_input_with_default("Email", config.get('email', ''))
    password = get_input_with_default("Password", config.get('password', ''))
    
    config['email'] = email
    config['password'] = password
    save_config(config)
    print_success("Email updated")
    print_success("Password updated")
    input("\nPress Enter to continue...")

def set_antibot_menu(config):
    clear_screen()
    bot.show_menu_banner("ClaimCoin")
    print_header("Set AntiBot API Key")
    print_instruction("Enter your AntiBot API Key for solving anti-bot images.")
    print()
    
    api_key = get_input_with_default("AntiBot API Key", config.get('antibot_key', ''))
    config['antibot_key'] = api_key
    save_config(config)
    print_success("AntiBot API Key updated")
    input("\nPress Enter to continue...")

def main():
    config = load_config()
    
    while True:
        try:
            choice = show_main_menu()
            
            if choice == '1':
                clear_screen()
                bot.show_menu_banner("ClaimCoin")
                print_header("Set User Agent")
                current = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                new_ua = get_input_with_default("Enter User Agent", current)
                config['user_agent'] = new_ua
                save_config(config)
                print_success("User Agent updated")
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                set_account_menu(config)
                
            elif choice == '3':
                set_antibot_menu(config)
                
            elif choice == '4':
                clear_screen()
                bot.show_menu_banner("ClaimCoin")
                
                if not config.get('email') or not config.get('password'):
                    print_error("Email and Password are required!")
                    input("\nPress Enter to continue...")
                    continue
                
                if not config.get('antibot_key'):
                    print_error("AntiBot API Key is required!")
                    input("\nPress Enter to continue...")
                    continue
                
                bot_obj = ClaimCoinBot(config)
                
                try:
                    bot_obj.run()
                except KeyboardInterrupt:
                    bot.clear_inline()
                    print(f'\n{C["yellow"]}[STOPPED] Bot safely terminated.{C["reset"]}')
                    time.sleep(1.5)
                except Exception as e:
                    bot.error(f"Bot error: {str(e)}")
                    input("\nPress Enter to continue...")
                
            elif choice == '5':
                print(f"\n{C['yellow']}Exiting...{C['reset']}")
                break
                
        except KeyboardInterrupt:
            print(f"\n{C['yellow']}Exiting...{C['reset']}")
            break
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
