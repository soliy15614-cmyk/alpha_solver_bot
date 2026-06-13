#!/usr/bin/env python3
import requests
import re
import json
import time
import random
import sys
import os
import subprocess
from solver import sync_solve_captcha

# ============================================================
# COLOR SYSTEM
# ============================================================
G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
C = '\033[96m'
D = '\033[90m'
E = '\033[0m'

SESSION_FILE = "arable_session.json"
CONFIG_FILE = "config_data.json"

def load_user_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return {"user_agent": "", "email": "", "password": ""}

def save_session_data(user_agent, cookies_dict):
    data = {"user_agent": user_agent, "cookies": cookies_dict, "saved_at": time.time()}
    try:
        with open(SESSION_FILE, 'w') as f: json.dump(data, f)
        return True
    except: return False

def load_session_data():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f: return json.load(f)
    except: pass
    return None

def human_pause(action='default'):
    delays = {'page': (2.0, 4.5), 'read': (1.5, 3.5), 'think': (2.0, 5.0), 'click': (0.8, 2.5), 'type': (0.3, 0.9)}
    min_d, max_d = delays.get(action, (1.0, 3.0))
    time.sleep(random.uniform(min_d, max_d))

# ============================================================
# CORE FAUCET ENGINE
# ============================================================
class FaucetBot:
    def __init__(self):
        self.base = "https://aruble.net"
        self.session = requests.Session()
        
        # Load configuration data
        config = load_user_config()
        self.user_agent = config.get("user_agent", "")
        self.email = config.get("email", "")
        self.password = config.get("password", "")
        
        self.csrf = ""
        self.captcha_token = ""
        self.username = "Loading..."
        self.balance = "0.00"
        self.claims_done = 0
        self.claims_max = 70
        self.page_time = time.time()
        self.fp = "".join(random.choices("abcdef0123456789", k=64))
        self.success_logs = []

    def ui_header(self, action_text="Running"):
        os.system('cls' if os.name == 'nt' else 'clear')
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
        print(f"{C}User    =>{E} {self.username}")
        print(f"{C}Balance =>{E} {self.balance} ({self.claims_done}/{self.claims_max} Claims)")
        print(f"\n{D}═══════════════════════════════════════════════════════{E}")
        
        for log in self.success_logs[-4:]:
            print(log)
            print(f"{D}═══════════════════════════════════════════════════════{E}")
        
        sys.stdout.write(action_text)
        sys.stdout.flush()

    def get_cloudflare_bypass(self):
        self.ui_header(f"{Y}[~] Security challenge detected. Bypassing Cloudflare...{E}")
        try:
            process = subprocess.Popen(["python3", "tes.py", f"{self.base}/faucet"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            data_bypass = json.loads(stdout.strip())
            
            user_agent = data_bypass.get("user_agent")
            cf_value = data_bypass.get("cf_clearance")
            if not cf_value or not user_agent: return False

            cf_token = cf_value["value"] if isinstance(cf_value, dict) and "value" in cf_value else (str(cf_value).split('=')[1] if '=' in str(cf_value) else str(cf_value))
            self.user_agent = user_agent
            self.session.cookies.set("cf_clearance", cf_token, domain="aruble.net")
            save_session_data(self.user_agent, self.session.cookies.get_dict())
            return True
        except Exception:
            return False

    def headers(self, extra=None):
        h = {'User-Agent': self.user_agent, 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"'}
        if extra: h.update(extra)
        return h

    def signal(self, path='/'):
        try:
            elapsed = int((time.time() - self.page_time) * 1000)
            self.session.post(f"{self.base}/bot-check/signal", data={'mouse': str(random.randint(1, 4)), 'keyboard': str(random.randint(0, 2)), 'scroll': str(random.randint(1, 3)), 'touch': str(random.randint(2, 5)), 'elapsed': str(elapsed), 'mouse_linear': str(random.randint(0, 2)), 'direct_clicks': str(random.randint(1, 3)), 'integrity': '', 'path': path}, headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': f"{self.base}{path}"}), timeout=10)
        except: pass

    def init_session(self):
        """சேமிக்கப்பட்ட குக்கீஸ்களை ஏற்றிப் பயன்படுத்தும் பகுதி"""
        saved = load_session_data()
        if saved and saved.get("user_agent"):
            self.user_agent = saved["user_agent"]
            for name, value in saved["cookies"].items(): 
                self.session.cookies.set(name, value, domain="aruble.net")
            return True
        return False

    def check_and_extract_csrf(self, html_text):
        match = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([a-f0-9]{64})["\']', html_text, re.IGNORECASE)
        if match:
            self.csrf = match.group(1)
            return True
        return False

    def login(self):
        # முதலில் ஏற்கனவே உள்ள குக்கீஸ்களை லோட் செய்கிறது
        self.init_session()
        self.ui_header(f"{Y}[~] Testing connection to Faucet page...{E}")
        self.page_time = time.time()

        # நீங்கள் கேட்ட பிரத்யேக மாற்றம்: முதலில் பேஸ் யூஆர்எல்லிற்கு ரிக்வெஸ்ட் அனுப்பிச் சோதித்தல்
        try:
            test_resp = self.session.get(f"{self.base}/faucet", headers=self.headers(), timeout=12, allow_redirects=True)
            status = test_resp.status_code
        except Exception:
            status = 403

        # ஸ்டேட்டஸ் 200 அல்லது 302 ஆக இருந்தால் பைபாஸ் செய்யாமல் நேரடியாக தொடரும்
        if status in [200, 302]:
            self.ui_header(f"{G}[✓] Connection established successfully (Status {status}){E}")
            r = test_resp
        else:
            # 403 அல்லது வேறு எரர் வந்தால் மட்டுமே கிளவுட்பிளேயர் பைபாஸ் செய்யும்
            if not self.get_cloudflare_bypass(): return False
            try:
                r = self.session.get(f"{self.base}/faucet", headers=self.headers(), timeout=15)
            except Exception: return False

        # ஏற்கனவே லாகின் ஆகியுள்ளதா என்று செக் செய்தல்
        try:
            if self.check_and_extract_csrf(r.text):
                uname = re.search(r'<span[^>]*class="uname"[^>]*>([^<]+)</span>', r.text, re.I)
                if uname:
                    self.username = uname.group(1).strip()
                    bal = re.search(r'id="balanceAmount"[^>]*>([^<]+)</div>', r.text, re.I)
                    if bal: self.balance = bal.group(1).strip()
                    self._fetch_info()
                    # லாகின் வெற்றிகரமாக இருந்தால் தற்போதைய குக்கீஸ்களை அப்டேட் செய்து சேமிக்கும்
                    save_session_data(self.user_agent, self.session.cookies.get_dict())
                    return True
                    
            r_home = self.session.get(self.base, headers=self.headers(), timeout=15)
            self.check_and_extract_csrf(r_home.text)
        except Exception:
            return False

        human_pause('read')
        self.signal('/')
        human_pause('click')

        # புதிய லாகின் செயல்முறை
        try:
            r = self.session.get(f"{self.base}/captcha/challenge", headers=self.headers({'x-requested-with': 'XMLHttpRequest'}), timeout=10)
            captcha = r.json()
        except: return False

        self.ui_header(f"{Y}[Solver] Solving Login Captcha via Telegram...{E}")
        solved_payload = sync_solve_captcha(captcha)
        if not solved_payload: return False

        try:
            r = self.session.post(f"{self.base}/captcha/verify", data=solved_payload, headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'Content-Type': 'application/x-www-form-urlencoded'}), timeout=10)
            result = r.json()
            if not result.get('success'): return False
            captcha_token = result.get('token')
        except: return False

        try:
            r = self.session.post(f"{self.base}/api/auth/login", data={'_csrf_token': self.csrf, 'email': self.email, 'password': self.password, 'captcha_token': captcha_token, 'remember_me': '1'}, headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'Content-Type': 'application/x-www-form-urlencoded'}), timeout=15)
            res = r.json()
            if res.get('success'):
                # லாகின் முடிந்தவுடன் குக்கீஸ்களைச் சேமித்தல்
                save_session_data(self.user_agent, self.session.cookies.get_dict())
                self._fetch_info()
                return True
            return False
        except Exception: return False

    def _fetch_info(self):
        try:
            r = self.session.get(f"{self.base}/faucet", headers=self.headers(), timeout=15)
            self.check_and_extract_csrf(r.text)
            claims = re.search(r'claimsToday["\']?\s*:\s*(\d+)', r.text)
            if claims: self.claims_done = int(claims.group(1))
            claims_max = re.search(r'claimsMax["\']?\s*:\s*(\d+)', r.text)
            if claims_max: self.claims_max = int(claims_max.group(1))
            bal = re.search(r'id="balanceAmount"[^>]*>([^<]+)</div>', r.text, re.I)
            if bal: self.balance = bal.group(1).strip()
            uname = re.search(r'<span[^>]*class="uname"[^>]*>([^<]+)</span>', r.text, re.I)
            if uname: self.username = uname.group(1).strip()
        except: pass

    def claim(self):
        self.page_time = time.time()
        self.ui_header(f"{Y}[~] Initiating Claim Sequence...{E}")
        
        # கிளைம் செய்யும் முன்பும் நெட்வொர்க் ஸ்டேட்டஸ் செக் செய்தல்
        try:
            r = self.session.get(f"{self.base}/faucet", headers=self.headers(), timeout=15)
            if r.status_code == 403:
                if not self.get_cloudflare_bypass(): return None
                r = self.session.get(f"{self.base}/faucet", headers=self.headers(), timeout=15)

            self.check_and_extract_csrf(r.text)
            cd = re.search(r'globalCooldown\s*:\s*(\d+)', r.text)
            if cd and int(cd.group(1)) > 0:
                return {'next_claim_in': int(cd.group(1))}
        except: return None

        human_pause('read')
        self.signal('/faucet')
        human_pause('click')

        try:
            r = self.session.get(f"{self.base}/captcha/challenge", headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'referer': f"{self.base}/faucet"}), timeout=10)
            captcha = r.json()
        except: return None

        self.ui_header(f"{Y}[Solver] Requesting Telegram background solution for Claim...{E}")
        solved_payload = sync_solve_captcha(captcha)
        if not solved_payload: return None

        try:
            r = self.session.post(f"{self.base}/captcha/verify", data=solved_payload, headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'referer': f"{self.base}/faucet", 'Content-Type': 'application/x-www-form-urlencoded'}), timeout=10)
            res = r.json()
            if not res.get('success'): return None
            self.captcha_token = res.get('token')
        except: return None

        try:
            r = self.session.post(f"{self.base}/faucet/claim", data={'dest': 'account', 'wc_id': '0', 'captcha_token': self.captcha_token, 'fp': self.fp, '_csrf_token': self.csrf}, headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'referer': f"{self.base}/faucet", 'Content-Type': 'application/x-www-form-urlencoded'}), timeout=15)
            result = r.json()
            if result.get('success'):
                self.claims_done = result.get('claims_today', 0)
                self.balance = result.get('balance_after', '0.00')
                
                log_msg = f"{G}[SUCCESS] +{result.get('amount', '5.0')} added to your balance{E}"
                self.success_logs.append(log_msg)
                
                # ஒவ்வொரு வெற்றிகரமான கிளைமிற்குப் பிறகும் குக்கீஸ்களைச் சேமிக்கிறது
                save_session_data(self.user_agent, self.session.cookies.get_dict())
                return result
            return None
        except Exception: return None

    def wait_cooldown(self, seconds):
        total_wait = seconds + random.randint(5, 15)
        for remaining in range(total_wait, 0, -1):
            mins, secs = divmod(remaining, 60)
            timer_format = f"{mins:02d}:{secs:02d}"
            self.ui_header(f"{Y}[WAIT] {timer_format} ☕{E}")
            if remaining % 60 == 0: self.signal('/faucet')
            time.sleep(1)

def run_faucet():
    bot = FaucetBot()
    if not bot.login():
        print(f"\n{R}[!] Authentication failed! Check config values.{E}")
        time.sleep(2)
        return
        
    while True:
        if bot.claims_done >= bot.claims_max:
            print(f"\n{G}[✓] Daily Claim Limit Reached!{E}")
            time.sleep(2)
            break
        result = bot.claim()
        if result:
            if 'next_claim_in' in result:
                bot.wait_cooldown(result['next_claim_in'])
            else:
                bot.wait_cooldown(300)
        else:
            time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    try:
        run_faucet()
    except KeyboardInterrupt:
        sys.exit(0)

