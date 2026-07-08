#!/usr/bin/env python3
import requests
import time
import re
import json
import os
import sys
import subprocess
import tempfile
from datetime import datetime
from colorama import init, Fore, Back, Style
import pyfiglet
from typing import Optional, Dict, Any
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich import box
from rich.columns import Columns
import threading
from telethon.sync import TelegramClient
from telethon import functions, types
import random
import warnings
from bs4 import BeautifulSoup

# Initialize
init(autoreset=True)
warnings.filterwarnings('ignore')
os.environ["PYTHONWARNINGS"] = "ignore"

console = Console()

API_ID = 32744606
API_HASH = 'f58682565ec84dcd4e529a33246f07aa'
SESSION_NAME = 'alpha'

# Line separator
SEP = "[dim]" + "═" * 60 + "[/dim]"

class TypeWriter:
    @staticmethod
    def type_text(text, delay=0.03, style=None):
        for char in text:
            time.sleep(random.uniform(0.01, delay))
            if style:
                console.print(char, end="", style=style)
            else:
                console.print(char, end="")
        console.print()
    
    @staticmethod
    def type_input(prompt, style="cyan"):
        TypeWriter.type_text(prompt, 0.02, style)
        return input().strip()

class FancyProgress:
    @staticmethod
    def show_progress(description, total=100, color="cyan"):
        with Progress(
            SpinnerColumn("dots"),
            TextColumn(f"[{color}]{{task.description}}[/{color}]"),
            BarColumn(bar_width=40, style=color, complete_style=f"bold {color}", finished_style="green"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(f"[{color}]{description}[/{color}]", total=total)
            for i in range(total):
                time.sleep(random.uniform(0.01, 0.03))
                progress.update(task, advance=1)
            progress.update(task, completed=total, description=f"[green]✓ {description} Complete![/green]")
            time.sleep(0.3)

class AlphaSolver:
    @staticmethod
    def setup_session():
        console.clear()
        try:
            banner = pyfiglet.figlet_format("ALPHA", font="slant")
            console.print(Panel(banner, style="bold cyan", border_style="cyan"))
        except:
            console.print(Panel("ALPHA SOLVER", style="bold cyan", border_style="cyan"))
        
        console.print()
        TypeWriter.type_text("Setting up Telegram Session...", 0.03, "bold cyan")
        console.print()
        console.print("[yellow]API_ID:[/yellow] [green]32744606[/green]")
        console.print("[yellow]API_HASH:[/yellow] [green]f58682565ec84dcd4e529a33246f07aa[/green]")
        console.print("[yellow]SESSION:[/yellow] [green]alpha[/green]")
        console.print()
        
        FancyProgress.show_progress("Initializing Alpha Session", 50, "cyan")
        
        try:
            client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
            with client:
                console.print()
                console.print(Panel("[bold green]SUCCESS![/bold green]\n[green]alpha.session created successfully![/green]", border_style="green"))
                me = client.get_me()
                console.print(f"[bold yellow]Logged in as:[/bold yellow] [cyan]{me.first_name}[/cyan]")
                console.print(f"[bold yellow]Phone:[/bold yellow] [cyan]{me.phone if me.phone else 'N/A'}[/cyan]")
                console.print(f"[bold yellow]ID:[/bold yellow] [cyan]{me.id}[/cyan]")
                console.print()
                FancyProgress.show_progress("Testing Connection", 30, "yellow")
                result = client(functions.help.GetNearestDcRequest())
                console.print(f"[bold yellow]Connected to DC:[/bold yellow] [green]{result.nearest_dc}[/green]")
                console.print(f"[bold yellow]Country:[/bold yellow] [green]{result.country}[/green]")
        except Exception as e:
            console.print()
            console.print(Panel(f"[bold red]Error: {str(e)}[/bold red]", border_style="red"))
        
        console.print()
        console.print(SEP)
        console.print("[yellow]PRESS ENTER TO CONTINUE . . .[/yellow]", end="")
        input()

class Config:
    CONFIG_FILE = "psycho_config.json"
    
    def __init__(self):
        self.data = {
            "email": "",
            "password": "",
            "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
        }
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    saved = json.load(f)
                    self.data.update(saved)
        except:
            pass
    
    def save(self):
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass
    
    def get(self, key: str) -> str:
        return self.data.get(key, "")
    
    def set(self, key: str, value: str):
        self.data[key] = value
        self.save()

class IPChecker:
    @staticmethod
    def get_ip_info():
        try:
            if os.path.exists("ip.py"):
                result = subprocess.run([sys.executable, "ip.py", "info"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return json.loads(result.stdout)
            response = requests.get("http://ip-api.com/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {"success": "true", "ip": data.get("query", "Unknown"), "country": data.get("country", "Unknown"), "country_code": data.get("countryCode", "Unknown"), "region": data.get("regionName", "Unknown"), "city": data.get("city", "Unknown"), "isp": data.get("isp", "Unknown")}
        except:
            pass
        return None

    @staticmethod
    def display_ip_info():
        FancyProgress.show_progress("Fetching IP Information", 40, "cyan")
        info = IPChecker.get_ip_info()
        if not info:
            console.print("[red]Failed to fetch IP information[/red]")
            return
        console.print()
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan", title="IP Information")
        table.add_column("Key", style="bold yellow", width=18)
        table.add_column("Value", style="green")
        for key, value in [("IP", info.get('ip')), ("COUNTRY", info.get('country')), ("CITY", info.get('city')), ("ISP", info.get('isp'))]:
            table.add_row(key, value or 'N/A')
        console.print(table)

class ClaimCoinFaucet:
    def __init__(self, config: Config):
        self.base_url = "https://claimcoin.in"
        self.login_url = f"{self.base_url}/login"
        self.faucet_url = f"{self.base_url}/faucet"
        self.verify_url = f"{self.base_url}/faucet/verify"
        self.auth_url = f"{self.base_url}/auth/login"
        self.turnstile_sitekey = "0x4AAAAAAB6ZWSg9eOY7OVRl"
        self.config = config
        self.consecutive_fails = 0
        self.max_fails = 5
        self.claim_count = 0
        self.total_claimed = 0.0
        self.current_user_agent = None
        self.current_cf_clearance = None
        self.main_session = None
    
    def log_step(self, step, message, color="cyan"):
        console.print(f"[{color}][{step}][/{color}] {message}")
    
    def bypass_cloudflare(self, url):
        try:
            from seledroid import webdriver
        except ImportError:
            console.print("[red]Seledroid not installed![/red]")
            return False

        self.log_step("CF", "Launching browser for Cloudflare bypass...", "yellow")
        
        with Progress(SpinnerColumn("dots"), TextColumn("[cyan]{task.description}[/cyan]"), BarColumn(bar_width=30, style="cyan"), TimeElapsedColumn(), console=console, transient=True) as progress:
            task = progress.add_task("[cyan]Bypassing Cloudflare...[/cyan]", total=20)
            
            driver = webdriver.Chrome(gui=True, pip_mode=True)
            driver.get(url)
            
            clearance = None
            
            for i in range(20):
                time.sleep(1)
                progress.update(task, advance=1)
                cookie_obj = driver.get_cookie("cf_clearance")
                if cookie_obj:
                    clearance = cookie_obj["value"] if isinstance(cookie_obj, dict) else str(cookie_obj)
                    if clearance.startswith("cf_clearance="):
                        clearance = clearance.replace("cf_clearance=", "", 1)
                    progress.update(task, completed=20, description="[green]Cloudflare Bypassed![/green]")
                    break
            
            try:
                uagent = driver.user_agent
            except:
                uagent = None
            
            driver.close()
            
            if clearance and uagent:
                self.current_cf_clearance = clearance
                self.current_user_agent = uagent
                console.print(f"[green]cf_clearance: {clearance[:30]}...[/green]")
                return True
            
            console.print("[red]Failed to get cf_clearance![/red]")
            return False
    
    def create_session_with_cookies(self):
        session = requests.Session()
        ua = self.current_user_agent or self.config.get("user_agent")
        session.headers.update({
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        })
        
        if self.current_cf_clearance:
            session.cookies.set("cf_clearance", self.current_cf_clearance, domain=".claimcoin.in")
        
        return session
    
    def solve_turnstile(self, url=None):
        if url is None:
            url = self.login_url
        
        self.log_step("TS", "Solving Turnstile captcha...", "cyan")
        
        try:
            if not os.path.exists("t.py"):
                console.print("[red]t.py not found![/red]")
                return None
            
            # No timeout - unlimited
            result = subprocess.run(['python', 't.py', url, self.turnstile_sitekey], capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                response = json.loads(output)
                if response.get("success") == "true" and response.get("token"):
                    console.print(f"[green]Turnstile solved![/green]")
                    return response["token"]
            
            console.print(f"[red]Turnstile failed![/red]")
            return None
        except Exception as e:
            console.print(f"[red]Turnstile error: {e}[/red]")
            return None
    
    def solve_antibot(self, html_content):
        self.log_step("AB", "Solving Anti-Bot Links...", "cyan")
        
        try:
            if not os.path.exists("anti.py"):
                console.print("[red]anti.py not found![/red]")
                return None
            
            # Use tempfile to create temporary file safely
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"faucet_{int(time.time())}.html")
            
            console.print(f"[dim]Temp file: {temp_file}[/dim]")
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # No timeout - unlimited
            result = subprocess.run(['python', 'anti.py', temp_file], capture_output=True, text=True)
            
            # Clean up
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
            
            if result.returncode == 0:
                output = result.stdout.strip()
                console.print(f"[dim]Anti-Bot output: {output}[/dim]")
                response = json.loads(output)
                if response.get("success") == True or response.get("success") == "true":
                    solution = response.get("solution")
                    console.print(f"[green]Anti-Bot solved: {solution}[/green]")
                    return solution
            
            console.print(f"[red]Anti-Bot failed! stdout: {result.stdout[:200]}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Anti-Bot error: {e}[/red]")
            return None
    
    def extract_csrf_token(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf_token_name'})
        if csrf_input:
            token = csrf_input.get('value')
            console.print(f"[green]CSRF: {token[:20]}...[/green]")
            return token
        console.print("[red]CSRF Token not found![/red]")
        return None
    
    def parse_timer(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        minute_elem = soup.find('b', {'id': 'minute'})
        second_elem = soup.find('b', {'id': 'second'})
        if minute_elem and second_elem:
            try:
                minutes = int(minute_elem.text.strip())
                seconds = int(second_elem.text.strip())
                return (minutes * 60) + seconds
            except:
                pass
        return 0
    
    def login(self):
        console.print()
        console.print(SEP)
        self.log_step("LOGIN", "Starting login process...", "bold magenta")
        console.print(SEP)
        
        self.main_session = self.create_session_with_cookies()
        session = self.main_session
        
        # Get login page
        self.log_step("1", f"GET {self.login_url}", "yellow")
        try:
            response = session.get(self.login_url, timeout=None, allow_redirects=True)
            console.print(f"[dim]Status: {response.status_code} | URL: {response.url}[/dim]")
        except Exception as e:
            console.print(f"[red]Connection failed: {e}[/red]")
            return None
        
        # Cloudflare check
        if response.status_code in [403, 503]:
            self.log_step("1.1", "Cloudflare detected! Bypassing...", "yellow")
            if not self.bypass_cloudflare(self.login_url):
                return None
            self.main_session = self.create_session_with_cookies()
            session = self.main_session
            response = session.get(self.login_url, timeout=None)
            console.print(f"[dim]After bypass - Status: {response.status_code}[/dim]")
        
        # Check if already logged in
        if 'dashboard' in response.url.lower():
            console.print("[green]Already logged in![/green]")
            return session
        
        # Extract CSRF
        self.log_step("2", "Extracting CSRF token...", "cyan")
        csrf_token = self.extract_csrf_token(response.text)
        if not csrf_token:
            return None
        
        # Solve Turnstile
        self.log_step("3", "Solving Turnstile...", "cyan")
        turnstile_token = self.solve_turnstile()
        if not turnstile_token:
            return None
        
        # Login
        self.log_step("4", "Sending login request...", "bold cyan")
        payload = {
            'csrf_token_name': csrf_token,
            'email': self.config.get("email"),
            'password': self.config.get("password"),
            'captcha': 'turnstile',
            'cf-turnstile-response': turnstile_token
        }
        
        console.print(f"[dim]Email: {self.config.get('email')}[/dim]")
        console.print(f"[dim]CSRF: {csrf_token[:20]}...[/dim]")
        
        login_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.base_url,
            "Referer": self.login_url,
        }
        
        try:
            response = session.post(
                self.auth_url, 
                data=payload, 
                headers=login_headers,
                allow_redirects=True, 
                timeout=None
            )
            console.print(f"[dim]Login Status: {response.status_code}[/dim]")
            console.print(f"[dim]Final URL: {response.url}[/dim]")
            
            if 'dashboard' in response.url:
                console.print("[bold green]LOGIN SUCCESSFUL![/bold green]")
                console.print(SEP)
                return session
            elif response.status_code == 200 and 'dashboard' in response.text.lower():
                console.print("[bold green]LOGIN SUCCESSFUL![/bold green]")
                console.print(SEP)
                return session
            else:
                console.print(f"[red]Login failed![/red]")
                if 'Invalid Details' in response.text:
                    console.print("[red]Error: Invalid Details[/red]")
                console.print(SEP)
                return None
        except Exception as e:
            console.print(f"[red]Login error: {e}[/red]")
            return None
    
    def claim_faucet(self):
        if not self.main_session:
            self.log_step("ERR", "No session! Re-logging in...", "yellow")
            if not self.login():
                return False, None
        
        session = self.main_session
        
        # Get faucet page
        console.print(SEP)
        self.log_step("C1", f"GET {self.faucet_url}", "yellow")
        
        faucet_headers = {
            "Referer": self.base_url + "/dashboard",
        }
        
        try:
            response = session.get(self.faucet_url, headers=faucet_headers, timeout=None, allow_redirects=True)
            console.print(f"[dim]Status: {response.status_code} | URL: {response.url}[/dim]")
            
        except Exception as e:
            console.print(f"[red]Faucet page error: {e}[/red]")
            return False, None
        
        # Cloudflare on faucet
        if response.status_code in [403, 503]:
            self.log_step("C1.1", "Cloudflare on faucet! Bypassing...", "yellow")
            if self.bypass_cloudflare(self.faucet_url):
                self.main_session = self.create_session_with_cookies()
                if not self.login():
                    return False, None
                session = self.main_session
                response = session.get(self.faucet_url, timeout=None)
        
        # Check if redirected to login
        if 'login' in response.url.lower():
            self.log_step("EXP", "Session expired! Re-logging in...", "yellow")
            if not self.login():
                return False, None
            session = self.main_session
            response = session.get(self.faucet_url, timeout=None)
            if 'login' in response.url.lower():
                console.print("[red]Still getting login page![/red]")
                return False, None
        
        # Check if on faucet page
        if 'faucet' not in response.url.lower() and 'claim' not in response.text.lower() and 'antibotlinks' not in response.text.lower():
            console.print(f"[red]Not on faucet page! URL: {response.url}[/red]")
            return False, None
        
        # Extract CSRF
        self.log_step("C2", "Extracting CSRF token...", "cyan")
        csrf_token = self.extract_csrf_token(response.text)
        if not csrf_token:
            console.print("[red]Cannot find CSRF token![/red]")
            return False, None
        
        # Check for elements
        has_turnstile = 'cf-turnstile' in response.text
        has_antibot = 'antibotlinks' in response.text.lower()
        console.print(f"[dim]Turnstile: {has_turnstile} | Anti-Bot: {has_antibot}[/dim]")
        
        # Solve Anti-Bot
        self.log_step("C3", "Solving Anti-Bot Links...", "cyan")
        antibot_solution = self.solve_antibot(response.text)
        if not antibot_solution:
            console.print("[red]Anti-Bot solving failed![/red]")
            return False, None
        
        # Prepare payload
        verify_payload = {
            'antibotlinks': antibot_solution,
            'csrf_token_name': csrf_token,
            'captcha': 'turnstile'
        }
        
        if has_turnstile:
            self.log_step("C4", "Solving Turnstile...", "cyan")
            turnstile_token = self.solve_turnstile(self.faucet_url)
            if turnstile_token:
                verify_payload['cf-turnstile-response'] = turnstile_token
        
        # Submit claim
        self.log_step("C5", f"POST {self.verify_url}", "bold cyan")
        console.print(f"[dim]Payload: antibotlinks={antibot_solution}, csrf={csrf_token[:20]}...[/dim]")
        
        verify_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.base_url,
            "Referer": self.faucet_url,
            "X-Requested-With": "XMLHttpRequest"
        }
        
        try:
            verify_response = session.post(
                self.verify_url, 
                data=verify_payload, 
                headers=verify_headers,
                allow_redirects=True, 
                timeout=None
            )
            console.print(f"[dim]Verify Status: {verify_response.status_code}[/dim]")
            
            response_text = verify_response.text
            
            if 'Good job!' in response_text:
                amount_match = re.search(r'([\d.]+)\s*CCP', response_text)
                if amount_match:
                    amount = float(amount_match.group(1))
                    self.total_claimed += amount
                    console.print()
                    console.print(Panel(f"[bold green]+{amount} CCP CLAIMED![/bold green]\n[cyan]Total: {self.total_claimed} CCP[/cyan]", border_style="green", title="SUCCESS"))
                    console.print()
                
                wait_time = self.parse_timer(response_text)
                console.print(SEP)
                return True, wait_time if wait_time > 0 else 300
            
            elif 'Invalid Anti-Bot Links' in response_text:
                console.print("[red]Invalid Anti-Bot Links![/red]")
                console.print(SEP)
                return False, None
            
            elif 'success' in response_text.lower() or 'claimed' in response_text.lower():
                console.print("[green]Claim appears successful![/green]")
                wait_time = self.parse_timer(response_text)
                console.print(SEP)
                return True, wait_time if wait_time > 0 else 300
            
            else:
                console.print(f"[yellow]Unknown response:[/yellow]")
                console.print(f"[dim]{response_text[:300]}...[/dim]")
                console.print(SEP)
                return False, None
                
        except Exception as e:
            console.print(f"[red]Verify error: {e}[/red]")
            console.print(SEP)
            return False, None
    
    def continuous_claim(self):
        console.clear()
        self.display_banner()
        
        console.print()
        TypeWriter.type_text("Initializing PSYCHO BOT...", 0.03, "bold green")
        
        startup_text = Text()
        startup_text.append("Email: ", style="bold yellow")
        startup_text.append(f"{self.config.get('email')}\n", style="cyan")
        startup_text.append("Target: ", style="bold yellow")
        startup_text.append("claimcoin.in\n", style="cyan")
        startup_text.append("Max Fails: ", style="bold yellow")
        startup_text.append(f"{self.max_fails}", style="cyan")
        
        console.print(Panel(startup_text, border_style="green", title="Configuration"))
        time.sleep(1)
        
        FancyProgress.show_progress("Logging In", 40, "magenta")
        console.print()
        
        if not self.login():
            console.print()
            console.print(Panel("[bold red]Login Failed! Cannot continue.[/bold red]", border_style="red"))
            return
        
        console.print()
        TypeWriter.type_text("Bot is ready! Starting claim loop...", 0.03, "bold green")
        console.print()
        
        while self.consecutive_fails < self.max_fails:
            self.claim_count += 1
            
            console.print(f"[bold cyan]━━━ Claim #{self.claim_count} ━━━[/bold cyan]")
            
            result, wait_time = self.claim_faucet()
            
            if result == "relogin":
                console.print("[yellow]Re-logging in...[/yellow]")
                if not self.login():
                    console.print("[red]Re-login failed![/red]")
                console.print()
                continue
            
            if result and wait_time:
                self.consecutive_fails = 0
                
                console.print(f"[yellow]Cooldown: {wait_time}s[/yellow]")
                
                with Progress(SpinnerColumn("dots"), TextColumn("[yellow]{task.description}[/yellow]"), BarColumn(bar_width=40, style="yellow"), TimeElapsedColumn(), TextColumn("[cyan]{task.fields[rem]}[/cyan]"), console=console, transient=True) as progress:
                    task = progress.add_task("[yellow]Waiting...[/yellow]", total=wait_time, rem=f"{wait_time}s")
                    for i in range(wait_time):
                        time.sleep(1)
                        rem = wait_time - i - 1
                        progress.update(task, advance=1, rem=f"{rem}s")
                
                console.print()
            
            else:
                self.consecutive_fails += 1
                console.print(f"[red]Claim failed! ({self.consecutive_fails}/{self.max_fails})[/red]")
                
                if self.consecutive_fails >= self.max_fails:
                    console.print()
                    console.print(Panel("[bold red]MAX FAILURES REACHED![/bold red]", border_style="red"))
                    console.print(SEP)
                    break
                
                console.print(f"[yellow]Retrying in 30 seconds...[/yellow]")
                with Progress(SpinnerColumn("dots"), TextColumn("[red]{task.description}[/red]"), BarColumn(bar_width=40, style="red"), console=console, transient=True) as progress:
                    task = progress.add_task("[red]Retry cooldown...[/red]", total=30)
                    for i in range(30):
                        time.sleep(1)
                        progress.update(task, advance=1)
                console.print()
        
        # Summary
        console.print()
        console.print(SEP)
        summary = Table(title="FINAL SUMMARY", box=box.DOUBLE, border_style="cyan")
        summary.add_column("Metric", style="bold yellow", width=20)
        summary.add_column("Value", style="bold green", width=30)
        summary.add_row("Email", self.config.get("email"))
        summary.add_row("Total Attempts", str(self.claim_count))
        summary.add_row("Total Claimed", f"{self.total_claimed} CCP")
        console.print(summary)
        console.print(SEP)
    
    @staticmethod
    def display_banner():
        console.clear()
        try:
            banner = pyfiglet.figlet_format("PSYCHO BOT", font="slant")
            console.print(Panel(banner, style="bold magenta", border_style="magenta"))
        except:
            console.print(Panel("PSYCHO BOT", style="bold magenta", border_style="magenta"))
        
        info_table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        info_table.add_column("Key", style="bold yellow", width=15)
        info_table.add_column("Value", style="green")
        info_table.add_row("DEVELOPER", "alphapython12")
        info_table.add_row("CHANNEL", "psychobot1")
        info_table.add_row("DOMAIN", "ClaimCoin.in")
        info_table.add_row("CAPTCHA", "TURNSTILE + ANTIBOT")
        console.print(info_table)
        
        console.print(Columns([
            Panel("[bold red]WARNING: [/bold red][yellow]USE AT YOUR OWN RISK![/yellow]", border_style="red"),
            Panel("[blue]STATUS: [/blue][green]FREE[/green]    [blue]BYPASS: [/blue][yellow]AUTO[/yellow]", border_style="blue")
        ]))
        console.print()

class Menu:
    def __init__(self):
        self.config = Config()
    
    def show_main_menu(self):
        console.clear()
        ClaimCoinFaucet.display_banner()
        
        menu_table = Table(show_header=False, box=box.ROUNDED, border_style="cyan", title="MAIN MENU", title_style="bold cyan")
        menu_table.add_column("Option", style="bold white", width=5, justify="center")
        menu_table.add_column("Description", style="cyan")
        
        menu_table.add_row("[1]", "SETUP ALPHA SOLVER")
        menu_table.add_row("[2]", "SET USER AGENT")
        menu_table.add_row("[3]", "SET EMAIL & PASSWORD")
        menu_table.add_row("[4]", "CHECK IP ADDRESS")
        menu_table.add_row("[5]", "START WORK")
        
        console.print(menu_table)
        console.print()
        console.print("[bold yellow]       > [/bold yellow]", end="")
    
    def setup_alpha_solver(self):
        console.clear()
        ClaimCoinFaucet.display_banner()
        TypeWriter.type_text("ALPHA SOLVER SETUP", 0.03, "bold cyan")
        console.print()
        AlphaSolver.setup_session()
    
    def set_user_agent(self):
        console.clear()
        ClaimCoinFaucet.display_banner()
        current_ua = self.config.get("user_agent")
        console.print(f"[yellow]Current UA:[/yellow] [dim]{current_ua[:60]}...[/dim]")
        console.print()
        user_agent = TypeWriter.type_input("Enter User-Agent: ", "cyan")
        if user_agent:
            self.config.set("user_agent", user_agent)
            FancyProgress.show_progress("Saving", 20, "green")
            console.print("[bold green]SAVED![/bold green]")
        console.print()
        console.print(SEP)
        console.print("[yellow]PRESS ENTER . . .[/yellow]", end="")
        input()
    
    def set_email_password(self):
        console.clear()
        ClaimCoinFaucet.display_banner()
        current_email = self.config.get("email")
        if current_email:
            console.print(f"[yellow]Current Email:[/yellow] [cyan]{current_email}[/cyan]")
        console.print()
        email = TypeWriter.type_input("Enter Email: ", "cyan")
        if email and '@' in email:
            self.config.set("email", email)
            console.print("[green]Email saved![/green]")
        else:
            console.print("[red]Invalid email![/red]")
            console.print(SEP)
            console.print("[yellow]PRESS ENTER . . .[/yellow]", end="")
            input()
            return
        console.print()
        password = TypeWriter.type_input("Enter Password: ", "cyan")
        if password:
            self.config.set("password", password)
            FancyProgress.show_progress("Saving", 20, "green")
            console.print("[bold green]CREDENTIALS SAVED![/bold green]")
        console.print()
        console.print(SEP)
        console.print("[yellow]PRESS ENTER . . .[/yellow]", end="")
        input()
    
    def check_ip(self):
        console.clear()
        ClaimCoinFaucet.display_banner()
        IPChecker.display_ip_info()
        console.print()
        console.print(SEP)
        console.print("[yellow]PRESS ENTER . . .[/yellow]", end="")
        input()
    
    def start_work(self):
        email = self.config.get("email")
        password = self.config.get("password")
        
        if not email or not password:
            console.print("[red]Please set email & password first! (Option 3)[/red]")
            time.sleep(2)
            return
        
        console.clear()
        ClaimCoinFaucet.display_banner()
        
        info = Text()
        info.append("Email: ", style="bold yellow")
        info.append(f"{email}\n", style="cyan")
        info.append("Password: ", style="bold yellow")
        info.append(f"{'*' * len(password)}", style="cyan")
        console.print(Panel(info, border_style="green", title="Credentials"))
        console.print()
        
        TypeWriter.type_text("Starting bot...", 0.03, "bold green")
        time.sleep(2)
        
        faucet = ClaimCoinFaucet(self.config)
        faucet.continuous_claim()
        
        console.print()
        console.print(SEP)
        console.print("[yellow]PRESS ENTER . . .[/yellow]", end="")
        input()
    
    def run(self):
        while True:
            try:
                self.show_main_menu()
                choice = input().strip()
                if choice == '1': self.setup_alpha_solver()
                elif choice == '2': self.set_user_agent()
                elif choice == '3': self.set_email_password()
                elif choice == '4': self.check_ip()
                elif choice == '5': self.start_work()
                elif choice.lower() == 'exit':
                    console.clear()
                    console.print(Panel("[red]Goodbye![/red]", border_style="red"))
                    break
                else:
                    console.print("[red]Invalid choice![/red]")
                    time.sleep(1)
            except KeyboardInterrupt:
                console.clear()
                console.print(Panel("[yellow]Interrupted![/yellow]", border_style="yellow"))
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                time.sleep(2)

def create_ip_script():
    if not os.path.exists("ip.py"):
        with open("ip.py", "w") as f:
            f.write('''#!/usr/bin/env python3
import requests, json, sys
def get_ip_info():
    try:
        r = requests.get("http://ip-api.com/json/", timeout=10)
        if r.status_code == 200:
            d = r.json()
            if d.get("status") == "success":
                return {"success":"true","ip":d.get("query"),"country":d.get("country"),"city":d.get("city"),"isp":d.get("isp")}
    except: pass
    return {"success":"false"}
if __name__ == "__main__":
    print(json.dumps(get_ip_info(), indent=2))
''')
        os.chmod("ip.py", 0o755)

if __name__ == "__main__":
    try:
        import pyfiglet, colorama, requests, rich
        from telethon import TelegramClient
        from bs4 import BeautifulSoup
    except ImportError:
        console.print("[yellow]Installing packages...[/yellow]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet", "colorama", "requests", "rich", "telethon", "beautifulsoup4"])
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    create_ip_script()
    Menu().run()
