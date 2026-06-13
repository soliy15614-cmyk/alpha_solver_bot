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
import bypass  # திருத்தப்பட்ட புதிய டெலிகிராம் பாட் பைபாஸ் கோப்பு

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
            with open(CONFIG_FILE, 'r') as f: return json.load(f)
        except: pass
    return {"user_agent": "", "email": "", "password": ""}

def load_session_data():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f: return json.load(f)
    except: pass
    return None

def human_pause(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

# ============================================================
# CORE SHORTLINK ENGINE
# ============================================================
class ShortlinkBypasser:
    def __init__(self):
        self.base = "https://aruble.net"
        self.session = requests.Session()
        
        config = load_user_config()
        self.user_agent = config.get("user_agent", "")
        
        self.csrf = ""
        self.username = "Loading..."
        self.balance = "0.00"
        
        self.target_types = ["paycut", "fastcut", "sharecut", "justcut", "shrinkearn", "exe.io", "cuty.io"]
        self.last_signal_time = 0
        self.success_logs = []

    def ui_header(self, action_text="Processing"):
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
        print(f"{C}Balance  =>{E} {self.balance} COINS")
        print(f"\n{D}═══════════════════════════════════════════════════════{E}")
        
        for log in self.success_logs[-3:]:
            print(log)
            print(f"{D}═══════════════════════════════════════════════════════{E}")
        
        print(f"{Y}{action_text}{E}")

    def send_body_signal(self, path, referer):
        try:
            current_time = time.time()
            elapsed = int((current_time - self.last_signal_time) * 1000) if self.last_signal_time > 0 else random.randint(5000, 15000)
            self.last_signal_time = current_time

            signal_data = {
                'mouse': str(random.randint(3, 8)), 'keyboard': str(random.randint(0, 2)),
                'scroll': str(random.randint(1, 4)), 'touch': str(random.randint(2, 6)),
                'elapsed': str(elapsed), 'mouse_linear': str(random.randint(0, 2)),
                'direct_clicks': str(random.randint(1, 3)), 'integrity': '', 'path': path
            }
            self.session.post(f"{self.base}/bot-check/signal", data=signal_data, headers={
                'User-Agent': self.user_agent, 'x-requested-with': 'XMLHttpRequest',
                'origin': self.base, 'referer': referer
            }, timeout=10)
        except: pass

    def get_cloudflare_bypass(self):
        self.ui_header("[~] Cloudflare Challenge Detected! Bypassing...")
        try:
            proc = subprocess.Popen(["python3", "tes.py", f"{self.base}/shortlinks"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = proc.communicate()
            data = json.loads(stdout.strip())
            ua = data.get("user_agent")
            cf = data.get("cf_clearance")
            if not ua or not cf: return False

            token = cf["value"] if isinstance(cf, dict) and "value" in cf else (str(cf).split('=')[1] if '=' in str(cf) else str(cf))
            self.user_agent = ua
            self.session.cookies.set("cf_clearance", token, domain="aruble.net")
            return True
        except: return False

    def headers(self, extra=None):
        h = {'User-Agent': self.user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection': 'keep-alive'}
        if extra: h.update(extra)
        return h

    def init_session(self):
        saved = load_session_data()
        if saved and saved.get("user_agent"):
            self.user_agent = saved["user_agent"]
            for name, value in saved["cookies"].items(): self.session.cookies.set(name, value, domain="aruble.net")
            return True
        return False

    def extract_csrf(self, html):
        match = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([a-f0-9]{64})["\']', html, re.I)
        if match:
            self.csrf = match.group(1)
            return True
        return False

    def fetch_user_info(self):
        try:
            r = self.session.get(f"{self.base}/shortlinks", headers=self.headers(), timeout=15)
            if r.status_code == 403:
                if not self.get_cloudflare_bypass(): return False
                r = self.session.get(f"{self.base}/shortlinks", headers=self.headers(), timeout=15)
            
            self.extract_csrf(r.text)
            uname = re.search(r'<span[^>]*class="uname"[^>]*>([^<]+)</span>', r.text, re.I)
            if uname: self.username = uname.group(1).strip()
            bal = re.search(r'id="balanceAmount"[^>]*>([^<]+)</div>', r.text, re.I)
            if bal: self.balance = bal.group(1).strip()
            return True
        except: return False

    def get_available_shortlinks(self):
        self.ui_header("[~] Scanning for available shortlinks...")
        try:
            resp = self.session.get(f"{self.base}/shortlinks", headers=self.headers(), timeout=15)
            html = resp.text
            cards = re.findall(r'<div class="sl-link-card">(.*?)</a>\s*</div>\s*</div>', html, re.DOTALL)
            available = []
            for card in cards:
                title_match = re.search(r'<div class="sl-link-title">([^<]+)</div>', card)
                url_match = re.search(r'href="(/shortlinks/go/[^"]+)"', card)
                views_match = re.search(r'<div class="sl-link-views">(\d+)/(\d+)</div>', card)

                if title_match and url_match:
                    title = title_match.group(1).lower()
                    url = f"{self.base}{url_match.group(1)}"
                    if views_match and int(views_match.group(1)) >= int(views_match.group(2)): continue
                    
                    if any(t in title for t in self.target_types) or "tpi.li" in title:
                        available.append({"title": title, "url": url})
            return available
        except: return []

    def call_telegram_bypass(self, target_url):
        self.ui_header("🔄 Processing URL Bypass Routine...")
        try:
            bypassed = bypass.bypass_url_sync(target_url)
            
            # பாட் பிழை செய்தி அல்லது விளம்பரம் அனுப்பினால் இந்த லிங்க் தவிர்க்கப்படும்
            if bypassed == "SKIP_LINK" or not bypassed:
                print(f"\n{R}[!] Skipping this shortlink due to Bot Interruption/Ads.{E}")
                human_pause(2, 3)
                return "SKIP"

            service_name = "shortlink"
            for t in self.target_types:
                if t in target_url.lower():
                    service_name = t
                    break
            if "tpi.li" in target_url.lower(): service_name = "shrinkearn (tpi.li)"

            print(f"\n{G}✅ Bypassed!{E}")
            print(f"{C}🔗 Service:{E} {service_name}")
            print(f"{C}🎯 Destination:{E} {bypassed}")
            print(f"{C}📉 Charged:{E} 3 Tokens\n")
            human_pause(3, 5)
            return bypassed
        except:
            return None

    def process_shortlink(self, target):
        self.ui_header(f"[~] Requesting Shortlink: {target['title'].upper()}")
        try:
            resp = self.session.get(target['url'], headers=self.headers(), allow_redirects=True, timeout=20)
            actual_url = resp.url
            
            for r in resp.history:
                url_lower = r.url.lower()
                if (any(t in url_lower for t in self.target_types) or "tpi.li" in url_lower) and "aruble.net" not in url_lower:
                    actual_url = r.url
                    break

            bypassed_url = self.call_telegram_bypass(actual_url)
            if bypassed_url == "SKIP" or not bypassed_url: 
                return False  # லூப்பிற்கு 'False' அனுப்பி அடுத்த லிங்கிற்குத் தாவச் சொல்கிறது

            # Human Simulation Reading Delay
            for i in range(25, 0, -1):
                if i % 5 == 0: self.send_body_signal('/shortlinks', self.base)
                sys.stdout.write(f"\r{D}[Human Behavior] Reading content... {i}s remaining{E}")
                sys.stdout.flush()
                time.sleep(1)
            print()

            h_param = bypassed_url.split('h=')[-1] if 'h=' in bypassed_url else None
            if not h_param: return False

            verify_resp = self.session.get(f"{self.base}/shortlinks/verify", params={'h': h_param}, headers=self.headers(), timeout=15)
            verify_html = verify_resp.text
            self.send_body_signal('/shortlinks/verify', bypassed_url)

            link_token = re.search(r"linkToken:\s*'([^']+)'", verify_html)
            csrf_token = re.search(r"csrfToken:\s*'([^']+)'", verify_html)
            hp_name = re.search(r"hpName:\s*'([^']+)'", verify_html)
            if not link_token or not csrf_token: return False

            # Captcha Challenge via solver.py
            self.ui_header("[Solver] Fetching verification captcha...")
            cap_resp = self.session.get(f"{self.base}/captcha/challenge", headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'referer': bypassed_url}), timeout=10)
            solved_payload = sync_solve_captcha(cap_resp.json())
            if not solved_payload: return False

            v_resp = self.session.post(f"{self.base}/captcha/verify", data=solved_payload, headers=self.headers({'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'referer': bypassed_url}), timeout=10)
            captcha_token = v_resp.json().get('token')
            if not captcha_token: return False

            # Reward Claim
            self.ui_header("[~] Submitting Reward Claim...")
            claim_data = {
                'link_token': link_token.group(1), 'captcha_token': captcha_token,
                '_csrf_token': csrf_token.group(1), hp_name.group(1) if hp_name else 'field_54ac0c8f': ""
            }
            c_resp = self.session.post(f"{self.base}/shortlinks/claim", data=claim_data, headers={
                'User-Agent': self.user_agent, 'x-requested-with': 'XMLHttpRequest', 'origin': self.base, 'referer': bypassed_url
            }, timeout=15)
            
            result = c_resp.json()
            if result.get('success'):
                self.balance = result.get('new_balance', self.balance)
                self.success_logs.append(f"{G}[SUCCESS] Claimed Shortlink! Reward: +{result.get('reward', '0')} COINS{E}")
                return True
            return False
        except: return False

def run_shortlink():
    bot = ShortlinkBypasser()
    if not bot.init_session() or not bot.fetch_user_info():
        print(f"\n{R}[!] Active session missing. Please run Faucet Claim first to log in!{E}")
        time.sleep(2.5)
        return

    links = bot.get_available_shortlinks()
    if not links:
        bot.ui_header(f"{Y}[!] No target shortlinks available at this moment.{E}")
        human_pause(2, 3)
    else:
        for idx, link in enumerate(links, 1):
            bot.ui_header(f"[~] Processing Link {idx}/{len(links)}")
            
            # லிங்க் பாதியிலேயே பிழை அல்லது விளம்பரத்தால் நின்றால், 
            # இது 'False' ஆகி எரர் லாஜிக்குகளைக் கடந்து அடுத்த லிங்கிற்குச் சென்றுவிடும்
            success = bot.process_shortlink(link)
            
            if success:
                for wait in range(random.randint(12, 18), 0, -1):
                    sys.stdout.write(f"\r{Y}[Cooldown] Next target in {wait}s...{E}")
                    sys.stdout.flush()
                    time.sleep(1)
            else:
                # லிங்க் ஸ்கிப் செய்யப்பட்டால் சிறிய இடைவெளிக்குப் பின் அடுத்த லிங்க் தொடங்கும்
                human_pause(2, 3)

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
    print(f"{G}[✓] ALL AVAILABLE SHORTLINKS PROCESSED SUCCESSFULLY!{E}\n")
    input(f"{G}press enter . . .{E}")

if __name__ == "__main__":
    try: run_shortlink()
    except KeyboardInterrupt: sys.exit(0)

