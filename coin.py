#!/usr/bin/env python3
"""
CoinPayuFree Bot - Complete Automation Script
"""

import os
import sys
import time
import json
import re
import random
import requests
from bs4 import BeautifulSoup

# ============================================================
# PSYCHO UI - Complete UI Framework
# ============================================================
class PsychoUI:
    def __init__(self, typing_speed=0.002):
        self.speed = typing_speed
        self.success_history = []
        self.max_history = 5
        self.display_success = True
        
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
        self.user = None
        self.balance = None

    def type_text(self, text, color="", delay=0.001):
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    def show_banner(self, faucet_name="CoinPayuFree", show_success=True):
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
        
        if self.user and self.balance is not None:
            print(f" {self.gray}│ {self.reset}User     {self.gray}» {self.green}{self.user:<20} {self.gray}│ {self.reset}Balance  {self.gray}» {self.gold}{self.balance:<10} coins {self.gray}│{self.reset}")
        
        print(f" {self.gray}└──────────────────────────────────────────────────────────────┘{self.reset}\n")

        if show_success and self.success_history:
            for past_success in self.success_history[-self.max_history:]:
                print(f" {self.green}✨ {past_success}{self.reset}")
                print(f" {self.gray}────────────────────────────────────────────────────────────{self.reset}")
            print()

    def set_user_info(self, user, balance):
        self.user = user
        self.balance = balance

    def info(self, message):
        self.type_text(f"  {self.gray}• {self.reset}{message}", self.gray, 0.001)

    def warning(self, message):
        self.type_text(f"  {self.yellow}⚠ {self.reset}{message}", self.yellow, 0.002)

    def error(self, message):
        self.type_text(f"  {self.red}✘ {self.reset}{message}", self.red, 0.002)

    def success(self, message, faucet_name="CoinPayuFree"):
        self.success_history.append(message)
        if len(self.success_history) > self.max_history:
            self.success_history = self.success_history[-self.max_history:]
        self.show_banner(faucet_name, True)

    def show_menu_banner(self, faucet_name="CoinPayuFree"):
        self.show_banner(faucet_name, False)

    def inline_status(self, text, color="\033[38;5;223m"):
        max_len = 80
        if len(text) > max_len:
            text = text[:max_len-3] + "..."
        sys.stdout.write(f"\r  {color}▶ {self.reset}{text}")
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
            bar = '█' * filled + '░' * (bar_length - filled)
            sys.stdout.write(f"\r  {self.yellow}⏳ {self.reset}{label} [{self.sec}{bar}{self.reset}] {self.gold}{percent:.0f}%{self.reset}")
            sys.stdout.flush()
            if i < seconds:
                time.sleep(1)
        sys.stdout.write("\r" + " " * 90 + "\r")
        sys.stdout.flush()

    def progress_bar(self, current, total, label="Progress"):
        if total <= 0:
            return
        percent = (current / total) * 100
        bar_length = 30
        filled = int(bar_length * current // total)
        bar = '█' * filled + '░' * (bar_length - filled)
        sys.stdout.write(f"\r  {self.sec}▶ {self.reset}{label} [{self.gold}{bar}{self.reset}] {self.green}{percent:.0f}%{self.reset}")

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
BASE_URL = "https://coinpayufree.com"
LOGIN_URL = f"{BASE_URL}/login"
LOGIN_ACTION = f"{BASE_URL}/auth/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
FAUCET_URL = f"{BASE_URL}/faucet"
FAUCET_CLAIM_URL = f"{BASE_URL}/faucet/verify"
WHEEL_URL = f"{BASE_URL}/wheel"
WHEEL_START_URL = f"{BASE_URL}/wheel/start_claim"
WHEEL_VERIFY_URL = f"{BASE_URL}/wheel/complete_claim"
DAILY_BONUS_URL = f"{BASE_URL}/bonus"
DAILY_CLAIM_URL = f"{BASE_URL}/bonus/claim"
WITHDRAWAL_URL = f"{BASE_URL}/withdraw"
WITHDRAWAL_POST_URL = f"{BASE_URL}/dashboard/withdraw"

TURNSTILE_SITEKEY = "0x4AAAAAAAhdmcfO-UZf-p6L"
RECAPTCHA_SITEKEY = "6LfrI8cpAAAAAD9fihZI_2p3IyMRNiPGwHwuYkr-"

SESSION_FILE = "coinpayu_session.json"
CONFIG_FILE = "coinpayu_config.json"

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
        "email": "", 
        "password": "", 
        "multibot_key": "", 
        "bypass_key": "",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "withdraw_method": "faucetpay", 
        "faucetpay_email": "", 
        "withdraw_amount": "",
        "recaptcha_solver": "multibot",
        "antibot_solver": "bypassallshortlink",
        "turnstile_solver": "bypassallshortlink"
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
# CAPTCHA SOLVERS
# ============================================================

# ----- MultiBot API (reCAPTCHA v2 & Turnstile) -----
def solve_multibot_captcha(api_key, method, sitekey, pageurl, max_attempts=20):
    bot.inline_status(f"Solving {method} via MultiBot...")
    
    try:
        params = {
            "key": api_key,
            "method": method,
            "pageurl": pageurl,
            "json": "1",
        }
        
        if method == "userrecaptcha":
            params["googlekey"] = sitekey
        elif method == "turnstile":
            params["sitekey"] = sitekey
        
        files = {k: (None, v) for k, v in params.items()}
        resp = requests.post("https://api.multibot.cloud/in.php", files=files, timeout=30)
        result = resp.json()
        
        if result.get("status") == 1:
            task_id = result.get("request")
            bot.inline_status(f"Task ID: {task_id}")
            
            for attempt in range(max_attempts):
                time.sleep(5)
                poll_resp = requests.get(
                    f"https://api.multibot.cloud/res.php?key={api_key}&action=get&id={task_id}&json=1",
                    timeout=30
                )
                poll_result = poll_resp.json()
                
                if poll_result.get("status") == 1:
                    token = poll_result.get("request")
                    bot.clear_inline()
                    bot.info(f"{method} solved via MultiBot")
                    return token
                elif poll_result.get("request") == "CAPCHA_NOT_READY":
                    bot.inline_status(f"Solving... ({attempt+1}/{max_attempts})")
                    continue
                else:
                    bot.warning(f"Error: {poll_result.get('request')}")
                    return None
        else:
            bot.warning(f"Error: {result.get('request')}")
            return None
    except Exception as e:
        bot.warning(f"MultiBot error: {str(e)}")
        return None

# ----- BypassAllShortLink API (reCAPTCHA v2, Turnstile, AntiBot) -----
def solve_bypassall_captcha(api_key, method, sitekey, pageurl, max_attempts=20):
    bot.inline_status(f"Solving {method} via BypassAllShortLink...")
    api_base = "https://bypassallshortlinks.space"
    
    try:
        resp = requests.get(f"{api_base}/in.php", params={'key': api_key, 'method': method, 'pageurl': pageurl, 'sitekey': sitekey}, timeout=30)
        result = resp.text.strip()
        
        if result.startswith('OK|'):
            task_id = result.split('|')[1]
            for attempt in range(max_attempts):
                time.sleep(5)
                poll_resp = requests.get(f"{api_base}/res.php", params={'key': api_key, 'id': task_id}, timeout=30)
                poll_result = poll_resp.text.strip()
                
                if poll_result == 'CAPCHA_NOT_READY':
                    bot.inline_status(f"Solving... ({attempt+1}/{max_attempts})")
                    continue
                elif poll_result.startswith('OK|'):
                    token = poll_result.split('|')[1]
                    bot.clear_inline()
                    bot.info(f"{method} solved via BypassAllShortLink")
                    return token
                else:
                    bot.warning(f"Error: {poll_result}")
                    return None
        else:
            bot.warning(f"Error: {result}")
            return None
    except Exception as e:
        bot.warning(f"BypassAllShortLink error: {str(e)}")
        return None

def solve_bypassall_antibot(html, api_key):
    bot.inline_status("Solving AntiBot via BypassAllShortLink...")
    soup = BeautifulSoup(html, 'html.parser')
    alert = soup.find('div', class_='alert-warning') or soup.find('p', class_='alert-warning')
    if not alert:
        return None
    
    main_img = alert.find('img')
    if not main_img or 'src' not in main_img.attrs:
        return None
    
    main_src = main_img['src']
    if not main_src.startswith('data:image/png;base64,'):
        return None
    
    main_base64 = main_src.split(',')[1]
    
    script = soup.find('script', string=re.compile(r'var ablinks='))
    if not script:
        return None
    
    script_text = script.string
    matches = re.findall(r'rel="(\d+)".*?src="data:image/png;base64,([^"]+)"', script_text, re.DOTALL)
    if not matches:
        matches = re.findall(r'rel=\\"(\d+)\\".*?src=\\"data:image/png;base64,([^\\\"]+)\\"', script_text, re.DOTALL)
    if not matches:
        matches = re.findall(r"rel='(\d+)'.*?src='data:image/png;base64,([^']+)'", script_text, re.DOTALL)
    
    if not matches:
        return None
    
    options = {}
    rel_mapping = {}
    for idx, (rel, base64_str) in enumerate(matches, 1):
        options[str(idx)] = base64_str
        rel_mapping[str(idx)] = rel
    
    api_url = "https://bypassallshortlinks.space/api.php"
    api_payload = {'api_key': api_key, 'action': 'antibot', 'main': main_base64, 'options': options}
    
    try:
        api_res = requests.post(api_url, json=api_payload, timeout=30)
        task_resp = api_res.text.strip()
        bot.inline_status(f"AntiBot: {task_resp}")
        
        if "id" in task_resp.lower() or task_resp.isdigit():
            task_id = re.sub(r'[^0-9]', '', task_resp)
            if task_id:
                for _ in range(20):
                    time.sleep(3)
                    get_res = requests.get(f"https://bypassallshortlinks.space/res.php?id={task_id}&key={api_key}", timeout=10)
                    order_string = get_res.text.strip()
                    if order_string and "NOTREADY" not in order_string and "ERROR" not in order_string:
                        if ',' in order_string:
                            result = " " + " ".join([rel_mapping[idx.strip()] for idx in order_string.split(',') if idx.strip() in rel_mapping])
                            bot.clear_inline()
                            bot.info("AntiBot solved via BypassAllShortLink")
                            return result
        else:
            if ',' in task_resp:
                result = " " + " ".join([rel_mapping[idx.strip()] for idx in task_resp.split(',') if idx.strip() in rel_mapping])
                bot.clear_inline()
                bot.info("AntiBot solved via BypassAllShortLink")
                return result
    except:
        pass
    return None

# ============================================================
# SOLVER WRAPPER FUNCTIONS
# ============================================================
def solve_recaptcha_v2(sitekey, pageurl, config):
    solver = config.get("recaptcha_solver", "multibot")
    api_key = config.get("multibot_key" if solver == "multibot" else "bypass_key", "")
    
    if solver == "multibot":
        return solve_multibot_captcha(api_key, "userrecaptcha", sitekey, pageurl)
    elif solver == "bypassallshortlink":
        return solve_bypassall_captcha(api_key, "recaptcha", sitekey, pageurl)
    return None

def solve_turnstile(sitekey, pageurl, config):
    solver = config.get("turnstile_solver", "bypassallshortlink")
    api_key = config.get("bypass_key" if solver == "bypassallshortlink" else "multibot_key", "")
    
    if solver == "multibot":
        return solve_multibot_captcha(api_key, "turnstile", sitekey, pageurl)
    elif solver == "bypassallshortlink":
        return solve_bypassall_captcha(api_key, "turnstile", sitekey, pageurl)
    return None

def solve_antibot(html, config):
    solver = config.get("antibot_solver", "bypassallshortlink")
    api_key = config.get("bypass_key", "")
    
    if solver == "bypassallshortlink":
        return solve_bypassall_antibot(html, api_key)
    return None

# ============================================================
# MAIN BOT
# ============================================================
class CoinPayuBot:
    def __init__(self, config):
        self.config = config
        self.email = config.get("email", "")
        self.password = config.get("password", "")
        self.user_agent = config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.withdraw_method = config.get("withdraw_method", "faucetpay")
        self.faucetpay_email = config.get("faucetpay_email", "")
        self.withdraw_amount = config.get("withdraw_amount", "")
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        saved = load_session()
        if saved and saved.get("user_agent"):
            self.user_agent = saved["user_agent"]
            for name, value in saved["cookies"].items():
                self.session.cookies.set(name, value, domain="coinpayufree.com")
        
        self.logged_in = False
        self.balance = 0
        self.username = ""
        self.csrf_token = ""
        self.faucet_last_claim = 0
        self.faucet_wait_time = 3900  # 65 minutes in seconds
        
    def _headers(self, extra=None):
        headers = {'User-Agent': self.user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection': 'keep-alive', 'Referer': BASE_URL}
        if extra:
            headers.update(extra)
        return headers
    
    def _get_csrf(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        csrf = soup.find('input', {'name': 'csrf_token_name'}) or soup.find('input', {'id': 'token'})
        return csrf.get('value') if csrf else None
    
    def _get_swal_message(self, html):
        match = re.search(r"Swal\.fire\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)", html)
        if match:
            return {"title": match.group(1), "text": match.group(2), "icon": match.group(3)}
        match = re.search(r"text:\s*'([^']+)'", html)
        if match:
            return {"title": "", "text": match.group(1), "icon": "info"}
        return None
    
    def _get_balance(self, html):
        match = re.search(r'Balance:?\s*<b>([\d,]+)\s*coins?</b>', html, re.IGNORECASE)
        if match:
            return int(match.group(1).replace(',', ''))
        return 0
    
    def _get_username(self, html):
        match = re.search(r'key="t-henry">([^<]+)</span>', html)
        if match:
            return match.group(1).strip()
        return None
    
    def is_session_valid(self):
        try:
            resp = self.session.get(DASHBOARD_URL, headers=self._headers(), timeout=10, allow_redirects=False)
            if resp.status_code == 200 and '<title>Dashboard' in resp.text:
                return True
            if '/login' in resp.headers.get('Location', ''):
                return False
            return False
        except:
            return False
    
    def login(self):
        bot.info("Logging in...")
        for attempt in range(1, 4):
            try:
                resp = self.session.get(LOGIN_URL, headers=self._headers(), timeout=15)
                if resp.status_code != 200:
                    time.sleep(2)
                    continue
                
                csrf = self._get_csrf(resp.text)
                if not csrf:
                    time.sleep(2)
                    continue
                
                recaptcha = solve_recaptcha_v2(RECAPTCHA_SITEKEY, LOGIN_URL, self.config)
                if not recaptcha:
                    time.sleep(3)
                    continue
                
                payload = {
                    'csrf_token_name': csrf,
                    'email': self.email,
                    'password': self.password,
                    'captcha': 'recaptchav2',
                    'g-recaptcha-response': recaptcha
                }
                time.sleep(random.uniform(1, 2))
                
                resp = self.session.post(LOGIN_ACTION, data=payload, headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}), timeout=30, allow_redirects=True)
                
                if '<title>Dashboard' in resp.text or '/dashboard' in resp.url:
                    cookies = self.session.cookies.get_dict()
                    save_session(cookies, self.user_agent)
                    self.logged_in = True
                    self.balance = self._get_balance(resp.text)
                    self.username = self._get_username(resp.text)
                    
                    bot.set_user_info(self.username, self.balance)
                    
                    bot.info(f"Login successful! User: {self.username}")
                    bot.info(f"Balance: {self.balance} coins")
                    return True
                time.sleep(3)
            except:
                time.sleep(3)
        return False
    
    def ensure_logged_in(self):
        if self.logged_in and self.is_session_valid():
            self.check_dashboard()
            return True
        return self.login()
    
    def check_dashboard(self):
        try:
            resp = self.session.get(DASHBOARD_URL, headers=self._headers(), timeout=15)
            if resp.status_code == 200:
                self.balance = self._get_balance(resp.text)
                self.username = self._get_username(resp.text)
                bot.set_user_info(self.username, self.balance)
                return True
        except:
            pass
        return False
    
    def claim_wheel(self):
        try:
            resp = self.session.get(WHEEL_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                return False
            
            html = resp.text
            
            # Check timer from HTML
            timer = re.search(r'id="minute">(\d+)</div>.*?id="second">(\d+)</div>', html, re.DOTALL)
            if timer:
                total = int(timer.group(1)) * 60 + int(timer.group(2))
                if total > 0:
                    bot.info(f"Wheel cooldown: {total}s")
                    bot.countdown(total + 2, "Wheel Timer")
                    return self.claim_wheel()
            
            # Check if wheel is ready
            if 'proverka' not in html or 'progress-wrapper' not in html:
                bot.info("Wheel not ready, waiting...")
                time.sleep(5)
                return self.claim_wheel()
            
            bot.info("Wheel ready! Spinning...")
            
            resp = self.session.post(WHEEL_START_URL, headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}), timeout=15)
            data = resp.json()
            
            if data.get('status') != 'success':
                bot.warning(f"Wheel start failed: {data.get('status')}")
                return False
            
            token = data.get('token')
            if not token:
                bot.warning("No token received")
                return False
            
            wait = data.get('seconds', 10)
            bot.info(f"Waiting {wait}s for result...")
            bot.countdown(wait + random.randint(2, 4), "Processing")
            
            resp = self.session.post(WHEEL_VERIFY_URL, data={'token': token}, headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}), timeout=15)
            data = resp.json()
            
            if data.get('status') == 'success':
                msg = data.get('reward', 'coins')
                bot.success(f"God job! {msg} added your balance.", "CoinPayuFree")
                self.check_dashboard()
                return True
            else:
                bot.warning(f"Wheel claim failed: {data.get('status')}")
                return False
        except Exception as e:
            bot.warning(f"Wheel error: {str(e)}")
            return False
    
    def claim_faucet(self):
        # Check if 65 minutes have passed since last claim
        current_time = time.time()
        if current_time - self.faucet_last_claim < self.faucet_wait_time and self.faucet_last_claim > 0:
            remaining = int(self.faucet_wait_time - (current_time - self.faucet_last_claim))
            bot.info(f"Faucet cooldown: {remaining}s remaining (65 minutes wait)")
            bot.countdown(remaining, "Faucet Cooldown")
            return self.claim_faucet()
        
        try:
            resp = self.session.get(FAUCET_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                return False
            
            html = resp.text
            
            # Check if redirected to wait page
            if '/wait' in resp.url:
                wait_match = re.search(r'id="countdown">(\d+)</span>', resp.text)
                if wait_match:
                    total = int(wait_match.group(1))
                    bot.info(f"Faucet cooldown: {total}s")
                    bot.countdown(total + 5, "Faucet Timer")
                    return self.claim_faucet()
            
            csrf = self._get_csrf(html)
            
            # If no CSRF token, wait 65 minutes
            if not csrf:
                bot.info("No CSRF token found. Waiting 65 minutes...")
                self.faucet_last_claim = time.time()
                bot.countdown(self.faucet_wait_time, "Faucet Wait (65 min)")
                return self.claim_faucet()
            
            bot.info("Faucet ready! Claiming...")
            
            # Solve AntiBot
            antibot = solve_antibot(html, self.config)
            if not antibot:
                antibot = " 7499 1023 7320"
            
            # Solve Turnstile
            turnstile = solve_turnstile(TURNSTILE_SITEKEY, FAUCET_URL, self.config)
            if not turnstile:
                return False
            
            payload = {
                'antibotlinks': antibot,
                'csrf_token_name': csrf,
                'captcha': 'turnstile',
                'cf-turnstile-response': turnstile
            }
            time.sleep(random.uniform(1, 2))
            
            resp = self.session.post(FAUCET_CLAIM_URL, data=payload, headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}), timeout=30, allow_redirects=True)
            
            # Check if redirected to wait page after claim
            if '/wait' in resp.url:
                wait_match = re.search(r'id="countdown">(\d+)</span>', resp.text)
                if wait_match:
                    total = int(wait_match.group(1))
                    bot.info(f"Faucet cooldown: {total}s")
                    bot.countdown(total + 5, "Faucet Timer")
                    return self.claim_faucet()
            
            # Check for success message
            swal = self._get_swal_message(resp.text)
            if swal:
                if swal['icon'] == 'success':
                    bot.success(f"Good job! {swal['text']}", "CoinPayuFree")
                    self.balance += 50
                    bot.set_user_info(self.username, self.balance)
                    self.faucet_last_claim = time.time()
                    return True
                else:
                    bot.warning(f"{swal['text']}")
                    self.faucet_last_claim = time.time()
                    bot.info("Waiting 65 minutes before next attempt...")
                    bot.countdown(self.faucet_wait_time, "Faucet Wait (65 min)")
                    return self.claim_faucet()
            
            # Check for any success indicator
            if 'coins' in resp.text and 'added' in resp.text:
                match = re.search(r"Swal\.fire\(\s*'Good job!',\s*'([^']+)'", resp.text)
                if match:
                    bot.success(f"Good job! {match.group(1)}", "CoinPayuFree")
                else:
                    bot.success("Good job! 50 coins has been added to your balance", "CoinPayuFree")
                self.balance += 50
                bot.set_user_info(self.username, self.balance)
                self.faucet_last_claim = time.time()
                return True
            
            # If no success, wait 65 minutes
            self.faucet_last_claim = time.time()
            bot.info("Faucet claim failed. Waiting 65 minutes...")
            bot.countdown(self.faucet_wait_time, "Faucet Wait (65 min)")
            return self.claim_faucet()
            
        except Exception as e:
            bot.warning(f"Faucet error: {str(e)}")
            self.faucet_last_claim = time.time()
            return False
    
    def claim_daily_bonus(self):
        try:
            resp = self.session.get(DAILY_BONUS_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                return False
            
            csrf = self._get_csrf(resp.text)
            if not csrf:
                bot.info("Daily Bonus not available")
                return False
            
            bot.info("Daily Bonus ready! Claiming...")
            
            resp = self.session.post(DAILY_CLAIM_URL, data={'csrf_token_name': csrf}, headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}), timeout=30, allow_redirects=True)
            
            swal = self._get_swal_message(resp.text)
            if swal:
                if swal['icon'] == 'success':
                    bot.success(f"Good job! {swal['text']}", "CoinPayuFree")
                    self.balance += 80
                    bot.set_user_info(self.username, self.balance)
                    return True
                else:
                    bot.warning(f"{swal['text']}")
                    return False
            return False
        except Exception as e:
            bot.warning(f"Daily bonus error: {str(e)}")
            return False
    
    def process_withdrawal(self):
        if not self.withdraw_amount:
            return False
        
        try:
            resp = self.session.get(WITHDRAWAL_URL, headers=self._headers(), timeout=15)
            if resp.status_code != 200:
                return False
            
            csrf = self._get_csrf(resp.text)
            if not csrf:
                return False
            
            self.check_dashboard()
            bot.info(f"Withdrawing {self.withdraw_amount} coins...")
            
            turnstile = solve_turnstile(TURNSTILE_SITEKEY, WITHDRAWAL_URL, self.config)
            
            payload = {
                'csrf_token_name': csrf,
                'method': '10',
                'amount': self.withdraw_amount,
                'wallet': self.faucetpay_email if self.withdraw_method == 'faucetpay' else self.email,
                'captcha': 'turnstile'
            }
            if turnstile:
                payload['cf-turnstile-response'] = turnstile
            
            time.sleep(random.uniform(1, 2))
            resp = self.session.post(WITHDRAWAL_POST_URL, data=payload, headers=self._headers({'Content-Type': 'application/x-www-form-urlencoded'}), timeout=30, allow_redirects=True)
            
            swal = self._get_swal_message(resp.text)
            if swal:
                if swal['icon'] == 'success':
                    bot.success(f"Good job! {swal['text']}", "CoinPayuFree")
                    self.balance -= int(self.withdraw_amount)
                    bot.set_user_info(self.username, self.balance)
                    return True
                else:
                    bot.warning(f"{swal['text']}")
                    return False
            return False
        except Exception as e:
            bot.warning(f"Withdrawal error: {str(e)}")
            return False

