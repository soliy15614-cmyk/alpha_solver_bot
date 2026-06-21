#!/usr/bin/env python3
"""
Altcryp Bot - Complete Automation Script
With Seledroid Captcha Solver Support
+ Dynamic Fingerprint Generation (Device-Aware)
"""

import os
import sys
import time
import json
import re
import random
import warnings
import platform
import socket
import hashlib
import requests
from bs4 import BeautifulSoup

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')
os.environ["PYTHONWARNINGS"] = "ignore"

# ============================================================
# SELEDROID CAPTCHA SOLVER (Optional - Android only)
# ============================================================
SELEDROID_AVAILABLE = False
try:
    from seledroid import webdriver as seledroid_webdriver
    from seledroid.webdriver.common.by import By
    SELEDROID_AVAILABLE = True
except ImportError:
    pass

def solve_turnstile_seledroid_fullscreen(pageurl, max_wait=90):
    """
    Seledroid FULLSCREEN mode - Opens browser in full screen
    User manually solves captcha, token is extracted from JavaScript
    Returns ONLY the token (no user_agent needed)
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
        bot.info(f"Seledroid [FULLSCREEN]: {pageurl}")
        bot.info("Solve the captcha in the FULLSCREEN browser...")
        
        turnstile_token = None
        elapsed = 0
        interval = 2
        
        while elapsed < max_wait:
            try:
                token_element = driver.find_element(By.NAME, "cf-turnstile-response")
                token_value = token_element.get_attribute("value")
                
                if not token_value:
                    token_element = driver.find_element(By.NAME, "g-recaptcha-response")
                    token_value = token_element.get_attribute("value")
                
                if token_value and len(token_value) > 10:
                    turnstile_token = token_value
                    bot.info("Seledroid: Token extracted from JavaScript!")
                    break
            except Exception:
                pass
            
            time.sleep(interval)
            elapsed += interval
        
        driver.close()
        return turnstile_token
    
    except Exception as e:
        bot.warning(f"Seledroid error: {str(e)}")
        return None


def solve_turnstile_seledroid_interstitial(pageurl, max_wait=90):
    """
    Seledroid INTERSTITIAL mode - Opens browser as side panel (pip_mode=True)
    User manually solves captcha, token is extracted from JavaScript
    Returns ONLY the token
    """
    if not SELEDROID_AVAILABLE:
        return None
    
    try:
        driver = seledroid_webdriver.Chrome(gui=True, pip_mode=True)
        driver.get(pageurl)
        bot.info(f"Seledroid [INTERSTITIAL]: {pageurl}")
        bot.info("Solve the captcha in the side panel browser...")
        
        turnstile_token = None
        elapsed = 0
        interval = 2
        
        while elapsed < max_wait:
            try:
                token_element = driver.find_element(By.NAME, "cf-turnstile-response")
                token_value = token_element.get_attribute("value")
                
                if not token_value:
                    token_element = driver.find_element(By.NAME, "g-recaptcha-response")
                    token_value = token_element.get_attribute("value")
                
                if token_value and len(token_value) > 10:
                    turnstile_token = token_value
                    bot.info("Seledroid: Token extracted from JavaScript!")
                    break
            except Exception:
                pass
            
            time.sleep(interval)
            elapsed += interval
        
        driver.close()
        return turnstile_token
    
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
        self.version = "3.0.0"

    def type_text(self, text, color="", delay=0.001):
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    def show_banner(self, faucet_name="Altcryp"):
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

    def success(self, message, faucet_name="Altcryp"):
        self.success_history.append(message)
        self.show_success = True
        self.show_banner(faucet_name)
    
    def show_menu_banner(self, faucet_name="Altcryp"):
        self.show_success = False
        self.show_banner(faucet_name)
    
    def show_work_banner(self, faucet_name="Altcryp"):
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
DOMAIN = "https://altcryp.com"
LOGIN_URL = f"{DOMAIN}"
LOGIN_ACTION = f"{DOMAIN}/auth/login"
FAUCET_BASE = f"{DOMAIN}/faucet/currency"
FAUCET_VERIFY = f"{DOMAIN}/faucet/verify"
FIREWALL_URL = f"{DOMAIN}/firewall"
FIREWALL_VERIFY = f"{DOMAIN}/firewall/verify"

TURNSTILE_SITEKEY = "0x4AAAAAAAHPLPJjjJUpAitl"

SESSION_FILE = "altcryp_session.json"
CONFIG_FILE = "altcryp_config.json"

# ============================================================
# SOLVER MODES
# ============================================================
SOLVER_MODES = {
    "api": "BypassAllShortLinks API",
    "seledroid_fullscreen": "Seledroid [FULLSCREEN - Manual]",
    "seledroid_interstitial": "Seledroid [INTERSTITIAL - Side Panel]"
}

# ============================================================
# ALL COINS LIST
# ============================================================
ALL_COINS = [
    "bnb", "bch", "dash", "doge", "dgb", "pol", "sol", "trx", 
    "ltc", "xrp", "zec", "usdt", "ton", "pepe", "eth", "fey", "trump"
]

# ============================================================
# SESSION & CONFIG
# ============================================================
def save_session(cookies_dict, user_agent):
    data = {"cookies": cookies_dict, "user_agent": user_agent, "saved_at": time.time()}
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def load_session():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return None

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
        "wallet": "",
        "api_key": "",
        "solver_mode": "api",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "device_profile": "auto"  # auto, android, windows, custom
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
# DYNAMIC DEVICE DETECTION & FINGERPRINT GENERATOR
# ============================================================
def get_device_info():
    """
    Dynamically detect device information from the running system.
    Returns a dict with all detected device parameters.
    """
    info = {}
    
    # Detect OS
    system = platform.system().lower()
    if system == 'linux':
        # Check if Android (Termux) by looking for specific paths
        if os.path.exists('/data/data/com.termux') or 'ANDROID_ROOT' in os.environ:
            info['os_name'] = 'Android'
            info['platform'] = 'android'
        else:
            info['os_name'] = 'Linux'
            info['platform'] = 'linux'
    elif system == 'windows':
        info['os_name'] = 'Windows'
        info['platform'] = 'windows'
    elif system == 'darwin':
        info['os_name'] = 'MacOS'
        info['platform'] = 'macos'
    else:
        info['os_name'] = 'Unknown'
        info['platform'] = 'unknown'
    
    # Detect browser info from user agent
    ua = os.environ.get('HTTP_USER_AGENT', '')
    
    # Get hostname as device identifier
    try:
        info['hostname'] = socket.gethostname()
    except:
        info['hostname'] = 'unknown'
    
    # Get local IP (for hashing only, not sent)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        info['local_ip'] = s.getsockname()[0]
        s.close()
    except:
        info['local_ip'] = '127.0.0.1'
    
    # CPU count
    info['cpu_cores'] = str(os.cpu_count() or 4)
    
    # Timezone
    try:
        import time as t
        info['timezone_offset'] = -t.timezone // 3600
        info['timezone_str'] = f"UTC{'+' if info['timezone_offset'] >= 0 else ''}{info['timezone_offset']}"
    except:
        info['timezone_offset'] = 5.5
        info['timezone_str'] = 'UTC+5:30'
    
    # Detect if running in Termux (Android)
    info['is_termux'] = os.path.exists('/data/data/com.termux') or 'TERMUX_VERSION' in os.environ
    
    # Screen resolution (defaults based on platform)
    if info['is_termux'] or info['platform'] == 'android':
        info['screen_width'] = random.choice([360, 412, 414, 375])
        info['screen_height'] = random.choice([800, 915, 896, 812])
    elif info['platform'] == 'windows':
        info['screen_width'] = random.choice([1366, 1920, 1536])
        info['screen_height'] = random.choice([768, 1080, 864])
    else:
        info['screen_width'] = random.choice([1366, 1920, 1440])
        info['screen_height'] = random.choice([768, 1080, 900])
    
    # Generate consistent device hash based on hostname + IP
    device_seed = f"{info.get('hostname', '')}-{info.get('local_ip', '')}-{info.get('platform', '')}"
    info['device_hash'] = hashlib.md5(device_seed.encode()).hexdigest()[:12]
    
    # Browser language
    info['browser_lang'] = random.choice(['en-US', 'en-GB', 'en-IN', 'en'])
    
    # Color depth
    info['color_depth'] = str(random.choice([24, 32]))
    
    # Platform-specific timezone
    if info['is_termux']:
        info['timezone_name'] = 'Asia/Colombo'
    elif info['platform'] == 'windows':
        info['timezone_name'] = random.choice(['Asia/Kolkata', 'Asia/Colombo', 'Asia/Dhaka'])
    else:
        info['timezone_name'] = random.choice(['Asia/Kolkata', 'Asia/Colombo', 'Asia/Dhaka', 'Europe/London'])
    
    return info


def generate_fingerprint_data(device_info=None, user_agent=None):
    """
    Generate realistic fingerprint data based on actual device info.
    This makes each request look unique to the actual device being used.
    """
    if device_info is None:
        device_info = get_device_info()
    
    # Determine OS name for fingerprint
    if device_info['platform'] == 'android' or device_info['is_termux']:
        fp_os_name = 'Android'
        fp_browser_name = 'Chrome'
    elif device_info['platform'] == 'windows':
        fp_os_name = 'Windows'
        fp_browser_name = 'Chrome'
    elif device_info['platform'] == 'linux':
        fp_os_name = 'Linux'
        fp_browser_name = 'Chrome'
    elif device_info['platform'] == 'macos':
        fp_os_name = 'MacOS'
        fp_browser_name = 'Safari'
    else:
        fp_os_name = 'Android'
        fp_browser_name = 'Chrome'
    
    # Screen resolution
    screen_res = f"{device_info['screen_width']}x{device_info['screen_height']}"
    
    # CPU cores
    cpu_cores = device_info['cpu_cores']
    
    # Timezone
    timezone = device_info['timezone_name']
    
    # Browser language
    browser_lang = device_info['browser_lang']
    
    # Color depth
    color_depth = device_info['color_depth']
    
    # Generate device token using consistent hash
    # This ensures same device always gets same token
    canvas_data = f"FaucetSpy_Track_2026_Secure_v2_{device_info['device_hash']}"
    components = [
        canvas_data,
        screen_res,
        color_depth,
        cpu_cores,
        timezone,
        browser_lang,
        "5"  # random seed
    ]
    str_data = '||'.join(components)
    hash_val = 0
    for char in str_data:
        hash_val = ((hash_val << 5) - hash_val) + ord(char)
        hash_val = hash_val & hash_val
    fp_token = "HW_" + str(abs(hash_val))[:16]
    
    return {
        'fp_device_token': fp_token,
        'fp_os_name': fp_os_name,
        'fp_browser_name': fp_browser_name,
        'fp_screen_res': screen_res,
        'fp_user_timezone': timezone,
        'fp_browser_lang': browser_lang,
        'fp_cpu_cores': cpu_cores,
        'fp_adblocker': random.choice(['Enabled', 'Disabled']),
        '_device_hash': device_info['device_hash'],  # internal use only
        '_platform': device_info['platform']  # internal use only
    }


# ============================================================
# UNIFIED CAPTCHA SOLVER
# ============================================================
def solve_turnstile(api_key, sitekey, pageurl, solver_mode="api", max_attempts=30):
    """
    Unified Turnstile solver with multiple backends:
    - api: BypassAllShortLinks API
    - seledroid_fullscreen: Seledroid fullscreen manual mode
    - seledroid_interstitial: Seledroid side panel manual mode
    Returns ONLY the token
    """
    
    # Seledroid FULLSCREEN mode
    if solver_mode == "seledroid_fullscreen":
        if not SELEDROID_AVAILABLE:
            bot.error("Seledroid not available!")
            return None
        
        bot.info("Using Seledroid [FULLSCREEN]...")
        token = solve_turnstile_seledroid_fullscreen(pageurl)
        if token:
            bot.info("Seledroid: Token extracted successfully!")
            return token
        else:
            bot.warning("Seledroid failed!")
            return None
    
    # Seledroid INTERSTITIAL mode
    if solver_mode == "seledroid_interstitial":
        if not SELEDROID_AVAILABLE:
            bot.error("Seledroid not available!")
            return None
        
        bot.info("Using Seledroid [INTERSTITIAL]...")
        token = solve_turnstile_seledroid_interstitial(pageurl)
        if token:
            bot.info("Seledroid: Token extracted successfully!")
            return token
        else:
            bot.warning("Seledroid failed!")
            return None
    
    # API mode (default)
    bot.inline_status("Solving Turnstile via API...")
    api_base = "https://bypassallshortlinks.space"
    
    try:
        submit_url = f"{api_base}/in.php"
        params = {
            'key': api_key,
            'method': 'turnstile',
            'pageurl': pageurl,
            'sitekey': sitekey
        }
        
        resp = requests.get(submit_url, params=params, timeout=30)
        result = resp.text.strip()
        bot.inline_status(f"API: {result}")
        
        if result.startswith('OK|'):
            task_id = result.split('|')[1]
            bot.info(f"Task ID: {task_id}")
            
            poll_url = f"{api_base}/res.php"
            for attempt in range(max_attempts):
                time.sleep(5)
                poll_resp = requests.get(poll_url, params={'key': api_key, 'id': task_id}, timeout=30)
                poll_result = poll_resp.text.strip()
                bot.inline_status(f"Polling: {poll_result}")
                
                if poll_result == 'CAPCHA_NOT_READY':
                    continue
                elif poll_result.startswith('OK|'):
                    token = poll_result.split('|')[1]
                    bot.clear_inline()
                    bot.info("Turnstile solved via API")
                    return token
                elif 'ERROR' in poll_result:
                    bot.warning(f"API Error: {poll_result}")
                    return None
                else:
                    continue
            
            bot.warning("API Timeout")
            return None
        else:
            bot.warning(f"API Error: {result}")
            return None
    except Exception as e:
        bot.warning(f"API Error: {str(e)}")
        return None

# ============================================================
# MAIN BOT
# ============================================================
class AltcrypBot:
    def __init__(self, config):
        self.config = config
        self.wallet = config.get("wallet", "")
        self.api_key = config.get("api_key", "")
        self.solver_mode = config.get("solver_mode", "api")
        self.user_agent = config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Detect device info ONCE at startup
        self.device_info = get_device_info()
        bot.info(f"Device: {self.device_info['platform']} | CPU: {self.device_info['cpu_cores']} cores")
        bot.info(f"Screen: {self.device_info['screen_width']}x{self.device_info['screen_height']}")
        bot.info(f"Device Hash: {self.device_info['device_hash']}")
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        saved = load_session()
        if saved and saved.get("user_agent"):
            self.user_agent = saved["user_agent"]
            for name, value in saved["cookies"].items():
                self.session.cookies.set(name, value, domain="altcryp.com")
        
        self.logged_in = False
        self.total_claimed = 0
        self.selected_coins = []
        
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
        soup = BeautifulSoup(html, 'html.parser')
        csrf = soup.find('input', {'name': 'csrf_token_name'})
        if csrf and csrf.get('value'):
            return csrf.get('value')
        csrf = soup.find('input', {'id': 'token'})
        if csrf and csrf.get('value'):
            return csrf.get('value')
        return None
    
    def _get_token(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        token = soup.find('input', {'name': 'token'})
        if token and token.get('value'):
            return token.get('value')
        return None
    
    def _get_swal_message(self, html):
        match = re.search(r"Swal\.fire\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)", html)
        if match:
            return {"title": match.group(1), "text": match.group(2), "icon": match.group(3)}
        return None
    
    def _has_captcha(self, html):
        return 'cf-turnstile' in html or 'turnstile' in html
    
    def _get_sitekey(self, html):
        match = re.search(r'data-sitekey="([^"]+)"', html)
        if match:
            return match.group(1)
        match = re.search(r"data-sitekey='([^']+)'", html)
        if match:
            return match.group(1)
        return None
    
    def _generate_fp_data(self):
        """
        Generate fingerprint data based on ACTUAL device running this script.
        Each device will produce unique, consistent fingerprint.
        """
        return generate_fingerprint_data(self.device_info, self.user_agent)
    
    def handle_firewall(self, html):
        bot.info("Firewall detected! Solving Turnstile...")
        
        csrf = self._get_csrf(html)
        if not csrf:
            bot.error("CSRF token not found in firewall page")
            return False
        
        sitekey = self._get_sitekey(html)
        if not sitekey:
            bot.error("Sitekey not found in firewall page")
            return False
        
        bot.info(f"CSRF: {csrf}")
        bot.info(f"Sitekey: {sitekey}")
        bot.info(f"Solver: {SOLVER_MODES.get(self.solver_mode, 'API')}")
        
        turnstile = solve_turnstile(
            self.api_key, sitekey, FIREWALL_URL, 
            solver_mode=self.solver_mode
        )
        
        if not turnstile:
            bot.error("Failed to solve Turnstile")
            return False
        
        payload = {
            'csrf_token_name': csrf,
            'captchaType': 'turnstile',
            'cf-turnstile-response': turnstile
        }
        
        resp = self.session.post(
            FIREWALL_VERIFY,
            data=payload,
            headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}),
            timeout=30,
            allow_redirects=True
        )
        
        if resp.status_code == 200:
            bot.info("Firewall bypassed successfully!")
            return True
        else:
            bot.error(f"Firewall verify failed: {resp.status_code}")
            return False
    
    def is_logged_in(self):
        try:
            resp = self.session.get(LOGIN_URL, headers=self._headers(), timeout=10)
            if resp.status_code == 200:
                if '/firewall' in resp.url:
                    bot.info("Firewall page detected")
                    if self.handle_firewall(resp.text):
                        return self.is_logged_in()
                    return False
                
                csrf = self._get_csrf(resp.text)
                if not csrf:
                    self.logged_in = True
                    return True
                return False
            return False
        except:
            return False
    
    def login(self):
        bot.info("Logging in...")
        
        try:
            resp = self.session.get(LOGIN_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                bot.error(f"Failed to load page (status {resp.status_code})")
                return False
            
            if '/firewall' in resp.url:
                bot.info("Firewall page detected during login")
                if self.handle_firewall(resp.text):
                    return self.login()
                return False
            
            html = resp.text
            csrf = self._get_csrf(html)
            
            if not csrf:
                bot.info("Already logged in!")
                self.logged_in = True
                return True
            
            bot.info(f"CSRF Token: {csrf}")
            
            has_captcha = self._has_captcha(html)
            
            payload = {
                'wallet': self.wallet,
                'csrf_token_name': csrf,
            }
            
            if has_captcha:
                bot.info("Turnstile detected on login page")
                sitekey = self._get_sitekey(html) or TURNSTILE_SITEKEY
                
                turnstile = solve_turnstile(
                    self.api_key, sitekey, LOGIN_URL,
                    solver_mode=self.solver_mode
                )
                
                if turnstile:
                    payload['captcha'] = 'turnstile'
                    payload['cf-turnstile-response'] = turnstile
                    bot.info("Turnstile solved")
                else:
                    bot.error("Failed to solve Turnstile")
                    return False
            else:
                payload['captcha'] = ''
            
            time.sleep(random.uniform(1, 2))
            
            resp = self.session.post(
                LOGIN_ACTION,
                data=payload,
                headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}),
                timeout=30,
                allow_redirects=True
            )
            
            swal = self._get_swal_message(resp.text)
            if swal and swal['icon'] == 'success':
                cookies = self.session.cookies.get_dict()
                save_session(cookies, self.user_agent)
                self.logged_in = True
                bot.success(f"Login Success", "Altcryp")
                return True
            
            if '<title>Dashboard' in resp.text or '/dashboard' in resp.url:
                cookies = self.session.cookies.get_dict()
                save_session(cookies, self.user_agent)
                self.logged_in = True
                bot.success("Login Success", "Altcryp")
                return True
            
            if '/home' in resp.url or 'dashboard' in resp.url:
                cookies = self.session.cookies.get_dict()
                save_session(cookies, self.user_agent)
                self.logged_in = True
                bot.success("Login Success", "Altcryp")
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
    
    def is_session_valid(self):
        try:
            resp = self.session.get(f"{DOMAIN}/dashboard", headers=self._headers(), timeout=10, allow_redirects=False)
            if resp.status_code == 200:
                if '/firewall' in resp.url:
                    bot.info("Firewall detected during session check")
                    if self.handle_firewall(resp.text):
                        return self.is_session_valid()
                    return False
                if '<title>Dashboard' in resp.text or 'dashboard' in resp.url:
                    return True
                if '/login' in resp.headers.get('Location', ''):
                    return False
                return True
            return False
        except:
            return False
    
    def ensure_logged_in(self):
        if self.is_logged_in():
            return True
        return self.login()
    
    def claim_faucet(self, currency):
        try:
            faucet_url = f"{FAUCET_BASE}/{currency}"
            
            resp = self.session.get(faucet_url, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                bot.warning(f"Failed to load {currency} faucet page")
                return False
            
            if '/firewall' in resp.url:
                bot.info("Firewall detected during faucet claim")
                if self.handle_firewall(resp.text):
                    return self.claim_faucet(currency)
                return False
            
            html = resp.text
            
            timer_match = re.search(r'id="countdown">(\d+)</span>', html)
            if timer_match:
                wait = int(timer_match.group(1))
                if wait > 0:
                    bot.info(f"{currency.upper()} cooldown: {wait}s")
                    bot.countdown(wait + 2, f"{currency.upper()} Timer")
                    return self.claim_faucet(currency)
            
            csrf = self._get_csrf(html)
            if not csrf:
                bot.warning("CSRF token not found")
                return False
            
            token = self._get_token(html)
            if not token:
                bot.warning("Token not found")
                return False
            
            has_captcha = self._has_captcha(html)
            
            # Generate dynamic fingerprint based on ACTUAL device
            fp_data = self._generate_fp_data()
            
            # Show what fingerprint is being used (for debugging)
            bot.info(f"FP: {fp_data['fp_device_token']} | OS: {fp_data['fp_os_name']} | Screen: {fp_data['fp_screen_res']}")
            
            payload = {
                'username_fake_field': '',
                'fp_device_token': fp_data['fp_device_token'],
                'fp_os_name': fp_data['fp_os_name'],
                'fp_browser_name': fp_data['fp_browser_name'],
                'fp_screen_res': fp_data['fp_screen_res'],
                'fp_user_timezone': fp_data['fp_user_timezone'],
                'fp_browser_lang': fp_data['fp_browser_lang'],
                'fp_cpu_cores': fp_data['fp_cpu_cores'],
                'fp_adblocker': fp_data['fp_adblocker'],
                'csrf_token_name': csrf,
                'token': token,
            }
            
            if has_captcha:
                sitekey = self._get_sitekey(html) or TURNSTILE_SITEKEY
                
                turnstile = solve_turnstile(
                    self.api_key, sitekey, faucet_url,
                    solver_mode=self.solver_mode
                )
                
                if turnstile:
                    payload['captcha'] = 'turnstile'
                    payload['cf-turnstile-response'] = turnstile
                else:
                    bot.warning("Failed to solve Turnstile")
                    return False
            else:
                payload['captcha'] = ''
            
            time.sleep(random.uniform(1, 2))
            
            verify_url = f"{FAUCET_VERIFY}/{currency}"
            resp = self.session.post(
                verify_url,
                data=payload,
                headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}),
                timeout=30,
                allow_redirects=True
            )
            
            swal = self._get_swal_message(resp.text)
            if swal and swal['icon'] == 'success':
                self.total_claimed += 1
                bot.success(f"{currency.upper()} -> {swal['text']}", "Altcryp")
                return True
            
            if 'sent to your FaucetPay account' in resp.text:
                match = re.search(r'([\d.]+)\s+([A-Z]+)\s+has been sent', resp.text)
                if match:
                    self.total_claimed += 1
                    bot.success(f"{currency.upper()} -> {match.group(1)} {match.group(2)} sent!", "Altcryp")
                    return True
            
            error_match = re.search(r'<div class="alert alert-danger">([^<]+)</div>', resp.text)
            if error_match:
                bot.warning(f"{currency.upper()}: {error_match.group(1)}")
            else:
                bot.warning(f"{currency.upper()} claim failed")
            
            return False
            
        except Exception as e:
            bot.warning(f"Faucet error: {str(e)}")
            return False
    
    def select_coins_menu(self):
        while True:
            clear_screen()
            bot.show_menu_banner("Altcryp")
            
            print(f" {C['header']}{'═'*55}{C['reset']}")
            print(f" {C['header']}  Select Coins to Claim{C['reset']}")
            print(f" {C['header']}{'═'*55}{C['reset']}")
            print()
            
            if self.selected_coins:
                selected_str = ", ".join([c.upper() for c in self.selected_coins])
                print(f" {C['green']}Selected: {selected_str}{C['reset']}")
            else:
                print(f" {C['yellow']}No coins selected yet{C['reset']}")
            print()
            
            print(f" {C['gray']}{'─'*55}{C['reset']}")
            
            for idx, coin in enumerate(ALL_COINS, 1):
                if coin in self.selected_coins:
                    print(f"  {C['green']}[{idx}] ✓ {coin.upper()}{C['reset']}")
                else:
                    print(f"  {C['menu']}[{idx}]{C['reset']} {coin.upper()}")
            
            print(f" {C['gray']}{'─'*55}{C['reset']}")
            print(f"  {C['gold']}[A] Select All Coins{C['reset']}")
            print(f"  {C['gold']}[C] Clear All Selections{C['reset']}")
            print(f"  {C['gold']}[S] Start Claiming{C['reset']}")
            print(f"  {C['gold']}[B] Back to Main Menu{C['reset']}")
            print(f" {C['gray']}{'─'*55}{C['reset']}")
            
            choice = input(f"\n{C['menu']}Select option: {C['reset']}").strip().lower()
            
            if choice == 'a':
                self.selected_coins = ALL_COINS.copy()
                print(f" {C['green']}All coins selected!{C['reset']}")
                time.sleep(1)
            
            elif choice == 'c':
                self.selected_coins = []
                print(f" {C['yellow']}All selections cleared!{C['reset']}")
                time.sleep(1)
            
            elif choice == 's':
                if not self.selected_coins:
                    print(f" {C['red']}Please select at least one coin!{C['reset']}")
                    time.sleep(1)
                    continue
                return True
            
            elif choice == 'b':
                return False
            
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(ALL_COINS):
                    coin = ALL_COINS[idx]
                    if coin in self.selected_coins:
                        self.selected_coins.remove(coin)
                        print(f" {C['yellow']}Removed {coin.upper()}{C['reset']}")
                    else:
                        self.selected_coins.append(coin)
                        print(f" {C['green']}Added {coin.upper()}{C['reset']}")
                    time.sleep(0.5)
                else:
                    print(f" {C['red']}Invalid selection!{C['reset']}")
                    time.sleep(1)
            else:
                print(f" {C['red']}Invalid option!{C['reset']}")
                time.sleep(1)
    
    def run(self):
        bot.show_work_banner("Altcryp")
        
        # Show device info
        bot.info(f"Platform: {self.device_info['platform'].upper()}")
        bot.info(f"Device ID: {self.device_info['device_hash']}")
        
        if not self.wallet:
            bot.error("Wallet is required! Go to: Set Account")
            input("\nPress Enter to continue...")
            return
        
        if self.solver_mode == "api" and not self.api_key:
            bot.error("API Key required for API mode! Go to: Set Solver")
            input("\nPress Enter to continue...")
            return
        
        if self.solver_mode.startswith("seledroid") and not SELEDROID_AVAILABLE:
            bot.error("Seledroid not available! Install module first.")
            input("\nPress Enter to continue...")
            return
        
        if not self.select_coins_menu():
            return
        
        if not self.ensure_logged_in():
            bot.error("Login failed!")
            input("\nPress Enter to continue...")
            return
        
        cycle = 0
        
        while True:
            cycle += 1
            bot.show_work_banner("Altcryp")
            bot.info(f"--- Cycle {cycle} ---")
            bot.info(f"Solver: {SOLVER_MODES.get(self.solver_mode, 'API')}")
            
            if not self.is_session_valid():
                bot.info("Session expired. Re-logging in...")
                if not self.login():
                    bot.error("Re-login failed!")
                    input("\nPress Enter to continue...")
                    break
            
            for coin in self.selected_coins:
                bot.info(f"Claiming {coin.upper()}...")
                result = self.claim_faucet(coin)
                
                if not result:
                    bot.warning(f"{coin.upper()} claim failed")
                
                wait_time = random.randint(20, 25)
                bot.countdown(wait_time, "Cooldown")
            
            bot.info(f"Total claims: {self.total_claimed}")
            
            wait_time = random.randint(60, 120)
            bot.info(f"Next cycle in {wait_time}s")
            bot.countdown(wait_time, "Cycle Timer")

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

def show_device_info():
    """Show detected device information"""
    info = get_device_info()
    clear_screen()
    bot.show_menu_banner("Altcryp")
    print_header("Device Information")
    print_info(f"Platform    : {info['platform'].upper()}")
    print_info(f"OS Name     : {info['os_name']}")
    print_info(f"Hostname    : {info['hostname']}")
    print_info(f"CPU Cores   : {info['cpu_cores']}")
    print_info(f"Screen      : {info['screen_width']}x{info['screen_height']}")
    print_info(f"Timezone    : {info['timezone_name']}")
    print_info(f"Language    : {info['browser_lang']}")
    print_info(f"Device Hash : {info['device_hash']}")
    print_info(f"Termux      : {'Yes' if info['is_termux'] else 'No'}")
    print()
    print_instruction("This fingerprint data is used for all claim requests.")
    print_instruction("Each device gets a unique, consistent fingerprint.")
    input("\nPress Enter to continue...")

def show_set_account_menu(config):
    """Menu for setting FaucetPay account details"""
    clear_screen()
    bot.show_menu_banner("Altcryp")
    print_header("Set Account")
    print_instruction("Enter your FaucetPay email address")
    print()
    
    current_wallet = config.get('wallet', '')
    if current_wallet:
        print_info(f"Current: {current_wallet}")
    else:
        print_warning("No wallet set!")
    print()
    
    wallet = get_input_with_default("FaucetPay Email", current_wallet)
    config['wallet'] = wallet
    save_config(config)
    print_success("Account updated successfully!")
    input("\nPress Enter to continue...")

def show_set_solver_menu(config):
    """Menu for selecting captcha solver method"""
    while True:
        clear_screen()
        bot.show_menu_banner("Altcryp")
        print_header("Set Solver")
        print_instruction("Select captcha solving method")
        print()
        
        current_mode = config.get('solver_mode', 'api')
        current_name = SOLVER_MODES.get(current_mode, 'Unknown')
        print_info(f"Current solver: {C['green']}{current_name}{C['reset']}")
        print()
        print(f" {C['gray']}{'─'*55}{C['reset']}")
        
        print(f"  {C['menu']}[1]{C['reset']} {SOLVER_MODES['api']}")
        
        if SELEDROID_AVAILABLE:
            print(f"  {C['menu']}[2]{C['reset']} {SOLVER_MODES['seledroid_fullscreen']}")
            print(f"  {C['menu']}[3]{C['reset']} {SOLVER_MODES['seledroid_interstitial']}")
        else:
            print(f"  {C['red']}[2] Seledroid [UNAVAILABLE - Install module]{C['reset']}")
        
        print(f"  {C['gold']}[B] Back to Main Menu{C['reset']}")
        print(f" {C['gray']}{'─'*55}{C['reset']}")
        
        choice = input(f"\n{C['menu']}Select solver: {C['reset']}").strip().lower()
        
        if choice == '1':
            clear_screen()
            bot.show_menu_banner("Altcryp")
            print_header("BypassAllShortLinks API")
            print_instruction("Enter your API key from bypassallshortlinks.space")
            print()
            
            current_key = config.get('api_key', '')
            if current_key:
                masked = current_key[:4] + "****" + current_key[-4:] if len(current_key) > 8 else "****"
                print_info(f"Current: {masked}")
            else:
                print_warning("No API key set!")
            print()
            
            api_key = get_input_with_default("API Key", current_key)
            config['api_key'] = api_key
            config['solver_mode'] = 'api'
            save_config(config)
            print_success("Solver set to: BypassAllShortLinks API")
            input("\nPress Enter to continue...")
            return
        
        elif choice == '2' and SELEDROID_AVAILABLE:
            config['solver_mode'] = 'seledroid_fullscreen'
            save_config(config)
            print_success("Solver set to: Seledroid [FULLSCREEN]")
            print_instruction("Browser will open in FULL SCREEN for manual captcha solving")
            input("\nPress Enter to continue...")
            return
        
        elif choice == '3' and SELEDROID_AVAILABLE:
            config['solver_mode'] = 'seledroid_interstitial'
            save_config(config)
            print_success("Solver set to: Seledroid [INTERSTITIAL]")
            print_instruction("Browser will open as SIDE PANEL for manual captcha solving")
            input("\nPress Enter to continue...")
            return
        
        elif choice == 'b':
            return
        
        else:
            print_error("Invalid option!")
            time.sleep(1)

def show_main_menu():
    clear_screen()
    bot.show_menu_banner("Altcryp")
    print_header("Altcryp Bot - Main Menu")
    
    # Show Seledroid status
    if SELEDROID_AVAILABLE:
        print(f"  {C['green']}◆ Seledroid: AVAILABLE{C['reset']}")
    else:
        print(f"  {C['red']}◆ Seledroid: NOT AVAILABLE{C['reset']}")
    print()
    
    menu_options = {
        '1': 'Set Account (FaucetPay Email)',
        '2': 'Set Solver (Captcha Method)',
        '3': 'Set User Agent',
        '4': 'View Device Info',
        '5': 'Select Coins & Start Claiming',
        '6': 'Exit'
    }
    return get_menu_choice("Main Menu:", menu_options)

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

def main():
    config = load_config()
    
    while True:
        choice = show_main_menu()
        
        if choice == '1':
            show_set_account_menu(config)
            
        elif choice == '2':
            show_set_solver_menu(config)
            
        elif choice == '3':
            clear_screen()
            bot.show_menu_banner("Altcryp")
            print_header("Set User Agent")
            current = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            new_ua = get_input_with_default("Enter User Agent", current)
            config['user_agent'] = new_ua
            save_config(config)
            print_success("User Agent updated")
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            show_device_info()
            
        elif choice == '5':
            clear_screen()
            bot.show_menu_banner("Altcryp")
            
            if not config.get('wallet'):
                print_error("Wallet is required! Go to: Set Account")
                input("\nPress Enter to continue...")
                continue
            
            solver_mode = config.get('solver_mode', 'api')
            if solver_mode == 'api' and not config.get('api_key'):
                print_error("API Key required! Go to: Set Solver")
                input("\nPress Enter to continue...")
                continue
            
            if solver_mode.startswith('seledroid') and not SELEDROID_AVAILABLE:
                print_error("Seledroid not available!")
                input("\nPress Enter to continue...")
                continue
            
            bot_obj = AltcrypBot(config)
            
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
