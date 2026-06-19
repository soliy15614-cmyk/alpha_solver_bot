#!/usr/bin/env python3
import requests
import re
import json
import time
import random
import sys
import os
import subprocess
import base64
from bs4 import BeautifulSoup

from psycho_ui import PsychoUI
bot = PsychoUI(typing_speed=0.002)

COINS = [
    {"name": "LTC",  "url": "https://earncryptowrs.in/faucet/currency/ltc"},
    {"name": "ETH",  "url": "https://earncryptowrs.in/faucet/currency/eth"},
    {"name": "BNB",  "url": "https://earncryptowrs.in/faucet/currency/bnb"},
    {"name": "SOL",  "url": "https://earncryptowrs.in/faucet/currency/sol"},
    {"name": "TRX",  "url": "https://earncryptowrs.in/faucet/currency/trx"},
    {"name": "USDT", "url": "https://earncryptowrs.in/faucet/currency/usdt"},
    {"name": "ZEC",  "url": "https://earncryptowrs.in/faucet/currency/zec"},
    {"name": "DOGE", "url": "https://earncryptowrs.in/faucet/currency/doge"},
    {"name": "DGB",  "url": "https://earncryptowrs.in/faucet/currency/dgb"},
    {"name": "DASH", "url": "https://earncryptowrs.in/faucet/currency/dash"},
    {"name": "FEY",  "url": "https://earncryptowrs.in/faucet/currency/fey"},
]

SESSION_FILE = "earnwrs_session.json"
CONFIG_FILE = "earnwrs_config.json"

def save_session_data(user_agent, cookies_dict):
    data = {"user_agent": user_agent, "cookies": cookies_dict, "saved_at": time.time()}
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def load_session_data():
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
    return {"wallet_email": "", "api_key": "", "api_provider": ""}

def extract_swal_message(html):
    swal_pattern = r"Swal\.fire\(\s*\{[^}]*icon:\s*'(\w+)'[^}]*html:\s*'([^']+)'[^}]*\}\)"
    match = re.search(swal_pattern, html, re.DOTALL)
    if match:
        return {"icon": match.group(1), "message": match.group(2).strip()}
    
    html_pattern = r"html:\s*'([^']+)'"
    match = re.search(html_pattern, html, re.DOTALL)
    if match:
        message = match.group(1).strip()
        icon_match = re.search(r"icon:\s*'(\w+)'", html)
        return {"icon": icon_match.group(1) if icon_match else "info", "message": message}
    return None

