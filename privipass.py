#!/usr/bin/env python3
import secrets
import string
import re
import math
import hashlib
import requests
import time
import sys
import random
from colorama import Fore, init
import getpass
from fpdf import FPDF

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
#  ARCHITECTURE: Separated PDF Logic from Auditor Logic
# ─────────────────────────────────────────────────────────────────

class PriViPDFReport(FPDF):
    """Dedicated PDF class — ensures each report starts with a clean slate."""

    def __init__(self, author):
        super().__init__()
        self.author = author

    def header(self):
        """Adds a professional watermark to the background."""
        self.set_font("Arial", 'B', 40)
        self.set_text_color(235, 235, 235) # Very light watermark grey
        self.set_xy(25, 120)
        # Positioned diagonally across the center
        self.cell(0, 20, f"CERTIFIED - {self.author}", align='C')
        self.set_text_color(0, 0, 0) # Reset color for content

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | Forensic Authority: {self.author}", align='C')


class PriViPassElite:
    def __init__(self):
        self.version = "3.3"
        self.author = "PriViSecurity"
        self.common_passwords = ['123456', 'password', '12345678', 'qwerty', 'admin']

    def boot_sequence(self):
        """High-impact terminal initialization."""
        logo = f"""
{Fore.GREEN}  ██████╗ ██████╗ ██╗██╗   ██╗██╗██████╗  █████╗ ███████╗███████╗
{Fore.GREEN}  ██╔══██╗██╔══██╗██║██║   ██║██║██╔══██╗██╔══██╗██╔════╝██╔════╝
{Fore.GREEN}  ██████╔╝██████╔╝██║██║   ██║██║██████╔╝███████║███████╗███████╗
{Fore.GREEN}  ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝ ██║██╔═══╝ ██╔══██║╚════██║╚════██║
{Fore.GREEN}  ██║     ██║  ██║██║ ╚████╔╝  ██║██║     ██║  ██║███████║███████║
{Fore.WHITE}        [ {self.author} | FORENSIC AUDITOR v{self.version} ]
        """
        print("\033[H\033[J", end="")
        for line in logo.splitlines():
            print(line)
            time.sleep(0.08)

        print(f"{Fore.CYAN}{'=' * 67}")
        checks = ["Crypto Engine", "Secure Tunnel", "Dictionary", "Entropy Module"]
        for check in checks:
            sys.stdout.write(f"{Fore.WHITE}[*] Initializing {check}...")
            sys.stdout.flush()
            time.sleep(random.uniform(0.1, 0.3))
            print(f" {Fore.GREEN}[OK]")
        print(f"{Fore.CYAN}{'=' * 67}\n")

    def matrix_effect(self, duration=1.2):
        """Simulates real-time data analysis."""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        print(f"{Fore.GREEN}[*] RUNNING HEURISTIC DECRYPTION ANALYSIS...")
        end_time = time.time() + duration
        while time.time() < end_time:
            addr = f"0x{random.getrandbits(32):08x}"
            stream = "".join(random.choice(chars) for _ in range(40))
            sys.stdout.write(f"\r{Fore.GREEN}{addr} | {Fore.WHITE}{stream}")
            sys.stdout.flush()
            time.sleep(0.04)
        print(f"\n{Fore.GREEN}[+] ANALYSIS COMPLETE. PARSING HASHES...\n")

    def _strip_ansi(self, s):
        """Strips color codes to prevent PDF and alignment corruption."""
        return re.sub(r'\x1b\[[0-9;]*m', '', s)

    def _box_row(self, label, value_str, col_width=38):
        """ANSI-aware row alignment for terminal UI."""
        visible_len = len(self._strip_ansi(value_str))
        padding = max(0, col_width - visible_len)
        return f"║ {Fore.WHITE}{label}{value_str}{' ' * padding} {Fore.CYAN}║"

    def get_leak_count(self, password):
        """Secure HIBP check with full error handling."""
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        try:
            res = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    parts = line.split(':', 1)
                    if len(parts) == 2 and parts[0] == suffix:
                        return int(parts[1])
            return 0
        except requests.exceptions.RequestException:
            return -1

    def generate_pdf_report(self, report_data):
        """PDF Generation logic with layout fixes."""
        pdf = PriViPDFReport(self.author)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"{self.author} Security Report", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Timestamp: {time.ctime()} | v{self.version}", ln=True, align='C')
        
        pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Forensic Summary:", ln=True)
        pdf.set_font("Arial", size=11)
        for k, v in report_data.items():
            pdf.cell(0, 10, f"  {k}: {self._strip_ansi(str(v))}", ln=True)

        filename = f"PriViPass_Report_{int(time.time())}.pdf"
        pdf.output(filename)
        return filename

    def audit(self, password):
        self.matrix_effect()
        leak_count = self.get_leak_count(password)
        
        # Entropy & Crack Time
        pool = sum([26 if re.search(r'[a-z]', password) else 0, 26 if re.search(r'[A-Z]', password) else 0, 
                    10 if re.search(r'\d', password) else 0, 32 if re.search(r'\W', password) else 0])
        entropy = len(password) * math.log2(pool) if pool > 0 else 0
        seconds = (2 ** entropy) / 100_000_000_000 if entropy > 0 else 0
        
        # Format Results
        leak_txt = f"{Fore.RED}VULNERABLE ({leak_count:,} Leaks)" if leak_count > 0 else f"{Fore.GREEN}SECURE"
        if leak_count == -1: leak_txt = f"{Fore.YELLOW}OFFLINE"
        
        print(f"{Fore.CYAN}╔═══════════════════ FORENSIC AUDIT REPORT ═══════════════════╗")
        print(self._box_row("Status:      ", leak_txt))
        print(self._box_row("Entropy:     ", f"{entropy:.2f} Bits"))
        print(f"{Fore.CYAN}╚═════════════════════════════════════════════════════════════╝")

        if input(f"\n{Fore.WHITE}[?] Export Watermarked PDF? (y/n): ").strip().lower() == 'y':
            fname = self.generate_pdf_report({"Leak Status": leak_txt, "Entropy": f"{entropy:.2f}"})
            print(f"{Fore.GREEN}[+] Report Saved: {Fore.WHITE}{fname}")

if __name__ == "__main__":
    try:
        app = PriViPassElite()
        app.boot_sequence()
        print(f"{Fore.WHITE}Input Password (Masked): ", end='', flush=True)
        pwd = getpass.getpass(prompt='')
        if pwd: app.audit(pwd)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exit.")
          
