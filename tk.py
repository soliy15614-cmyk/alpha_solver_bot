#!/usr/bin/env python3
import requests
import time
import re
import json
import os
import sys
import subprocess
from datetime import datetime
from colorama import init, Fore, Back, Style
import pyfiglet
from typing import Optional, Dict, Any
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich import box
import threading

# Initialize colorama
init(autoreset=True)

# Rich console
console = Console()

class Config:
    """Configuration management"""
    CONFIG_FILE = "psycho_config.json"
    
    def __init__(self):
        self.data = {
            "faucetpay_email": "",
            "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
            "cookie_file": "taraking_cookies.json"
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
    def get_ip_info() -> Optional[Dict[str, Any]]:
        try:
            if os.path.exists("ip.py"):
                result = subprocess.run(
                    [sys.executable, "ip.py", "info"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return json.loads(result.stdout)
            
            response = requests.get("http://ip-api.com/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "success": "true",
                        "ip": data.get("query", "Unknown"),
                        "country": data.get("country", "Unknown"),
                        "country_code": data.get("countryCode", "Unknown"),
                        "region": data.get("regionName", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "zip": data.get("zip", "Unknown"),
                        "timezone": data.get("timezone", "Unknown"),
                        "isp": data.get("isp", "Unknown"),
                        "organization": data.get("org", "Unknown")
                    }
        except:
            pass
        return None

    @staticmethod
    def display_ip_info():
        info = IPChecker.get_ip_info()
        if not info:
            console.print("[red][!] Failed to fetch IP information[/red]")
            return
        
        table = Table(show_header=False, box=box.SIMPLE, border_style="cyan")
        table.add_column("Key", style="yellow", width=20)
        table.add_column("Value", style="green")
        
        rows = [
            ("𝐈𝐏", info.get('ip', 'N/A')),
            ("𝐂𝐎𝐔𝐍𝐓𝐑𝐘", info.get('country', 'N/A')),
            ("𝐂𝐎𝐔𝐍𝐓𝐑𝐘_𝐂𝐎𝐃𝐄", info.get('country_code', 'N/A')),
            ("𝐑𝐄𝐆𝐈𝐎𝐍", info.get('region', 'N/A')),
            ("𝐂𝐈𝐓𝐘", info.get('city', 'N/A')),
            ("𝐙𝐈𝐏", info.get('zip', 'N/A')),
            ("𝐓𝐈𝐌𝐄𝐙𝐎𝐍𝐄", info.get('timezone', 'N/A')),
            ("𝐈𝐒𝐏", info.get('isp', 'N/A')),
            ("𝐎𝐑𝐆𝐀𝐍𝐈𝐙𝐀𝐓𝐈𝐎𝐍", info.get('organization', 'N/A'))
        ]
        
        for key, value in rows:
            table.add_row(key, value)
        
        console.print(table)

class ClaimDisplay:
    """Manages the claim success display panel"""
    
    def __init__(self):
        self.success_messages = []
        self.max_display = 10
        self.lock = threading.Lock()
    
    def add_success(self, message: str):
        with self.lock:
            self.success_messages.append(message)
            if len(self.success_messages) > self.max_display:
                self.success_messages.pop(0)
    
    def get_display(self) -> str:
        with self.lock:
            if not self.success_messages:
                return ""
            return "\n".join(self.success_messages)

class TaraKingFaucet:
    """Main Faucet Claim Bot with Rich UI"""
    
    def __init__(self, config: Config):
        self.base_url = "https://taraking.top"
        self.config = config
        self.session = requests.Session()
        self.consecutive_fails = 0
        self.max_fails = 3
        self.claim_count = 0
        self.display = ClaimDisplay()
        self.load_cookies()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def save_cookies(self):
        try:
            cookie_file = self.config.get("cookie_file")
            cookies_dict = {}
            for cookie in self.session.cookies:
                cookies_dict[cookie.name] = {
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'expires': cookie.expires if hasattr(cookie, 'expires') else None,
                    'secure': cookie.secure
                }
            with open(cookie_file, 'w') as f:
                json.dump(cookies_dict, f, indent=2)
        except:
            pass
    
    def load_cookies(self):
        try:
            cookie_file = self.config.get("cookie_file")
            if os.path.exists(cookie_file):
                with open(cookie_file, 'r') as f:
                    cookies_dict = json.load(f)
                for name, cookie_data in cookies_dict.items():
                    self.session.cookies.set(
                        name=name,
                        value=cookie_data['value'],
                        domain=cookie_data.get('domain', ''),
                        path=cookie_data.get('path', '/')
                    )
        except:
            pass
    
    def get_headers(self, extra_headers: dict = None) -> dict:
        headers = {
            'User-Agent': self.config.get("user_agent"),
            'sec-ch-ua': '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'x-requested-with': 'mark.via.gp',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        
        if extra_headers:
            headers.update(extra_headers)
        
        cookie_str = '; '.join([f'{c.name}={c.value}' for c in self.session.cookies])
        if cookie_str:
            headers['Cookie'] = cookie_str
            
        return headers
    
    def extract_form_field(self) -> Optional[str]:
        try:
            response = self.session.get(
                self.base_url,
                headers=self.get_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                })
            )
            
            self.save_cookies()
            
            patterns = [
                r'name="([^"]+)"[^>]*placeholder="Enter your FaucetPay registered email"',
                r'name="([^"]+)"[^>]*placeholder="[^"]*[Ee]mail[^"]*"',
                r'<input[^>]*type="(?:text|email)"[^>]*name="([^"]+)"[^>]*class="[^"]*form-control[^"]*"'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response.text, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            return None
        except:
            return None
    
    def generate_captcha(self) -> Optional[Dict]:
        try:
            response = self.session.get(
                f"{self.base_url}/iconcaptcha.php",
                params={'action': 'generate'},
                headers=self.get_headers({
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': f"{self.base_url}/",
                    'priority': 'u=1, i'
                })
            )
            
            if response.status_code != 200:
                return None
            
            return response.json()
        except:
            return None
    
    def verify_captcha(self, target_key: str, token: str) -> Optional[str]:
        try:
            payload = {
                "selected": target_key,
                "token": token
            }
            
            response = self.session.post(
                f"{self.base_url}/iconcaptcha.php",
                params={'action': 'verify'},
                json=payload,
                headers=self.get_headers({
                    'Content-Type': 'application/json',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'origin': self.base_url,
                    'referer': f"{self.base_url}/",
                    'priority': 'u=1, i'
                })
            )
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            
            if data.get('success'):
                return data.get('pass_token', '')
            
            return None
        except:
            return None
    
    def wait_and_navigate(self):
        try:
            self.session.get(
                f"{self.base_url}/openlink.php",
                headers=self.get_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-dest': 'document',
                    'referer': f"{self.base_url}/",
                    'priority': 'u=0, i'
                }),
                allow_redirects=True
            )
        except:
            pass
    
    def extract_messages(self, html_content: str) -> list:
        messages = []
        
        success_pattern = r'<div[^>]*class="[^"]*alert[^"]*alert-success[^"]*"[^>]*>(.*?)</div>'
        success_matches = re.findall(success_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        error_pattern = r'<div[^>]*class="[^"]*alert[^"]*alert-(?:danger|warning|error)[^"]*"[^>]*>(.*?)</div>'
        error_matches = re.findall(error_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        def clean_html(text):
            clean = re.sub(r'<[^>]+>', '', text)
            clean = re.sub(r'\s+', ' ', clean)
            return clean.strip()
        
        for msg in success_matches:
            messages.append(('SUCCESS', clean_html(msg)))
        
        for msg in error_matches:
            messages.append(('ERROR', clean_html(msg)))
        
        return messages
    
    def submit_claim(self, field_name: str, pass_token: str) -> Optional[str]:
        try:
            payload = {
                field_name: self.config.get("faucetpay_email"),
                'captcha_type': 'icon',
                'icon_pass_token': pass_token
            }
            
            response = self.session.post(
                self.base_url,
                data=payload,
                headers=self.get_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'cache-control': 'max-age=0',
                    'upgrade-insecure-requests': '1',
                    'origin': self.base_url,
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': f"{self.base_url}/",
                    'priority': 'u=0, i'
                }),
                allow_redirects=True
            )
            
            messages = self.extract_messages(response.text)
            
            if messages:
                for msg_type, msg_text in messages:
                    if msg_type == 'SUCCESS':
                        self.consecutive_fails = 0
                        return msg_text
                    elif msg_type == 'ERROR':
                        pass
                
                return messages[-1][1] if messages else None
            else:
                return None
                
        except:
            return None
    
    def single_claim(self) -> Optional[str]:
        """Execute single claim attempt, return success message or None"""
        try:
            # Step 1: Extract form field
            field_name = self.extract_form_field()
            if not field_name:
                self.consecutive_fails += 1
                return None
            
            # Step 2: Generate captcha
            captcha_data = self.generate_captcha()
            if not captcha_data:
                self.consecutive_fails += 1
                return None
            
            # Step 3: Verify captcha
            pass_token = self.verify_captcha(
                captcha_data['target_key'],
                captcha_data['token']
            )
            if not pass_token:
                self.consecutive_fails += 1
                return None
            
            # Step 4: Navigate
            self.wait_and_navigate()
            
            # Step 5: Wait 12 seconds
            time.sleep(12)
            
            # Step 6: Submit claim
            result = self.submit_claim(field_name, pass_token)
            
            self.save_cookies()
            
            if result:
                self.consecutive_fails = 0
                return result
            else:
                self.consecutive_fails += 1
                return None
                
        except:
            self.consecutive_fails += 1
            return None
    
    @staticmethod
    def display_banner():
        """Display PSYCHO BOT banner"""
        console.clear()
        
        # ASCII Art
        try:
            banner = pyfiglet.figlet_format("PSYCHO BOT", font="slant")
            console.print(Panel(banner, style="bold magenta", border_style="magenta"))
        except:
            console.print(Panel("PSYCHO BOT", style="bold magenta", border_style="magenta"))
        
        # Info Panel
        info_table = Table(show_header=False, box=box.SIMPLE, border_style="cyan")
        info_table.add_column("Key", style="yellow", width=15)
        info_table.add_column("Value", style="green")
        
        info_table.add_row("[ DEVELOPER ]", "alphapython12")
        info_table.add_row("[ CHANNEL ]", "psychobot1")
        info_table.add_row("[ DOMAIN ]", "Taraking.top")
        info_table.add_row("[ CAPTCHA ]", "ICON CAPTCHA")
        
        console.print(info_table)
        
        # Warning Panel
        warning_text = Text()
        warning_text.append("[!! WARNING !!] ", style="bold red")
        warning_text.append("THIS IS YOUR OWN RISK !", style="yellow")
        
        status_text = Text()
        status_text.append("[ STATUS ] ", style="blue")
        status_text.append("FREE", style="green")
        status_text.append("    ")
        status_text.append("[ BYPASS ] ", style="blue")
        status_text.append("NON_API_KEY", style="yellow")
        
        console.print(Panel(warning_text, border_style="red"))
        console.print(Panel(status_text, border_style="blue"))
        console.print()

    def display_claim_interface(self, progress, task_id, current_status: str):
        """Display the claim interface with Rich"""
        
        # Build layout
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="success", size=len(self.display.success_messages) + 3 if self.display.success_messages else 3)
        )
        
        # Header
        header_text = Text()
        header_text.append("🤖 PSYCHO BOT - AUTO CLAIM", style="bold magenta")
        header_text.append(f"\n📧 {self.config.get('faucetpay_email')}", style="cyan")
        layout["header"].update(Panel(header_text, border_style="magenta"))
        
        # Main status
        main_table = Table(show_header=False, box=box.SIMPLE, border_style="cyan")
        main_table.add_column("Status", style="yellow", width=20)
        main_table.add_column("Info", style="white")
        
        main_table.add_row("🔄 Current Status", f"[bold cyan]{current_status}[/bold cyan]")
        main_table.add_row("📊 Total Claims", f"[green]{self.claim_count}[/green]")
        main_table.add_row("❌ Consecutive Fails", f"[red]{self.consecutive_fails}/{self.max_fails}[/red]")
        main_table.add_row("⏱️ Progress", progress)
        
        layout["main"].update(Panel(main_table, title="[bold]Claim Progress[/bold]", border_style="cyan"))
        
        # Success messages
        if self.display.success_messages:
            success_text = Text()
            for msg in self.display.success_messages:
                success_text.append("~" * 60 + "\n", style="green")
                success_text.append(f"[ SUCCESS ] {msg}\n", style="bold green")
                success_text.append("~" * 60 + "\n", style="green")
            
            layout["success"].update(
                Panel(success_text, title="[bold]✅ Recent Successes[/bold]", border_style="green")
            )
        else:
            layout["success"].update(
                Panel("[yellow]Waiting for first success...[/yellow]", border_style="yellow")
            )
        
        console.print(layout)

    def continuous_claim(self):
        """Run continuous claiming with Rich UI"""
        console.clear()
        self.display_banner()
        
        # Initial setup panel
        setup_text = Text()
        setup_text.append("🚀 Starting PSYCHO BOT...\n", style="bold green")
        setup_text.append(f"📧 Email: {self.config.get('faucetpay_email')}\n", style="cyan")
        setup_text.append(f"⚠️  Max Fails: {self.max_fails}\n", style="yellow")
        setup_text.append(f"⏱️  Wait between claims: 12 seconds", style="yellow")
        
        console.print(Panel(setup_text, border_style="green"))
        time.sleep(2)
        
        while self.consecutive_fails < self.max_fails:
            self.claim_count += 1
            
            # Create progress for claim process
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                
                # Step 1: Extract form field
                task = progress.add_task("[cyan]Extracting form field...", total=100)
                field_name = self.extract_form_field()
                progress.update(task, advance=33)
                time.sleep(0.5)
                
                if not field_name:
                    progress.update(task, description="[red]❌ Failed to extract form field!", completed=100)
                    self.consecutive_fails += 1
                    time.sleep(1)
                    continue
                
                progress.update(task, advance=33, description="[green]✅ Form field extracted")
                time.sleep(0.5)
                
                # Step 2: Generate captcha
                progress.update(task, description="[cyan]🎯 Generating captcha...")
                captcha_data = self.generate_captcha()
                progress.update(task, advance=34)
                
                if not captcha_data:
                    progress.update(task, description="[red]❌ Captcha generation failed!", completed=100)
                    self.consecutive_fails += 1
                    time.sleep(1)
                    continue
                
                progress.update(task, description="[green]✅ Captcha generated", completed=100)
                time.sleep(0.5)
            
            # Step 3: Verify captcha (separate progress for quick action)
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress2:
                task2 = progress2.add_task("[cyan]🔑 Verifying captcha...", total=100)
                pass_token = self.verify_captcha(
                    captcha_data['target_key'],
                    captcha_data['token']
                )
                progress2.update(task2, advance=50)
                
                if not pass_token:
                    progress2.update(task2, description="[red]❌ Verification failed!", completed=100)
                    self.consecutive_fails += 1
                    time.sleep(1)
                    continue
                
                progress2.update(task2, description="[green]✅ Captcha verified!", completed=100)
                time.sleep(0.5)
            
            # Step 4: Navigate and wait
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console
            ) as progress3:
                task3 = progress3.add_task("[cyan]⏳ Navigating & waiting 12 seconds...", total=120)
                
                self.wait_and_navigate()
                
                # Animated 12 second wait
                for i in range(12):
                    time.sleep(1)
                    progress3.update(task3, advance=10)
                
                progress3.update(task3, description="[green]✅ Wait completed!", completed=100)
                time.sleep(0.5)
            
            # Step 5: Submit claim
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress4:
                task4 = progress4.add_task("[cyan]📤 Submitting claim...", total=100)
                result = self.submit_claim(field_name, pass_token)
                progress4.update(task4, advance=100)
                
                if result:
                    progress4.update(task4, description="[bold green]✅ CLAIM SUCCESSFUL![/bold green]", completed=100)
                    
                    # Add to success display
                    self.display.add_success(result)
                    
                    # Show success with panel
                    console.print()
                    console.print("~" * 60, style="green")
                    console.print(f"[SUCCESS] {result}", style="bold green")
                    console.print("~" * 60, style="green")
                    
                    # Wait 12 seconds before next claim
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TimeElapsedColumn(),
                        console=console
                    ) as wait_progress:
                        wait_task = wait_progress.add_task("[yellow]⏳ Waiting 12 seconds for next claim...", total=120)
                        for i in range(12):
                            time.sleep(1)
                            wait_progress.update(wait_task, advance=10)
                    
                else:
                    progress4.update(task4, description="[red]❌ Claim failed![/red]", completed=100)
                    self.consecutive_fails += 1
                    
                    if self.consecutive_fails >= self.max_fails:
                        console.print()
                        console.print("[bold red]🛑 MAXIMUM FAILURES REACHED! STOPPING...[/bold red]")
                        break
                    
                    console.print(f"\n[red]Consecutive fails: {self.consecutive_fails}/{self.max_fails}[/red]")
                    time.sleep(3)
            
            # Clear for next iteration
            console.clear()
            self.display_banner()
            
            # Show success history
            if self.display.success_messages:
                console.print(Panel(
                    "\n".join(self.display.success_messages),
                    title="[bold green]✅ Claim History[/bold green]",
                    border_style="green"
                ))
        
        # Final summary
        console.print()
        summary = Table(title="[bold]📊 FINAL SUMMARY[/bold]", box=box.DOUBLE, border_style="cyan")
        summary.add_column("Metric", style="yellow")
        summary.add_column("Value", style="green")
        summary.add_row("Total Claims", str(self.claim_count))
        summary.add_row("Successful", str(len(self.display.success_messages)))
        summary.add_row("Failed", str(self.claim_count - len(self.display.success_messages)))
        summary.add_row("Email", self.config.get("faucetpay_email"))
        console.print(summary)