# ============================================================
# COLORFUL MENU FUNCTIONS
# ============================================================
def print_header(text):
    print(f"{C['header']}{'═'*55}{C['reset']}")
    print(f"{C['header']}  {text}{C['reset']}")
    print(f"{C['header']}{'═'*55}{C['reset']}")

def print_menu_option(key, value, status=None):
    if status:
        print(f"  {C['menu']}▶ [{key}]{C['reset']} {value} {C['green']}[{status}]{C['reset']}")
    else:
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
    bot.show_menu_banner("CoinPayuFree")
    print_header("CoinPayuFree Bot")
    
    menu_options = {
        '1': 'Set User Agent',
        '2': 'Set Email & Password',
        '3': 'Set Solver',
        '4': 'Set Withdraw',
        '5': 'Start Work',
        '6': 'Exit'
    }
    return get_menu_choice("Main Menu:", menu_options)

def show_work_menu():
    bot.show_menu_banner("CoinPayuFree")
    print_header("Start Work")
    
    work_options = {
        '1': 'Daily Bonus',
        '2': 'Manual Faucet',
        '3': 'Wheel Faucet',
        '4': 'Withdraw',
        '5': 'All Tasks (Loop)'
    }
    return get_menu_choice("Select Task:", work_options)

def show_solver_menu(config):
    bot.show_menu_banner("CoinPayuFree")
    print_header("Set Solver")
    
    recaptcha_solver = config.get("recaptcha_solver", "multibot")
    antibot_solver = config.get("antibot_solver", "bypassallshortlink")
    turnstile_solver = config.get("turnstile_solver", "bypassallshortlink")
    
    multibot_key = config.get("multibot_key", "")
    bypass_key = config.get("bypass_key", "")
    
    print(f"\n{C['gray']}Current Solver Status:{C['reset']}")
    print(f"  {C['menu']}▶ reCAPTCHA v2    : {C['green']}{recaptcha_solver}{C['reset']} {C['green']}[{'ON' if multibot_key or bypass_key else 'OFF'}]{C['reset']}")
    print(f"  {C['menu']}▶ AntiBot         : {C['green']}{antibot_solver}{C['reset']} {C['green']}[{'ON' if bypass_key else 'OFF'}]{C['reset']}")
    print(f"  {C['menu']}▶ Turnstile       : {C['green']}{turnstile_solver}{C['reset']} {C['green']}[{'ON' if multibot_key or bypass_key else 'OFF'}]{C['reset']}")
    print()
    
    solver_options = {
        '1': f"reCAPTCHA v2 (Current: {recaptcha_solver})",
        '2': f"AntiBot (Current: {antibot_solver})",
        '3': f"Turnstile (Current: {turnstile_solver})",
        '4': 'Set MultiBot API Key',
        '5': 'Set BypassAllShortLink API Key',
        '6': 'Back to Main Menu'
    }
    choice = get_menu_choice("Solver Menu:", solver_options)
    
    if choice == '1':
        bot.show_menu_banner("CoinPayuFree")
        print_header("reCAPTCHA v2 Solver")
        print(f"\n{C['gray']}Select solver for reCAPTCHA v2 (used for Login):{C['reset']}")
        recaptcha_options = {
            '1': 'MultiBot',
            '2': 'BypassAllShortLink',
            '3': 'Back'
        }
        opt = get_menu_choice("Choose:", recaptcha_options)
        if opt == '1':
            config['recaptcha_solver'] = 'multibot'
            print_success("reCAPTCHA v2 solver set to: MultiBot")
        elif opt == '2':
            config['recaptcha_solver'] = 'bypassallshortlink'
            print_success("reCAPTCHA v2 solver set to: BypassAllShortLink")
        save_config(config)
        input("\nPress Enter to continue...")
        return show_solver_menu(config)
    
    elif choice == '2':
        bot.show_menu_banner("CoinPayuFree")
        print_header("AntiBot Solver")
        print(f"\n{C['gray']}Select solver for AntiBot (used in Faucet):{C['reset']}")
        print_warning("Only BypassAllShortLink supports AntiBot")
        antibot_options = {
            '1': 'BypassAllShortLink',
            '2': 'Back'
        }
        opt = get_menu_choice("Choose:", antibot_options)
        if opt == '1':
            config['antibot_solver'] = 'bypassallshortlink'
            print_success("AntiBot solver set to: BypassAllShortLink")
        save_config(config)
        input("\nPress Enter to continue...")
        return show_solver_menu(config)
    
    elif choice == '3':
        bot.show_menu_banner("CoinPayuFree")
        print_header("Turnstile Solver")
        print(f"\n{C['gray']}Select solver for Cloudflare Turnstile (used in Faucet/Withdraw):{C['reset']}")
        turnstile_options = {
            '1': 'MultiBot',
            '2': 'BypassAllShortLink',
            '3': 'Back'
        }
        opt = get_menu_choice("Choose:", turnstile_options)
        if opt == '1':
            config['turnstile_solver'] = 'multibot'
            print_success("Turnstile solver set to: MultiBot")
        elif opt == '2':
            config['turnstile_solver'] = 'bypassallshortlink'
            print_success("Turnstile solver set to: BypassAllShortLink")
        save_config(config)
        input("\nPress Enter to continue...")
        return show_solver_menu(config)
    
    elif choice == '4':
        bot.show_menu_banner("CoinPayuFree")
        print_header("Set MultiBot API Key")
        current = config.get('multibot_key', '')
        api_key = get_input_with_default("Enter MultiBot API Key", current)
        config['multibot_key'] = api_key
        save_config(config)
        print_success("MultiBot API Key updated")
        input("\nPress Enter to continue...")
        return show_solver_menu(config)
    
    elif choice == '5':
        bot.show_menu_banner("CoinPayuFree")
        print_header("Set BypassAllShortLink API Key")
        current = config.get('bypass_key', '')
        api_key = get_input_with_default("Enter BypassAllShortLink API Key", current)
        config['bypass_key'] = api_key
        save_config(config)
        print_success("BypassAllShortLink API Key updated")
        input("\nPress Enter to continue...")
        return show_solver_menu(config)
    
    elif choice == '6':
        return