def run_cloudflare_bypass(session, verify_url):
    if not os.path.exists('tes.py'):
        return False
    try:
        bot.inline_status("Cloudflare defense triggered. Bypassing clear-tokens...")
        process = subprocess.Popen(
            ["python3", "tes.py", verify_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, _ = process.communicate(timeout=60)
        data = json.loads(stdout.strip())
        user_agent = data.get("user_agent")
        cf_value = data.get("cf_clearance")
        
        if not cf_value or not user_agent:
            bot.clear_inline()
            return False
        
        cf_token = str(cf_value).split('=')[1] if '=' in str(cf_value) else str(cf_value)
        session.headers.update({'User-Agent': user_agent})
        session.cookies.set("cf_clearance", cf_token, domain="earncryptowrs.in")
        save_session_data(user_agent, session.cookies.get_dict())
        bot.clear_inline()
        return True
    except:
        bot.clear_inline()
        return False

def solve_antibot(html, api_key):
    soup = BeautifulSoup(html, 'html.parser')
    alert = soup.find('p', class_='alert-warning')
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
    
    matches = re.findall(r'rel="(\d+)".*?src="data:image/png;base64,([^"]+)"', script.string)
    if not matches:
        matches = re.findall(r'rel=\\"(\d+)\\".*?src=\\"data:image/png;base64,([^\\\"]+)\\"', script.string)
        if not matches:
            return None
    
    options = {}
    rel_mapping = {}
    for index, (rel, base64_str) in enumerate(matches, start=1):
        options[str(index)] = base64_str
        rel_mapping[str(index)] = rel

    api_url = "https://bypassallshortlinks.space/api.php"
    api_payload = {
        'api_key': api_key,
        'action': 'antibot',
        'main': main_base64,
        'options': options
    }
    
    try:
        api_res = requests.post(api_url, json=api_payload, timeout=20)
        task_resp = api_res.text.strip()
        
        if "id" in task_resp or task_resp.isdigit():
            task_id = task_resp.replace("OK", "").replace("id", "").replace("=", "").strip()
            poll_url = f"https://bypassallshortlinks.space/res.php?id={task_id}&key={api_key}"
            
            for _ in range(15):
                time.sleep(3)
                get_res = requests.get(poll_url, timeout=10)
                order_string = get_res.text.strip()
                if order_string and "NOTREADY" not in order_string:
                    order_indices = order_string.split(',')
                    return " " + " ".join([
                        rel_mapping[idx.strip()]
                        for idx in order_indices
                        if idx.strip() in rel_mapping
                    ])
        else:
            if ',' in task_resp:
                return " " + " ".join([
                    rel_mapping[idx.strip()]
                    for idx in task_resp.split(',')
                    if idx.strip() in rel_mapping
                ])
    except:
        pass
    
    return None


class EarnCryptoBot:
    def __init__(self):
        self.base = "https://earncryptowrs.in"
        self.session = requests.Session()
        self.need_bypass = False
        self.verify_url = ""
        
        self.config = load_config()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.wallet_email = self.config.get("wallet_email", "")
        self.api_key = self.config.get("api_key", "")
        self.api_provider = self.config.get("api_provider", "")
        
        saved = load_session_data()
        if saved and saved.get("user_agent"):
            self.user_agent = saved["user_agent"]
            for name, value in saved["cookies"].items():
                self.session.cookies.set(name, value, domain="earncryptowrs.in")
    
    def headers(self, extra=None):
        h = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        if extra:
            h.update(extra)
        return h
    
    def generate_smart_token(self):
        data = {
            'ts': int(time.time() * 1000),
            'cpu': random.choice([4, 8]),
            'mem': random.choice([4, 8]),
            'w': 1920,
            'h': 1080,
            'touch': 0,
            'moves': random.randint(20, 80)
        }
        return base64.b64encode(json.dumps(data).encode()).decode()
    
    def login(self):
        try:
            r = self.session.get(f"{self.base}/dashboard", headers=self.headers(), timeout=15)
            if '<title>Dashboard' in r.text or '/dashboard' in r.url:
                return True
        except:
            pass
        
        bot.info("Authenticating master login portal...")
        try:
            r = self.session.get(f"{self.base}/auth/login", headers=self.headers(), timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            csrf = soup.find('input', {'name': 'csrf_token_name'})
            if not csrf:
                return False
            
            payload = {
                'wallet': self.wallet_email,
                'csrf_token_name': csrf.get('value'),
                'smart_token': self.generate_smart_token(),
                'captcha': 'smartcaptcha'
            }
            
            time.sleep(random.uniform(2.0, 3.0))
            
            r = self.session.post(
                f"{self.base}/auth/login",
                data=payload,
                headers=self.headers({'Content-Type': 'application/x-www-form-urlencoded'}),
                timeout=15
            )
            
            if '<title>Dashboard' in r.text or '/dashboard' in r.url:
                save_session_data(self.user_agent, self.session.cookies.get_dict())
                return True
            return False
        except:
            return False
    
    def claim_coin(self, coin):
        coin_name = coin["name"]
        faucet_url = coin["url"]
        retry_count = 0
        max_retries = 10
        
        while retry_count < max_retries:
            retry_count += 1
            
            if self.need_bypass:
                run_cloudflare_bypass(self.session, self.verify_url if self.verify_url else faucet_url)
                self.need_bypass = False
                time.sleep(random.uniform(2.0, 3.0))
            
            bot.inline_status(f"[{coin_name}] Fetching remote payload data...")
            try:
                r = self.session.get(faucet_url, headers=self.headers(), timeout=15)
                if 'Just a moment...' in r.text or r.status_code == 403:
                    self.need_bypass = True
                    time.sleep(2)
                    continue
                html = r.text
            except:
                time.sleep(3)
                continue
            
            time.sleep(random.uniform(2.0, 3.0))
            
            soup = BeautifulSoup(html, 'html.parser')
            form = soup.find('form', {'id': 'fauform'})
            if not form:
                time.sleep(2)
                continue
            
            self.verify_url = form.get('action')
            csrf_input = soup.find('input', {'name': 'csrf_token_name'})
            token_input = soup.find('input', {'name': 'token'})
            if not csrf_input or not token_input:
                time.sleep(2)
                continue
            
            min_match = re.search(r'id="minute">(.*?)<\/span>', html)
            sec_match = re.search(r'id="second">(.*?)<\/span>', html)
            if min_match and sec_match:
                total_wait = (int(min_match.group(1).strip()) * 60) + int(sec_match.group(1).strip())
                if total_wait > 0:
                    bot.clear_inline()
                    bot.warning(f"{coin_name} is currently in cooldown mode.")
                    return "cooldown"
            
            bot.inline_status(f"[{coin_name}] Disarming image-array anti-bot...")
            antibot_solution = solve_antibot(html, self.api_key)
            if not antibot_solution:
                time.sleep(2)
                continue
            
            time.sleep(random.uniform(2.0, 3.0))
            
            bot.inline_status(f"[{coin_name}] Transmitting claim block payload...")
            payload = {
                'antibotlinks': antibot_solution,
                'csrf_token_name': csrf_input.get('value'),
                'token': token_input.get('value'),
                'wallet': self.wallet_email,
                'smart_token': self.generate_smart_token(),
                'captcha': 'smartcaptcha'
            }
            
            try:
                response = self.session.post(
                    self.verify_url,
                    data=payload,
                    headers=self.headers({'Content-Type': 'application/x-www-form-urlencoded'}),
                    timeout=15
                )
                html_res = response.text
            except:
                time.sleep(2)
                continue
            
            if 'Just a moment...' in html_res or response.status_code == 403:
                self.need_bypass = True
                time.sleep(2)
                continue
            
            bot.clear_inline()
            
            swal = extract_swal_message(html_res)
            if swal:
                if swal["icon"] == 'success':
                    bot.success(f"{coin_name} -> {swal['message']}", "EarnCryptoWRS")
                    return "success"
                elif "Invalid Anti-Bot" in swal["message"] or "invalid" in swal["message"].lower():
                    time.sleep(2)
                    continue
                else:
                    bot.error(f"{coin_name} -> {swal['message']}")
                    return "failed"
            
            if 'Success!' in html_res:
                amount_match = re.search(
                    r'(\d+\.\d+)\s*(?:USDT|LTC|ETH|BNB|SOL|TRX|ZEC|DOGE|DGB|DASH|FEY)',
                    html_res.upper()
                )
                msg = f"{coin_name} -> {amount_match.group(0)} sent to FaucetPay!" if amount_match else f"{coin_name} -> Claim success!"
                bot.success(msg, "EarnCryptoWRS")
                return "success"
            
            time.sleep(2)
            continue
        
        bot.clear_inline()
        bot.error(f"{coin_name} execution failed after maximum retries.")
        return "failed"
    
    def show_menu(self):
        while True:
            bot.show_banner("EarnCryptoWRS")
            
            wallet_status = "on" if self.config.get("wallet_email") else "off"
            api_status = "on" if self.config.get("api_key") else "off"
            
            print(f"  [1] Set Account             [{wallet_status}]")
            print(f"  [2] Set API Key             [{api_status}]")
            print(f"  [3] Start Work")
            print(f"  [4] Exit\n")
            
            choice = input("  Select option [1-4]: ").strip()
            
            if choice == "1":
                self.set_account()
            elif choice == "2":
                self.set_api_key()
            elif choice == "3":
                if not self.config.get("wallet_email"):
                    bot.error("Please set your account email first!")
                    time.sleep(2)
                    continue
                if not self.config.get("api_key"):
                    bot.error("Please set your API key first!")
                    time.sleep(2)
                    continue
                return True
            elif choice == "4":
                sys.exit(0)
            else:
                bot.error("Invalid choice!")
                time.sleep(1)
    
    def set_account(self):
        bot.show_banner("EarnCryptoWRS")
        print(f"  Current email: {self.config.get('wallet_email', 'Not set')}")
        print()
        email = input("  Enter wallet email: ").strip()
        if email:
            self.config["wallet_email"] = email
            self.wallet_email = email
            save_config(self.config)
            bot.success("Account email saved!", "EarnCryptoWRS")
        else:
            bot.error("Email cannot be empty!")
        time.sleep(1.5)
    
    def set_api_key(self):
        bot.show_banner("EarnCryptoWRS")
        print(f"  Current provider: {self.config.get('api_provider', 'Not set')}")
        print(f"  Current key: {self.config.get('api_key', 'Not set')[:20]}...")
        print()
        print("  Select API Provider:")
        print("  [1] Bypassallshortlink")
        print()
        choice = input("  Select [1]: ").strip()
        
        if choice == "1":
            self.config["api_provider"] = "bypassallshortlinks"
        else:
            bot.error("Invalid choice!")
            time.sleep(1)
            return
        
        api_key = input("  Enter API Key: ").strip()
        if api_key:
            self.config["api_key"] = api_key
            self.api_key = api_key
            save_config(self.config)
            bot.success("API key saved!", "EarnCryptoWRS")
        else:
            bot.error("API key cannot be empty!")
        time.sleep(1.5)
    
    def run(self):
        if not self.show_menu():
            return
        
        bot.show_banner("EarnCryptoWRS")
        
        if not self.login():
            bot.error("Login verification failed!")
            return
        
        bot.success("Session synchronized successfully.", "EarnCryptoWRS")
        
        while True:
            for coin in COINS:
                self.claim_coin(coin)
                bot.countdown(30)


if __name__ == "__main__":
    bot_engine = EarnCryptoBot()
    try:
        bot_engine.run()
    except KeyboardInterrupt:
        bot.clear_inline()
        print(f'\n\u001b[33;1m[STOPPED] Bot safely terminated by operator.\u001b[0m')
        sys.exit(0)
