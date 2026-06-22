#!/usr/bin/env python3
"""
Mix-Crypto.com Auto Claim Bot - PSYCHO Edition
Complete rewrite with PsychoUI framework & Seledroid hCaptcha support
v5.0 - Anti-bot Xevil API, Daily 5 claims limit, Session-less
"""

import os
import sys
import time
import json
import re
import random
import warnings
import requests
from html import unescape
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')
os.environ["PYTHONWARNINGS"] = "ignore"

# ============================================================
# SELEDROID HCAPTCHA SOLVER (Optional - Android only)
# ============================================================
SELEDROID_AVAILABLE = False
try:
    from seledroid import webdriver as seledroid_webdriver
    from seledroid.webdriver.common.by import By
    SELEDROID_AVAILABLE = True
except ImportError:
    pass

def solve_hcaptcha_seledroid(pageurl, max_wait=90):
    """
    Seledroid FULLSCREEN mode - Opens browser for manual hCaptcha solving.
    Extracts ONLY the h-captcha-response token from JavaScript.
    Includes ad-click recovery - if user accidentally clicks ad, 
    navigates back to original page and retries.
    """
    if not SELEDROID_AVAILABLE:
        return None
    
    try:
        driver = seledroid_webdriver.Chrome(gui=True, pip_mode=False)
        
        try:
            driver.maximize_window()
        except Exception:
            pass
        
        driver.get(pageurl)
        bot.info(f"Seledroid [HCAPTCHA]: {pageurl}")
        bot.info("Solve hCaptcha in FULLSCREEN browser...")
        bot.info("⚠ Avoid clicking advertisements!")
        
        hcaptcha_token = None
        elapsed = 0
        interval = 2
        retry_count = 0
        max_retries = 3
        
        while elapsed < max_wait and retry_count < max_retries:
            try:
                current_url = driver.current_url
                
                # Check if navigated away (ad click)
                if pageurl not in current_url and 'mix-crypto.com' not in current_url:
                    bot.warning("Detected ad redirect! Returning to captcha page...")
                    driver.get(pageurl)
                    time.sleep(3)
                    retry_count += 1
                    continue
                
                token_element = driver.find_element(By.NAME, "h-captcha-response")
                token_value = token_element.get_attribute("value")
                
                if not token_value:
                    token_element = driver.find_element(By.NAME, "g-recaptcha-response")
                    token_value = token_element.get_attribute("value")
                
                if token_value and len(token_value) > 10:
                    hcaptcha_token = token_value
                    bot.info("Seledroid: hCaptcha token extracted!")
                    break
            except Exception:
                pass
            
            time.sleep(interval)
            elapsed += interval
        
        driver.close()
        return hcaptcha_token
    
    except Exception as e:
        bot.warning(f"Seledroid error: {str(e)}")
        return None


# ============================================================
# PSYCHO UI - Premium UI Framework
# ============================================================
class PsychoUI:
    def __init__(self, typing_speed=0.002):
        self.speed = typing_speed
        self.success_history = []
        self.max_history = 999999
        self.show_success = True
        
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
        self.version = "5.0.0"

    def type_text(self, text, color="", delay=0.001):
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    def show_banner(self, faucet_name="Mix-Crypto"):
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
            if self.success_history:
                print(f" {self.gray}────────────────────────────────────────────────────────────{self.reset}")
            print()

    def info(self, message):
        self.type_text(f"  {self.gray}• {self.reset}{message}", self.gray, 0.001)

    def warning(self, message):
        self.type_text(f"  {self.yellow}! {self.reset}{message}", self.yellow, 0.002)

    def error(self, message):
        self.type_text(f"  {self.red}× {self.reset}{message}", self.red, 0.002)

    def success(self, message, faucet_name="Mix-Crypto"):
        # Clean message - remove &times; and extra HTML
        clean_msg = message.replace('&times;', '').replace('×', '').strip()
        # Remove extra whitespace
        clean_msg = ' '.join(clean_msg.split())
        self.success_history.append(clean_msg)
        self.show_success = True
        self.show_banner(faucet_name)
    
    def show_menu_banner(self, faucet_name="Mix-Crypto"):
        self.show_success = False
        self.show_banner(faucet_name)
    
    def show_work_banner(self, faucet_name="Mix-Crypto"):
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
# SILENT - Referral embedded, not visible to user
BASE_URL_REF = "https://mix-crypto.com/?r=arasarathinam3@gmail.com"
BASE_URL = "https://mix-crypto.com"
SITE_KEY = "a10f8c8d-e42a-4a71-b874-e6fa959b4cac"

