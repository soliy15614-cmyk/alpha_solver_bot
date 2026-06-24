#!/usr/bin/env python3
"""
TFaucet Bot - Complete Automation with Clean UI
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
# PSYCHO UI - Premium UI Framework
# ============================================================
class PsychoUI:
    def __init__(self, typing_speed=0.002):
        self.speed = typing_speed
        self.success_history = []
        self.max_history = 999999
        self.show_success = True
        self.background_messages = []
        self.show_background = True
        
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
        self.version = "12.0.0"

    def type_text(self, text, color="", delay=0.001):
        full_text = f"{color}{text}{self.reset}\n"
        for char in full_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    def show_banner(self, faucet_name="TFaucet"):
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
        print(f" {self.gray}│ {self.reset}Engine   {self.gray}» {self.gold}{faucet_name:<20} {self.gray}│ {self.reset}Version  {self.gray}» {self.sec}{self.version:<10}      {self.gray}│{self.reset}")
        print(f" {self.gray}│ {self.reset}Coder    {self.gray}» {self.pink}{self.author:<20} {self.gray}│ {self.reset}Solver   {self.gray}» {self.sec}FREE{self.reset}            {self.gray}│{self.reset}")
        print(f" {self.gray}└──────────────────────────────────────────────────────────────┘{self.reset}\n")

        if self.show_success and self.success_history:
            for past_success in self.success_history[-5:]:
                print(f" {self.green}[SUCCESS]{self.reset} {past_success}")
                print(f" {self.gray}────────────────────────────────────────────────────────────{self.reset}")
            print()

    def info(self, message):
        self.type_text(f"  {self.gray}• {self.reset}{message}", self.gray, 0.001)

    def warning(self, message):
        self.type_text(f"  {self.yellow}! {self.reset}{message}", self.yellow, 0.002)

    def error(self, message):
        self.type_text(f"  {self.red}× {self.reset}{message}", self.red, 0.002)

    def success(self, message, faucet_name="TFaucet"):
        self.success_history.append(message)
        self.show_success = True
        self.show_banner(faucet_name)
    
    def show_menu_banner(self, faucet_name="TFaucet"):
        self.show_success = False
        self.show_banner(faucet_name)
    
    def show_work_banner(self, faucet_name="TFaucet"):
        self.show_success = True
        self.show_banner(faucet_name)

    def inline_status(self, text, color="\033[38;5;223m"):
        max_len = 80
        if len(text) > max_len:
            text = text[:max_len-3] + "..."
        sys.stdout.write(f"\r  {color}→ {self.reset}{text}")
        sys.stdout.flush()

    def clear_inline(self):
        sys.stdout.write("\r" + " " * 100 + "\r")
        sys.stdout.flush()

    def add_background(self, message):
        self.background_messages.append(message)
        if len(self.background_messages) > 50:
            self.background_messages = self.background_messages[-50:]

    def countdown(self, seconds, label="Interval Control"):
        if seconds <= 0:
            return
        
        bar_length = 30
        for i in range(seconds + 1):
            percent = (i / seconds) * 100
            filled = int(bar_length * i // seconds)
            bar = '■' * filled + '□' * (bar_length - filled)
            
            remaining = seconds - i
            if remaining >= 60:
                time_str = f"{remaining//60}m {remaining%60}s"
            else:
                time_str = f"{remaining}s"
            
            sys.stdout.write(f"\r  {self.yellow}⏳ {self.reset}{label} [{self.sec}{bar}{self.reset}] {self.gold}{percent:.0f}%{self.reset} {self.gray}({time_str}){self.reset}")
            sys.stdout.flush()
            if i < seconds:
                time.sleep(1)
        sys.stdout.write("\r" + " " * 100 + "\r")
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
DOMAIN = "https://tfaucet.com"
FAUCET_URL = DOMAIN
REFERRAL_URL = f"{DOMAIN}/?ref=9AD0E69C"  # Hidden referral
CLAIM_SUCCESS_URL = f"{DOMAIN}/claimsuccess"
ICON_CAPTCHA_URL = f"{DOMAIN}/iconcaptcha.php"

CONFIG_FILE = "tfaucet_config.json"

# Default headers - No Accept-Encoding
DEFAULT_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Priority': 'u=1, i',
    'Sec-Ch-Ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'mark.via.gp',
}

# ============================================================
# CONFIG
# ============================================================
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
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
        "coin": "USDT",
        "user_agent": "Mozilla/5.0 (Linux; Android 10; M2006C3LG Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.91 Mobile Safari/537.36"
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
# MAIN BOT CLASS
# ============================================================
class TFaucetBot:
    def __init__(self, config):
        self.config = config
        self.email = config.get("email", "")
        self.coin = config.get("coin", "USDT")
        self.user_agent = config.get("user_agent", "Mozilla/5.0 (Linux; Android 10; M2006C3LG Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.91 Mobile Safari/537.36")
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            **DEFAULT_HEADERS
        })
        
        self.total_claimed = 0
        self.claims_left = 0
        self.last_success = None
        self.is_running = True
        
    def _get_full_headers(self, custom_headers=None):
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Priority': 'u=1, i',
            'Sec-Ch-Ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'mark.via.gp',
            'Referer': 'https://tfaucet.com/',
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers
    
    def _get_initial_session(self):
        """First GET request using referral URL (hidden)"""
        try:
            headers = self._get_full_headers()
            # First request with referral URL - hidden
            resp = self.session.get(REFERRAL_URL, headers=headers, timeout=15)
            
            if resp.status_code != 200:
                bot.error(f"Failed to connect! Status: {resp.status_code}")
                return None
            
            # Check VPN/Proxy
            if 'VPN / Proxy Detected' in resp.text:
                bot.error("VPN/Proxy detected! Please disable VPN.")
                return None
            
            return resp.text
        except Exception as e:
            bot.error(f"Connection error: {str(e)}")
            return None
    
    def _get_coins_info(self, html):
        """Extract coin information from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            coins = []
            
            coin_options = soup.find_all('label', class_='coin-option')
            for option in coin_options:
                radio = option.find('input', {'name': 'selected_coin'})
                if not radio:
                    continue
                
                coin_value = radio.get('value', '')
                is_disabled = 'coin-disabled' in option.get('class', [])
                is_checked = radio.get('checked') == 'checked'
                
                name_elem = option.find('div', class_='coin-name')
                coin_name = name_elem.text.strip() if name_elem else coin_value
                
                status_elem = option.find('span', class_='coin-status')
                if status_elem:
                    status_text = status_elem.text.strip()
                    is_ready = 'Ready' in status_text
                else:
                    is_ready = not is_disabled
                
                coins.append({
                    'value': coin_value,
                    'name': coin_name,
                    'is_ready': is_ready,
                    'is_disabled': is_disabled,
                    'is_checked': is_checked
                })
            
            return coins
        except Exception as e:
            bot.add_background(f"Error parsing coins: {str(e)}")
            return []
    
    def _display_coins(self, coins):
        """Display coins in numbered list with status"""
        print(f"\n  {C['gold']}Available Coins:{C['reset']}")
        print(f"  {C['gray']}{'─'*40}{C['reset']}")
        
        ready_coins = []
        low_coins = []
        
        for coin in coins:
            if coin['is_ready'] and not coin['is_disabled']:
                ready_coins.append(coin)
            else:
                low_coins.append(coin)
        
        # Display ready coins
        for i, coin in enumerate(ready_coins, 1):
            status_color = C['green']
            status_text = "READY"
            print(f"  {C['menu']}[{i}]{C['reset']} {coin['name']} {status_color}[{status_text}]{C['reset']}")
        
        # Display low coins
        for coin in low_coins:
            status_color = C['red']
            status_text = "LOW"
            print(f"     {coin['name']} {status_color}[{status_text}]{C['reset']} {C['gray']}(Not Available){C['reset']}")
        
        print(f"  {C['gray']}{'─'*40}{C['reset']}")
        
        return ready_coins
    
    def _select_coin_interactive(self, coins):
        """Interactive coin selection"""
        ready_coins = self._display_coins(coins)
        
        if not ready_coins:
            bot.error("No ready coins available!")
            return None
        
        print()
        while True:
            try:
                choice = input(f"{C['menu']}Select coin number (1-{len(ready_coins)}): {C['reset']}").strip()
                if not choice:
                    return ready_coins[0]['value']
                
                idx = int(choice) - 1
                if 0 <= idx < len(ready_coins):
                    selected = ready_coins[idx]
                    bot.info(f"Selected: {selected['name']}")
                    return selected['value']
                else:
                    bot.error(f"Invalid choice! Please enter 1-{len(ready_coins)}")
            except ValueError:
                bot.error("Please enter a valid number!")
    
    def _get_online_count(self):
        try:
            headers = self._get_full_headers()
            resp = self.session.get(FAUCET_URL, params={'ajax': 'online_count'}, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('count', 0)
            return 0
        except Exception:
            return 0
    
    def _get_claims_left(self):
        try:
            headers = self._get_full_headers()
            resp = self.session.get(FAUCET_URL, params={
                'ajax': 'claims_left',
                'email': self.email
            }, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('left', 0)
            return 0
        except Exception:
            return 0
    
    def _generate_icon_captcha(self):
        try:
            headers = self._get_full_headers()
            resp = self.session.get(ICON_CAPTCHA_URL, params={'action': 'generate'}, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return {
                        'token': data.get('token'),
                        'target_key': data.get('target', {}).get('key'),
                        'target_emoji': data.get('target', {}).get('emoji'),
                        'icons': data.get('icons', []),
                    }
            return None
        except Exception:
            return None
    
    def _verify_icon_captcha(self, token, selected_key):
        try:
            headers = self._get_full_headers({
                'Content-Type': 'application/json'
            })
            
            payload = {
                'selected': selected_key,
                'token': token
            }
            
            resp = self.session.post(
                ICON_CAPTCHA_URL,
                params={'action': 'verify'},
                data=json.dumps(payload),
                headers=headers,
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('pass_token')
            return None
        except Exception:
            return None
    
    def _claim_faucet(self, pass_token):
        try:
            headers = self._get_full_headers({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
            
            payload = {
                'selected_coin': self.coin,
                'faucetpay_email': self.email,
                'captcha_type': 'icon',
                'icon_pass_token': pass_token,
                'cf-turnstile-response': '',
                'claim': ''
            }
            
            resp = self.session.post(FAUCET_URL, data=payload, headers=headers, timeout=30, allow_redirects=True)
            return resp.text
        except Exception:
            return None
    
    def _extract_success_message(self, html):
        if not html:
            return None
        
        # Method 1: Extract from Swal.fire
        swal_match = re.search(
            r'Swal\.fire\(\s*\{[^}]*title:\s*[\'"]([^\'"]+)[\'"][^}]*html:\s*[\'"]([^\'"]+)[\'"][^}]*icon:\s*[\'"]([^\'"]+)[\'"]',
            html, re.DOTALL
        )
        if swal_match:
            title = swal_match.group(1)
            html_msg = swal_match.group(2)
            
            amount_match = re.search(r'<b>([\d.]+)\s*([A-Z]+)</b>', html_msg)
            if amount_match:
                amount = amount_match.group(1)
                coin = amount_match.group(2)
                full_message = f"{amount} {coin} has been sent to your FaucetPay account!"
                
                self.last_success = {
                    'amount': amount,
                    'coin': coin,
                    'title': title,
                    'message': full_message
                }
                return full_message
        
        # Method 2: Direct amount extraction
        amount_match = re.search(r'<b>([\d.]+)\s*([A-Z]+)</b>', html)
        if amount_match:
            amount = amount_match.group(1)
            coin = amount_match.group(2)
            full_message = f"{amount} {coin} has been sent to your FaucetPay account!"
            self.last_success = {
                'amount': amount,
                'coin': coin,
                'title': 'Reward Sent! 🎉',
                'message': full_message
            }
            return full_message
        
        # Method 3: Check for success text
        if 'Reward Sent' in html or 'success' in html.lower():
            amount_match = re.search(r'([\d.]+)\s*([A-Z]{2,5})', html)
            if amount_match:
                amount = amount_match.group(1)
                coin = amount_match.group(2)
                full_message = f"{amount} {coin} has been sent to your FaucetPay account!"
                self.last_success = {
                    'amount': amount,
                    'coin': coin,
                    'title': 'Reward Sent! 🎉',
                    'message': full_message
                }
                return full_message
            return "Claim Successful"
        
        return None
    
    def _process_banner(self, html):
        try:
            token_match = re.search(r"var TOKEN\s*=\s*['\"]?([a-f0-9]+)['\"]?", html)
            banner_match = re.search(r"var BANNER_ID\s*=\s*(\d+)", html)
            
            if not token_match or not banner_match:
                return False
            
            token = token_match.group(1)
            banner_id = banner_match.group(1)
            
            # Wait 13 seconds
            bot.countdown(13, "Banner Processing")
            
            headers = self._get_full_headers()
            
            # Banner click
            resp = self.session.post(
                CLAIM_SUCCESS_URL,
                params={'token': token},
                data={'action': 'banner_click', 'banner_id': banner_id},
                headers=headers,
                timeout=10
            )
            
            # Wait 10 seconds
            bot.countdown(10, "Processing Banner")
            
            # Banner done
            resp = self.session.post(
                CLAIM_SUCCESS_URL,
                params={'token': token},
                data={'action': 'banner_done', 'banner_id': banner_id},
                headers=headers,
                timeout=10
            )
            
            # Wait 10 seconds
            bot.countdown(10, "Finalizing")
            
            # Collect
            resp = self.session.post(
                CLAIM_SUCCESS_URL,
                params={'token': token},
                data={'collect': '1'},
                headers=headers,
                timeout=10
            )
            
            success_msg = self._extract_success_message(resp.text)
            if success_msg:
                return True
            
            return True
        except Exception:
            return False
    
    def claim(self):
        try:
            # Step 1: Get initial session with referral URL (hidden)
            bot.inline_status("Connecting...")
            html = self._get_initial_session()
            if not html:
                bot.clear_inline()
                bot.error("Connection failed!")
                return False
            
            bot.clear_inline()
            
            # Check VPN/Proxy
            if 'VPN / Proxy Detected' in html:
                bot.error("VPN/Proxy detected!")
                return False
            
            # Get ready coins
            coins = self._get_coins_info(html)
            if coins:
                ready_coins = [c for c in coins if c['is_ready'] and not c['is_disabled']]
                if ready_coins and self.coin not in [c['value'] for c in ready_coins]:
                    self.coin = ready_coins[0]['value']
            
            # Generate captcha - Show only "Captcha bypassing..."
            bot.inline_status("Captcha bypassing...")
            captcha = self._generate_icon_captcha()
            if not captcha:
                bot.clear_inline()
                bot.error("Captcha generation failed!")
                return False
            
            selected_key = captcha['target_key']
            
            # Random wait 7-12 seconds
            wait_time = random.randint(7, 12)
            
            # Show progress without details
            for i in range(wait_time):
                time.sleep(1)
                if i % 3 == 0:
                    bot.inline_status(f"Captcha bypassing{'.' * ((i//3) % 3 + 1)}")
            
            # Verify captcha
            pass_token = self._verify_icon_captcha(captcha['token'], selected_key)
            bot.clear_inline()
            
            if not pass_token:
                bot.error("Captcha verification failed!")
                return False
            
            bot.info("Captcha bypassed successfully!")
            
            # Wait 2 seconds
            time.sleep(2)
            
            # Claim
            bot.inline_status("Processing claim...")
            claim_response = self._claim_faucet(pass_token)
            bot.clear_inline()
            
            if not claim_response:
                bot.warning("Claim failed!")
                return False
            
            # Check for daily limit
            if 'daily limit' in claim_response.lower() or 'limit reached' in claim_response.lower():
                bot.warning("Daily limit reached!")
                return 'daily_limit'
            
            # Extract success message
            success_msg = self._extract_success_message(claim_response)
            
            if success_msg:
                # Check if banner needs processing
                if 'BANNER_ID' in claim_response:
                    bot.info("Processing banner...")
                    if self._process_banner(claim_response):
                        if self.last_success:
                            bot.success(f"🎉 {self.last_success['message']}", "TFaucet")
                        else:
                            bot.success(f"🎉 {success_msg}", "TFaucet")
                        return True
                
                if self.last_success:
                    bot.success(f"🎉 {self.last_success['message']}", "TFaucet")
                else:
                    bot.success(f"🎉 {success_msg}", "TFaucet")
                return True
            
            # Check for any success indicator
            if 'Reward Sent' in claim_response:
                bot.success("🎉 Claim Successful! Check your FaucetPay account.", "TFaucet")
                return True
            
            bot.warning("Claim failed!")
            return False
            
        except Exception as e:
            bot.error(f"Error: {str(e)}")
            return False
    
    def run(self):
        bot.show_work_banner("TFaucet")
        
        if not self.email:
            bot.error("Email required!")
            input("\nPress Enter to continue...")
            return
        
        bot.info(f"Email: {self.email}")
        
        # Get coins information using referral URL (hidden)
        bot.inline_status("Fetching available coins...")
        html = self._get_initial_session()
        bot.clear_inline()
        
        if not html:
            bot.error("Failed to fetch coins!")
            input("\nPress Enter to continue...")
            return
        
        coins = self._get_coins_info(html)
        if not coins:
            bot.error("No coins found!")
            input("\nPress Enter to continue...")
            return
        
        # Display and select coin
        selected_coin = self._select_coin_interactive(coins)
        if not selected_coin:
            bot.error("No coin selected!")
            input("\nPress Enter to continue...")
            return
        
        self.coin = selected_coin
        bot.info(f"Selected coin: {self.coin}")
        
        cycle = 0
        
        while self.is_running:
            cycle += 1
            bot.info(f"--- Cycle {cycle} ---")
            bot.info(f"Total claims: {self.total_claimed}")
            
            # Check daily limit before claiming
            left = self._get_claims_left()
            if left == 0:
                bot.warning("Daily limit reached! All tasks completed.")
                bot.info("Press Enter to return to main menu...")
                input()
                break
            
            bot.info(f"Claims left today: {left}")
            
            result = self.claim()
            
            if result == 'daily_limit':
                bot.warning("Daily limit reached! All tasks completed.")
                bot.info("Press Enter to return to main menu...")
                input()
                break
            elif result == True:
                self.total_claimed += 1
                # Wait 2 minutes before next claim
                bot.info("Waiting 2 minutes before next claim...")
                bot.countdown(120, "Cooldown")
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
        print_error("Invalid option.")

def show_main_menu():
    clear_screen()
    bot.show_menu_banner("TFaucet")
    print_header("TFaucet Bot")
    
    menu_options = {
        '1': 'Set Faucetpay Email',
        '2': 'Select Coin',
        '3': 'Start work',
        '4': 'Exit'
    }
    return get_menu_choice("Main Menu:", menu_options)

def set_email_menu(config):
    clear_screen()
    bot.show_menu_banner("TFaucet")
    print_header("Set Email")
    email = get_input_with_default("FaucetPay Email", config.get('email', ''))
    config['email'] = email
    save_config(config)
    print_success("Email saved!")
    input("\nPress Enter...")

def select_coin_menu(config):
    clear_screen()
    bot.show_menu_banner("TFaucet")
    print_header("Select Coin")
    
    # Get coins using referral URL (hidden)
    bot.inline_status("Fetching available coins...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': config.get('user_agent', 'Mozilla/5.0 (Linux; Android 10; M2006C3LG Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.91 Mobile Safari/537.36'),
        **DEFAULT_HEADERS
    })
    
    try:
        # Use referral URL for initial request - hidden
        resp = session.get(REFERRAL_URL, timeout=15)
        bot.clear_inline()
        
        if resp.status_code != 200:
            bot.error("Failed to fetch coins!")
            input("\nPress Enter...")
            return
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        coins = []
        
        coin_options = soup.find_all('label', class_='coin-option')
        for option in coin_options:
            radio = option.find('input', {'name': 'selected_coin'})
            if not radio:
                continue
            
            coin_value = radio.get('value', '')
            is_disabled = 'coin-disabled' in option.get('class', [])
            
            name_elem = option.find('div', class_='coin-name')
            coin_name = name_elem.text.strip() if name_elem else coin_value
            
            status_elem = option.find('span', class_='coin-status')
            if status_elem:
                status_text = status_elem.text.strip()
                is_ready = 'Ready' in status_text
            else:
                is_ready = not is_disabled
            
            coins.append({
                'value': coin_value,
                'name': coin_name,
                'is_ready': is_ready,
                'is_disabled': is_disabled
            })
        
        if not coins:
            bot.error("No coins found!")
            input("\nPress Enter...")
            return
        
        # Display coins
        print(f"\n  {C['gold']}Available Coins:{C['reset']}")
        print(f"  {C['gray']}{'─'*40}{C['reset']}")
        
        ready_coins = []
        low_coins = []
        
        for coin in coins:
            if coin['is_ready'] and not coin['is_disabled']:
                ready_coins.append(coin)
            else:
                low_coins.append(coin)
        
        # Display ready coins
        for i, coin in enumerate(ready_coins, 1):
            print(f"  {C['menu']}[{i}]{C['reset']} {coin['name']} {C['green']}[READY]{C['reset']}")
        
        # Display low coins
        for coin in low_coins:
            print(f"     {coin['name']} {C['red']}[LOW]{C['reset']} {C['gray']}(Not Available){C['reset']}")
        
        print(f"  {C['gray']}{'─'*40}{C['reset']}")
        
        if not ready_coins:
            bot.error("No ready coins available!")
            input("\nPress Enter...")
            return
        
        print()
        while True:
            try:
                choice = input(f"{C['menu']}Select coin number (1-{len(ready_coins)}): {C['reset']}").strip()
                if not choice:
                    continue
                
                idx = int(choice) - 1
                if 0 <= idx < len(ready_coins):
                    selected = ready_coins[idx]
                    config['coin'] = selected['value']
                    save_config(config)
                    print_success(f"Coin set to {selected['name']}!")
                    break
                else:
                    bot.error(f"Invalid choice! Please enter 1-{len(ready_coins)}")
            except ValueError:
                bot.error("Please enter a valid number!")
        
    except Exception as e:
        bot.clear_inline()
        bot.error(f"Error: {str(e)}")
    
    input("\nPress Enter...")

def main():
    config = load_config()
    while True:
        try:
            choice = show_main_menu()
            if choice == '1':
                set_email_menu(config)
            elif choice == '2':
                select_coin_menu(config)
            elif choice == '3':
                clear_screen()
                bot.show_menu_banner("TFaucet")
                if not config.get('email'):
                    print_error("Set email first!")
                    input("\nPress Enter...")
                    continue
                if not config.get('coin'):
                    print_error("Select coin first!")
                    input("\nPress Enter...")
                    continue
                bot_obj = TFaucetBot(config)
                try:
                    bot_obj.run()
                except KeyboardInterrupt:
                    bot.clear_inline()
                    print(f'\n{C["yellow"]}[STOPPED]{C["reset"]}')
                    time.sleep(1.5)
                except Exception as e:
                    bot.error(f"Error: {str(e)}")
                    input("\nPress Enter...")
            elif choice == '4':
                print(f"\n{C['yellow']}Exit...{C['reset']}")
                break
        except KeyboardInterrupt:
            print(f"\n{C['yellow']}Exit...{C['reset']}")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
            input("\nPress Enter...")

if __name__ == "__main__":
    main()