class Menu:
    """Interactive Menu System with Rich"""
    
    def __init__(self):
        self.config = Config()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_main_menu(self):
        console.clear()
        TaraKingFaucet.display_banner()
        
        menu_table = Table(show_header=False, box=box.SIMPLE, border_style="cyan")
        menu_table.add_column("Option", style="white", width=5)
        menu_table.add_column("Description", style="cyan")
        
        menu_table.add_row("[1]", "𝐒𝐄𝐓 𝐔𝐒𝐄𝐑 𝐀𝐆𝐄𝐍𝐓")
        menu_table.add_row("[2]", "𝐒𝐄𝐓 𝐅𝐀𝐔𝐂𝐄𝐓𝐏𝐀𝐘 𝐄𝐌𝐀𝐈𝐋")
        menu_table.add_row("[3]", "𝐂𝐇𝐄𝐂𝐊 𝐈𝐏 𝐀𝐃𝐃𝐑𝐄𝐒𝐒")
        menu_table.add_row("[4]", "𝐒𝐓𝐀𝐑𝐓 𝐖𝐎𝐑𝐊")
        
        console.print(menu_table)
        console.print("\n[yellow]       ➤ [/yellow]", end="")
    
    def set_user_agent(self):
        console.clear()
        TaraKingFaucet.display_banner()
        
        console.print("\n[green][+] 𝐄𝐍𝐓𝐄𝐑 𝐔𝐒𝐄𝐑 𝐀𝐆𝐄𝐍𝐓 => [/green]", end="")
        user_agent = input().strip()
        
        if user_agent:
            self.config.set("user_agent", user_agent)
            console.print("\n[green][+] USER-AGENT SAVED ![/green]")
        else:
            console.print("\n[red][!] Invalid input! Using default.[/red]")
        
        console.print("\n[cyan]_______________________________________________[/cyan]")
        input("[yellow]PRESS ENTER . . .[/yellow]")
    
    def set_email(self):
        console.clear()
        TaraKingFaucet.display_banner()
        
        console.print("\n[green][+] 𝐄𝐍𝐓𝐄𝐑 𝐅𝐀𝐔𝐂𝐄𝐓𝐏𝐀𝐘 𝐄𝐌𝐀𝐈𝐋 => [/green]", end="")
        email = input().strip()
        
        if email and '@' in email:
            self.config.set("faucetpay_email", email)
            console.print("\n[green][+] FAUCETPAY EMAIL SAVED ![/green]")
        else:
            console.print("\n[red][!] Invalid email format![/red]")
        
        console.print("\n[cyan]_______________________________________________[/cyan]")
        input("[yellow]PRESS ENTER . . .[/yellow]")
    
    def check_ip(self):
        console.clear()
        TaraKingFaucet.display_banner()
        
        IPChecker.display_ip_info()
        
        console.print("\n[cyan]_______________________________________________[/cyan]")
        input("[yellow]PRESS ENTER . . .[/yellow]")
    
    def start_work(self):
        email = self.config.get("faucetpay_email")
        
        if not email:
            console.print("\n[red][!] Please set FaucetPay email first! (Option 2)[/red]")
            time.sleep(2)
            return
        
        faucet = TaraKingFaucet(self.config)
        faucet.continuous_claim()
        
        console.print("\n[cyan]_______________________________________________[/cyan]")
        input("[yellow]PRESS ENTER . . .[/yellow]")
    
    def run(self):
        while True:
            try:
                self.show_main_menu()
                choice = input().strip()
                
                if choice == '1':
                    self.set_user_agent()
                elif choice == '2':
                    self.set_email()
                elif choice == '3':
                    self.check_ip()
                elif choice == '4':
                    self.start_work()
                elif choice.lower() == 'exit':
                    console.clear()
                    console.print("[red]Goodbye![/red]")
                    break
                else:
                    console.print("\n[red][!] Invalid choice![/red]")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                console.clear()
                console.print("\n[red][!] Interrupted by user![/red]")
                break
            except Exception as e:
                console.print(f"\n[red][!] Error: {e}[/red]")
                time.sleep(2)

def create_ip_script():
    ip_script = '''#!/usr/bin/env python3
import requests
import json
import sys

def get_ip_info():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "success": "true",
                    "ip": data.get("query", "Unknown"),
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "zip": data.get("zip", "Unknown"),
                    "latitude": data.get("lat", 0),
                    "longitude": data.get("lon", 0),
                    "timezone": data.get("timezone", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "organization": data.get("org", "Unknown"),
                    "as": data.get("as", "Unknown")
                }
    except Exception as e:
        pass
    
    return {"success": "false", "error": "Failed to fetch IP info"}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "info":
        print(json.dumps(get_ip_info(), indent=2))
    else:
        print(json.dumps(get_ip_info(), indent=2))
'''
    
    if not os.path.exists("ip.py"):
        with open("ip.py", "w") as f:
            f.write(ip_script)
        os.chmod("ip.py", 0o755)

if __name__ == "__main__":
    # Check and install required packages
    try:
        import pyfiglet
        import colorama
        import requests
        import rich
    except ImportError:
        console.print("[yellow]Installing required packages...[/yellow]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet", "colorama", "requests", "rich"])
        console.print("[green]Packages installed! Restarting...[/green]")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    create_ip_script()
    
    menu = Menu()
    menu.run()