CONFIG_FILE = "mixcrypto_config.json"
CLAIMS_FILE = "mixcrypto_claims.json"  # Track daily claims per account

# ============================================================
# DAILY CLAIM TRACKER (Per Account)
# ============================================================
def load_claims_data():
    """Load claims tracking data"""
    if os.path.exists(CLAIMS_FILE):
        try:
            with open(CLAIMS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_claims_data(data):
    """Save claims tracking data"""
    try:
        with open(CLAIMS_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

def get_today_key():
    """Get today's date as key (resets at 00:00 UTC)"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def check_daily_limit(email):
    """
    Check if account has reached daily limit (5 claims per day).
    Reset happens at 00:00 UTC.
    Returns: (bool, int) - (can_claim, remaining)
    """
    claims_data = load_claims_data()
    today = get_today_key()
    
    # Clean old dates
    cleaned = {}
    for acc, dates in claims_data.items():
        if isinstance(dates, dict) and today in dates:
            cleaned[acc] = {today: dates[today]}
    
    if email not in cleaned:
        return True, 5
    
    today_claims = cleaned[email].get(today, 0)
    remaining = 5 - today_claims
    return remaining > 0, remaining

def record_claim(email):
    """Record a successful claim for an account"""
    claims_data = load_claims_data()
    today = get_today_key()
    
    if email not in claims_data:
        claims_data[email] = {}
    
    if today not in claims_data[email]:
        claims_data[email] = {today: 1}
    else:
        claims_data[email][today] += 1
    
    save_claims_data(claims_data)

def get_daily_claims(email):
    """Get number of claims today for an account"""
    claims_data = load_claims_data()
    today = get_today_key()
    return claims_data.get(email, {}).get(today, 0)

# ============================================================
# CONFIG MANAGEMENT
# ============================================================
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "email": "",
        "xevil_api_key": "",
        "user_agent": "Mozilla/5.0 (Linux; Android 10; M2006C3LG Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.217 Mobile Safari/537.36",
        "use_seledroid": False
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
# COLORFUL MENU FUNCTIONS
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

# ============================================================
# ANTIBOT SOLVER (XEVIL API)
# ============================================================
def solve_antibot(page_html, xevil_api_key, antibot_api_url, antibot_res_url):
    """
    Solve 4 anti-bot images using XEVIL API.
    Maps API result like "2,1,3,4" to rel numbers like " 7211 6700 7608 7709"
    """
    soup = BeautifulSoup(page_html, 'html.parser')
    
    main_base64 = None
    
    # Method 1: Text context
    for text in soup.find_all(string=re.compile(r'click on the AntiBot links')):
        parent = text.parent
        img = parent.find('img')
        if not img:
            img = parent.find_previous('img')
        if img and 'base64' in img.get('src', ''):
            src = img['src']
            main_base64 = src.split(',')[1] if ',' in src else src
            break
    
    # Method 2: Class
    if not main_base64:
        for img in soup.find_all('img'):
            src = img.get('src', '')
            classes = img.get('class', [])
            if 'base64' in src and 'img-fluid' in classes:
                main_base64 = src.split(',')[1] if ',' in src else src
                break
    
    # Method 3: Largest
    if not main_base64:
        largest = None
        largest_size = 0
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if 'base64' in src:
                b64 = src.split(',')[1] if ',' in src else src
                if len(b64) > largest_size:
                    largest_size = len(b64)
                    largest = b64
        if largest:
            main_base64 = largest
    
    if not main_base64:
        bot.warning("Anti-bot main image not found")
        return None
    
    # Find ablinks script
    script_tag = None
    for script in soup.find_all('script'):
        if script.string and 'ablinks' in script.string:
            script_tag = script
            break
    
    if not script_tag:
        bot.warning("ablinks script not found")
        return None
    
    script_content = script_tag.string
    
    # Extract 4 options
    matches = re.findall(
        r'rel=\\"(\d+)\\".*?src=\\"data:image/png;base64,([^\\"]+)\\"',
        script_content
    )
    
    if not matches:
        matches = re.findall(
            r'rel="(\d+)".*?src="data:image/png;base64,([^"]+)"',
            script_content
        )
    
    if not matches:
        all_rels = re.findall(r'rel=["\'](\d+)["\']', script_content)
        all_b64 = re.findall(r'data:image/png;base64,([^"\']+)', script_content)
        if all_rels and all_b64 and len(all_rels) == len(all_b64):
            matches = list(zip(all_rels, all_b64))
    
    if not matches or len(matches) != 4:
        bot.warning(f"Expected 4 anti-bot options, found {len(matches) if matches else 0}")
        return None
    
    # Build API payload
    data = {
        'key': xevil_api_key,
        'method': 'antibot',
        'main': main_base64
    }
    
    rel_mapping = {}
    for index, (rel, base64_str) in enumerate(matches, start=1):
        base64_str = unescape(base64_str)
        base64_str = base64_str.replace('\\', '')
        data[str(index)] = base64_str
        rel_mapping[str(index)] = rel
    
    # Send to XEVIL API
    try:
        bot.inline_status("Solving Anti-Bot via XEVIL...")
        
        r = requests.post(
            antibot_api_url,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        resp = r.text.strip()
        
        order_string = None
        
        if '|' in resp:
            parts = resp.split('|', 1)
            first_part = parts[0].strip()
            
            if first_part == 'OK' or first_part.isdigit():
                task_id = parts[1].strip() if first_part == 'OK' else first_part
                
                for _ in range(30):
                    time.sleep(5)
                    r2 = requests.get(antibot_res_url, params={
                        'key': xevil_api_key,
                        'id': task_id,
                        'action': 'get'
                    }, timeout=10)
                    
                    result = r2.text.strip()
                    
                    if result and 'NOT_READY' not in result and 'PROCESSING' not in result:
                        if '|' in result:
                            result = result.split('|')[1].strip()
                        order_string = result
                        break
            else:
                order_string = parts[1].strip() if len(parts) > 1 else resp
        
        if not order_string:
            order_string = resp.replace('OK', '').replace('|', '').strip()
        
        bot.clear_inline()
        
        if order_string and ',' in order_string:
            indices = [x.strip() for x in order_string.split(',')]
            
            final_order = []
            for idx in indices:
                if idx in rel_mapping:
                    final_order.append(rel_mapping[idx])
            
            if len(final_order) == 4:
                solution = " " + " ".join(final_order)
                bot.info(f"Anti-Bot solved successfully")
                return solution
    
    except Exception as e:
        bot.warning(f"XEVIL API error: {str(e)}")
    
    bot.clear_inline()
    return None

# ============================================================
# ADLINK BYPASS
# ============================================================
def bypass_adlink(url):
    if "link.adlink.click" not in url:
        return None
    
    mapped = url.replace("link.adlink.click", "blog.adlink.click")
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.diudemy.com/"
    })
    
    try:
        r = session.get(mapped, timeout=15)
        page_html = r.text
        
        if 'name="ad_form_data"' not in page_html:
            return None
        
        soup = BeautifulSoup(page_html, 'html.parser')
        
        def get_val(name):
            el = soup.find("input", {"name": name})
            return el["value"] if el else ""
        
        post_data = {
            "_method": "POST",
            "_csrfToken": get_val("_csrfToken"),
            "ad_form_data": get_val("ad_form_data"),
            "_Token[fields]": get_val("_Token[fields]"),
            "_Token[unlocked]": get_val("_Token[unlocked]")
        }
        
        time.sleep(5)
        
        r2 = session.post(
            "https://blog.adlink.click/links/go",
            data=post_data,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": mapped,
                "Accept": "application/json,text/javascript,*/*;q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=15
        )
        
        data = r2.json()
        
        if "url" in data and "limit.php" not in data["url"]:
            return data["url"]
        
    except:
        pass
    
    return None

# ============================================================
# UNIFIED HCAPTCHA SOLVER
# ============================================================
def solve_hcaptcha(pageurl, use_seledroid=False):
    """
    Unified hCaptcha solver:
    - Seledroid (manual browser) if enabled
    - BypassAllShortLinks API as fallback
    Returns ONLY the token
    """
    
    if use_seledroid and SELEDROID_AVAILABLE:
        bot.info("Using Seledroid for hCaptcha...")
        token = solve_hcaptcha_seledroid(pageurl)
        if token:
            return token
        else:
            bot.warning("Seledroid failed, falling back to API...")
    
    bot.inline_status("Solving hCaptcha via API...")
    
    try:
        api_key = "jUPQAhwftyQV4CxUaUmDzwVHqBn4fqTs"
        
        r = requests.get("https://bypassallshortlinks.space/in.php", params={
            "key": api_key, "method": "hcaptcha",
            "sitekey": SITE_KEY, "pageurl": pageurl
        }, timeout=30)
        
        if "OK|" not in r.text:
            bot.clear_inline()
            bot.warning("hCaptcha API submission failed")
            return None
        
        task_id = r.text.split("|")[1]
        
        for _ in range(40):
            time.sleep(5)
            r = requests.get("https://bypassallshortlinks.space/res.php", params={
                "key": api_key, "action": "get", "id": task_id
            }, timeout=30)
            
            if "CAPCHA_NOT_READY" in r.text:
                continue
            if r.text.startswith("OK|"):
                token = r.text.split("|")[1]
                bot.clear_inline()
                bot.info("hCaptcha solved via API")
                return token
            break
    except Exception as e:
        bot.warning(f"hCaptcha API error: {str(e)}")
    
    bot.clear_inline()
    return None

# ============================================================
# MAIN BOT
# ============================================================
class MixCryptoBot:
    def __init__(self, config):
        self.config = config
        self.email = config.get("email", "")
        self.xevil_api_key = config.get("xevil_api_key", "")
        self.user_agent = config.get("user_agent", "Mozilla/5.0 (Linux; Android 10; M2006C3LG Build/QP1A.190711.020) AppleWebKit/537.36")
        self.use_seledroid = config.get("use_seledroid", False)
        
        # XEVIL API endpoints
        self.antibot_api_url = "https://157.180.15.203/in.php"
        self.antibot_res_url = "https://157.180.15.203/res.php"
        
        # Fresh session each time (no cookie saving)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        self.total_claims = 0
        self.daily_claims = 0
    
    def _headers(self, extra=None):
        h = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
        if extra:
            h.update(extra)
        return h
    
    def claim(self):
        # Check daily limit FIRST
        can_claim, remaining = check_daily_limit(self.email)
        if not can_claim:
            bot.error(f"Daily limit reached (5/5)! Resets at 00:00 UTC")
            self.daily_claims = 5
            return "daily_limit"
        
        self.daily_claims = get_daily_claims(self.email)
        bot.info(f"Daily claims: {self.daily_claims}/5 | Remaining: {remaining}")
        
        # SILENT: Use referral URL internally
        bot.inline_status("Loading page...")
        
        try:
            r = self.session.get(BASE_URL_REF, headers=self._headers(), timeout=15)
            page_html = r.text
        except Exception as e:
            bot.clear_inline()
            bot.error(f"Failed to load page: {str(e)}")
            return "failed"
        
        bot.clear_inline()
        
        # Check cooldown
        if 'You have to wait' in page_html:
            match = re.search(r'(\d+)\s*minute', page_html)
            wait_time = int(match.group(1)) * 60 if match else 60
            bot.info(f"Cooldown: {wait_time}s")
            bot.countdown(wait_time + 3, "Cooldown Timer")
            return "retry"
        
        # Get session token
        soup = BeautifulSoup(page_html, 'html.parser')
        token_input = soup.find('input', {'name': 'session-token'})
        if not token_input:
            bot.error("Session token not found")
            return "failed"
        
        session_token = token_input.get('value')
        bot.info("Session token obtained")
        
        # Solve anti-bot using XEVIL API
        antibot_solution = solve_antibot(
            page_html, self.xevil_api_key,
            self.antibot_api_url, self.antibot_res_url
        )
        if not antibot_solution:
            bot.error("Anti-bot solving failed")
            return "failed"
        
        # Solve hCaptcha
        bot.info("Solving hCaptcha...")
        captcha_token = solve_hcaptcha(BASE_URL, self.use_seledroid)
        if not captcha_token:
            bot.error("hCaptcha solving failed")
            return "failed"
        
        # Submit claim
        bot.inline_status("Submitting claim...")
        
        payload = {
            'session-token': session_token,
            'address': self.email,
            'antibotlinks': antibot_solution,
            'captcha': 'hcaptcha',
            'g-recaptcha-response': captcha_token,
            'h-captcha-response': captcha_token,
            'login': 'Verify Captcha'
        }
        
        try:
            r = self.session.post(
                BASE_URL, data=payload,
                headers=self._headers({
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': BASE_URL,
                    'Referer': BASE_URL_REF,
                    'x-requested-with': 'mark.via.gp'
                }),
                timeout=30
            )
            page_html = r.text
        except Exception as e:
            bot.clear_inline()
            bot.error(f"Submit failed: {str(e)}")
            return "failed"
        
        bot.clear_inline()
        
        # Check for direct success
        if 'was sent to your' in page_html:
            match = re.search(r'<div class="alert alert-success[^"]*"[^>]*>(.*?)</div>', page_html, re.DOTALL)
            if match:
                msg = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                msg = msg.replace('&times;', '').replace('×', '').strip()
                msg = ' '.join(msg.split())  # Clean whitespace
                self.total_claims += 1
                record_claim(self.email)
                bot.success(msg, "Mix-Crypto")
                return "success"
        
        # Check for redirect/hash
        match = re.search(r'\?hash=([^"\']+)', page_html)
        if match:
            hash_val = match.group(1)
            bot.info(f"Following hash verification...")
            
            bot.inline_status("Following redirect...")
            r = self.session.get(
                BASE_URL,
                params={'hash': hash_val},
                headers=self._headers({'Referer': BASE_URL_REF}),
                timeout=30,
                allow_redirects=False
            )
            
            location = r.headers.get('Location', '')
            bot.clear_inline()
            
            if location:
                bot.info("Redirect detected, bypassing AdLink...")
                
                bypassed = bypass_adlink(location)
                if bypassed:
                    bot.info("AdLink bypassed")
                    
                    token_match = re.search(r'token=([^&]+)', bypassed)
                    if token_match:
                        token = token_match.group(1)
                        bot.info(f"Verification token obtained")
                        
                        # Wait 2 MINUTES after AdLink bypass
                        bot.info("Waiting 2 minutes after AdLink bypass...")
                        bot.countdown(120, "AdLink Cooldown")
                        
                        bot.inline_status("Verifying claim...")
                        r = self.session.get(
                            BASE_URL,
                            params={'token': token},
                            headers=self._headers({'Referer': BASE_URL_REF}),
                            timeout=30
                        )
                        bot.clear_inline()
                        
                        if 'was sent to your' in r.text:
                            match = re.search(r'<div class="alert alert-success[^"]*"[^>]*>(.*?)</div>', r.text, re.DOTALL)
                            if match:
                                msg = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                                msg = msg.replace('&times;', '').replace('×', '').strip()
                                msg = ' '.join(msg.split())
                                self.total_claims += 1
                                record_claim(self.email)
                                bot.success(msg, "Mix-Crypto")
                                return "success"
                        
                        if 'You have to wait' in r.text:
                            match = re.search(r'(\d+)\s*minute', r.text)
                            wait_time = int(match.group(1)) * 60 if match else 60
                            bot.info(f"Cooldown: {wait_time}s")
                            return "cooldown"
        
        bot.warning("Claim verification failed")
        return "failed"
    
    def run(self):
        bot.show_work_banner("Mix-Crypto")
        
        if not self.email:
            bot.error("Email is required! Go to: Set Account")
            input("\nPress Enter to continue...")
            return
        
        if not self.xevil_api_key:
            bot.error("XEVIL API Key is required! Go to: Set XEVIL API Key")
            input("\nPress Enter to continue...")
            return
        
        bot.info(f"Account: {self.email}")
        bot.info(f"hCaptcha: {'Seledroid' if self.use_seledroid and SELEDROID_AVAILABLE else 'API'}")
        daily_count = get_daily_claims(self.email)
        bot.info(f"Today's claims: {daily_count}/5")
        bot.info(f"Reset at: 00:00 UTC")
        print()
        
        while True:
            result = self.claim()
            
            if result == "daily_limit":
                # Calculate time until 00:00 UTC
                now = datetime.now(timezone.utc)
                tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                wait_seconds = int((tomorrow - now).total_seconds())
                bot.info(f"Waiting for reset at 00:00 UTC ({wait_seconds}s)")
                bot.countdown(wait_seconds, "Daily Reset Timer")
                continue
            
            if result == "success":
                daily_count = get_daily_claims(self.email)
                bot.info(f"Daily: {daily_count}/5 | Total: {self.total_claims}")
                print()
            
            elif result == "retry":
                continue
            
            elif result == "cooldown":
                continue
            else:
                bot.warning("Retrying in 30s...")
                bot.countdown(30, "Retry Timer")

# ============================================================
# MENU FUNCTIONS
# ============================================================
def show_set_account_menu(config):
    """Menu for setting account email"""
    clear_screen()
    bot.show_menu_banner("Mix-Crypto")
    print_header("Set Account")
    print_instruction("Enter your FaucetPay or wallet email address")
    print()
    
    current_email = config.get('email', '')
    if current_email:
        print_info(f"Current: {current_email}")
        daily = get_daily_claims(current_email)
        print_info(f"Today's claims: {daily}/5")
    else:
        print_warning("No email set!")
    print()
    
    email = get_input_with_default("Email Address", current_email)
    config['email'] = email
    save_config(config)
    print_success("Account updated successfully!")
    input("\nPress Enter to continue...")

def show_set_xevil_menu(config):
    """Menu for setting XEVIL API Key"""
    clear_screen()
    bot.show_menu_banner("Mix-Crypto")
    print_header("Set XEVIL API Key")
    print_instruction("Enter your XEVIL API Key for Anti-Bot solving")
    print()
    
    current_key = config.get('xevil_api_key', '')
    if current_key:
        masked = current_key[:6] + "****" + current_key[-4:] if len(current_key) > 10 else "****"
        print_info(f"Current: {masked}")
    else:
        print_warning("No API key set!")
    print()
    
    api_key = get_input_with_default("XEVIL API Key", current_key)
    config['xevil_api_key'] = api_key
    save_config(config)
    print_success("XEVIL API Key updated!")
    input("\nPress Enter to continue...")

def show_set_solver_menu(config):
    """Menu for selecting hCaptcha solver"""
    while True:
        clear_screen()
        bot.show_menu_banner("Mix-Crypto")
        print_header("Set hCaptcha Solver")
        print_instruction("Select hCaptcha solving method")
        print()
        
        current_mode = config.get('use_seledroid', False)
        if current_mode and SELEDROID_AVAILABLE:
            print_info(f"Current: {C['green']}Seledroid [MANUAL]{C['reset']}")
        elif current_mode and not SELEDROID_AVAILABLE:
            print_info(f"Current: {C['yellow']}Seledroid (unavailable){C['reset']}")
        else:
            print_info(f"Current: {C['green']}BypassAllShortLinks API{C['reset']}")
        print()
        print(f" {C['gray']}{'─'*55}{C['reset']}")
        
        print(f"  {C['menu']}[1]{C['reset']} BypassAllShortLinks API (Auto)")
        
        if SELEDROID_AVAILABLE:
            print(f"  {C['menu']}[2]{C['reset']} Seledroid [MANUAL - Fullscreen Browser]")
        else:
            print(f"  {C['red']}[2] Seledroid [UNAVAILABLE]{C['reset']}")
        
        print(f"  {C['gold']}[B] Back to Main Menu{C['reset']}")
        print(f" {C['gray']}{'─'*55}{C['reset']}")
        
        choice = input(f"\n{C['menu']}Select solver: {C['reset']}").strip().lower()
        
        if choice == '1':
            config['use_seledroid'] = False
            save_config(config)
            print_success("Solver set to: BypassAllShortLinks API")
            input("\nPress Enter to continue...")
            return
        
        elif choice == '2' and SELEDROID_AVAILABLE:
            config['use_seledroid'] = True
            save_config(config)
            print_success("Solver set to: Seledroid [MANUAL]")
            print_instruction("Browser will open for manual hCaptcha solving")
            input("\nPress Enter to continue...")
            return
        
        elif choice == 'b':
            return
        
        else:
            print_error("Invalid option!")
            time.sleep(1)

def show_main_menu():
    clear_screen()
    bot.show_menu_banner("Mix-Crypto")
    print_header("Mix-Crypto Bot - Main Menu")
    
    if SELEDROID_AVAILABLE:
        print(f"  {C['green']}◆ Seledroid: AVAILABLE{C['reset']}")
    else:
        print(f"  {C['red']}◆ Seledroid: NOT AVAILABLE{C['reset']}")
    print()
    
    menu_options = {
        '1': 'Set Account [Email]',
        '2': 'Set XEVIL API Key [ANTI-BOT-BYPASS]',
        '3': 'Set hCaptcha Solver',
        '4': 'Set User Agent',
        '5': 'Start work',
        '6': 'Exit'
    }
    return get_menu_choice("Main Menu:", menu_options)

def main():
    config = load_config()
    
    while True:
        choice = show_main_menu()
        
        if choice == '1':
            show_set_account_menu(config)
            
        elif choice == '2':
            show_set_xevil_menu(config)
            
        elif choice == '3':
            show_set_solver_menu(config)
            
        elif choice == '4':
            clear_screen()
            bot.show_menu_banner("Mix-Crypto")
            print_header("Set User Agent")
            current = config.get('user_agent', 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36')
            new_ua = get_input_with_default("Enter User Agent", current)
            config['user_agent'] = new_ua
            save_config(config)
            print_success("User Agent updated")
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            clear_screen()
            bot.show_menu_banner("Mix-Crypto")
            
            if not config.get('email'):
                print_error("Email is required! Go to: Set Account")
                input("\nPress Enter to continue...")
                continue
            
            if not config.get('xevil_api_key'):
                print_error("XEVIL API Key is required! Go to: Set XEVIL API Key")
                input("\nPress Enter to continue...")
                continue
            
            if config.get('use_seledroid') and not SELEDROID_AVAILABLE:
                print_error("Seledroid not available!")
                input("\nPress Enter to continue...")
                continue
            
            bot_obj = MixCryptoBot(config)
            
            try:
                bot_obj.run()
            except KeyboardInterrupt:
                bot.clear_inline()
                print(f'\n{C["yellow"]}[STOPPED] Bot safely terminated.{C["reset"]}')
                time.sleep(1.5)
            except Exception as e:
                bot.error(f"Bot error: {str(e)}")
                input("\nPress Enter to continue...")
            
        elif choice == '6':
            print(f"\n{C['yellow']}Exiting...{C['reset']}")
            break

if __name__ == "__main__":
    main()