def main():
    config = load_config()
    
    while True:
        choice = show_main_menu()
        
        if choice == '1':
            bot.show_menu_banner("CoinPayuFree")
            print_header("Set User Agent")
            print_instruction("User Agent is used to identify your browser to the website.")
            print_instruction("Default user agent works for most cases.")
            current = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            new_ua = get_input_with_default("Enter User Agent", current)
            config['user_agent'] = new_ua
            save_config(config)
            print_success("User Agent updated")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            bot.show_menu_banner("CoinPayuFree")
            print_header("Set Email & Password")
            print_instruction("If you don't have an account yet, please register at:")
            print_instruction(f"{C['menu']}https://coinpayufree.com/register{C['reset']}")
            print_instruction("After registration, enter your registered email and password below.")
            print()
            
            email = get_input_with_default("Email", config.get('email', ''))
            password = get_input_with_default("Password", config.get('password', ''))
            config['email'] = email
            config['password'] = password
            save_config(config)
            print_success("Email updated")
            print_success("Password updated")
            print_instruction("You can now use Start Work option to begin earning coins.")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            show_solver_menu(config)
            
        elif choice == '4':
            bot.show_menu_banner("CoinPayuFree")
            print_header("Set Withdraw")
            print_instruction("Set up your withdrawal preferences.")
            print_instruction("Choose your withdrawal method and enter the amount.")
            print()
            
            method_choice = get_menu_choice("Select Withdraw Method:", {'1': 'faucetpay', '2': 'email'})
            method = 'faucetpay' if method_choice == '1' else 'email'
            config['withdraw_method'] = method
            
            if method == 'faucetpay':
                email = get_input_with_default("FaucetPay Email", config.get('faucetpay_email', ''))
                config['faucetpay_email'] = email
                print_info(f"FaucetPay Email: {email}")
            else:
                print_info(f"Using email: {config.get('email', 'Not set')}")
            
            amount = get_input_with_default("Withdraw Amount (coins)", config.get('withdraw_amount', '1000'))
            config['withdraw_amount'] = amount
            save_config(config)
            print_success(f"Withdraw set: {amount} coins via {method}")
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            work_choice = show_work_menu()
            
            if not config.get('email') or not config.get('password'):
                bot.show_menu_banner("CoinPayuFree")
                print_error("Email and Password not set!")
                print_instruction("Please go to [2] Set Email & Password first.")
                input("\nPress Enter to continue...")
                continue
            
            bot_obj = CoinPayuBot(config)
            
            bot.show_menu_banner("CoinPayuFree")
            
            if not bot_obj.ensure_logged_in():
                print_error("Login failed!")
                print_instruction("Please check your email and password.")
                input("\nPress Enter to continue...")
                continue
            
            if work_choice == '1':
                bot_obj.claim_daily_bonus()
            elif work_choice == '2':
                bot_obj.claim_faucet()
            elif work_choice == '3':
                bot_obj.claim_wheel()
            elif work_choice == '4':
                if config.get('withdraw_amount'):
                    bot_obj.process_withdrawal()
                else:
                    print_error("Withdraw amount not set!")
            elif work_choice == '5':
                bot.info("Starting Auto Loop...")
                try:
                    while True:
                        print()
                        bot.info("─── New Cycle ───")
                        if not bot_obj.ensure_logged_in():
                            break
                        
                        bot_obj.claim_daily_bonus()
                        time.sleep(3)
                        
                        bot_obj.claim_wheel()
                        time.sleep(3)
                        
                        bot_obj.claim_faucet()
                        time.sleep(3)
                        
                        bot_obj.check_dashboard()
                        bot.info(f"Balance: {bot_obj.balance} coins")
                        
                        if bot_obj.balance >= 1000 and config.get('withdraw_amount'):
                            bot_obj.process_withdrawal()
                        
                        wait = random.randint(60, 120)
                        bot.info(f"Next cycle in {wait} seconds")
                        bot.countdown(wait, "Cycle Timer")
                except KeyboardInterrupt:
                    bot.info("Loop stopped by user")
            
            bot_obj.check_dashboard()
            bot.info(f"Final Balance: {bot_obj.balance} coins")
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            print(f"\n{C['yellow']}Exiting...{C['reset']}")
            break

if __name__ == "__main__":
    main()
