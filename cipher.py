#!/usr/bin/env python3
"""
CIPHER — Interactive Crypto & Encoding Toolkit
"""

import os
import sys
import hashlib
import base64
import binascii
import secrets
import string
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich import box

console = Console(highlight=False)

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    clear()
    logo = Text()
    logo.append("\n  ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ \n", style="bold red")
    logo.append("  ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗\n", style="bold red")
    logo.append("  ██║     ██║██████╔╝███████║█████╗  ██████╔╝\n", style="bold red")
    logo.append("  ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗\n", style="bold red")
    logo.append("  ╚██████╗██║██║     ██║  ██║███████╗██║  ██║\n", style="bold red")
    logo.append("  ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\n", style="bold red")
    logo.append("\n  CRYPTO • HASH • ENCODING • PASSWORDS\n", style="bold white")
    console.print(logo)
    console.print(Panel(
        Align.center("[bold red]INTERACTIVE TOOLKIT[/bold red]"),
        style="red",
        box=box.HEAVY
    ))

def pause():
    console.print()
    Prompt.ask("[dim]press enter to return[/dim]", default="")

def hash_menu():
    banner()
    console.print("\n[bold red]HASH GENERATOR[/bold red]\n")
    
    text = Prompt.ask("[cyan]Text to hash[/cyan]")
    
    table = Table(box=box.SIMPLE_HEAVY, border_style="red")
    table.add_column("Algorithm", style="cyan", width=12)
    table.add_column("Hash", style="white")
    
    table.add_row("MD5", hashlib.md5(text.encode()).hexdigest())
    table.add_row("SHA1", hashlib.sha1(text.encode()).hexdigest())
    table.add_row("SHA256", hashlib.sha256(text.encode()).hexdigest())
    table.add_row("SHA512", hashlib.sha512(text.encode()).hexdigest())
    table.add_row("BLAKE2b", hashlib.blake2b(text.encode()).hexdigest())
    
    console.print(table)
    pause()

def encode_menu():
    banner()
    console.print("\n[bold red]ENCODER / DECODER[/bold red]\n")
    console.print("  1. Base64 Encode")
    console.print("  2. Base64 Decode")
    console.print("  3. Hex Encode")
    console.print("  4. Hex Decode")
    console.print("  5. URL Encode")
    console.print("  6. URL Decode")
    console.print()

    choice = Prompt.ask("[bold red]select[/bold red]", choices=["1","2","3","4","5","6"])
    text = Prompt.ask("\n[cyan]Input[/cyan]")

    try:
        if choice == "1":
            result = base64.b64encode(text.encode()).decode()
        elif choice == "2":
            result = base64.b64decode(text.encode()).decode()
        elif choice == "3":
            result = binascii.hexlify(text.encode()).decode()
        elif choice == "4":
            result = binascii.unhexlify(text.encode()).decode()
        elif choice == "5":
            import urllib.parse
            result = urllib.parse.quote(text)
        elif choice == "6":
            import urllib.parse
            result = urllib.parse.unquote(text)
        
        console.print(f"\n[bold green]Result:[/bold green]\n{result}")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
    
    pause()

def password_menu():
    banner()
    console.print("\n[bold red]PASSWORD GENERATOR[/bold red]\n")
    
    length = IntPrompt.ask("[cyan]Length[/cyan]", default=16)
    use_upper = Prompt.ask("Uppercase letters? (y/n)", choices=["y", "n"], default="y") == "y"
    use_digits = Prompt.ask("Digits? (y/n)", choices=["y", "n"], default="y") == "y"
    use_symbols = Prompt.ask("Symbols? (y/n)", choices=["y", "n"], default="y") == "y"

    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{}<>?"

    password = ''.join(secrets.choice(chars) for _ in range(length))
    
    console.print(f"\n[bold green]Generated Password:[/bold green]\n")
    console.print(Panel(password, style="bold green", box=box.HEAVY))
    
    # Простая оценка
    strength = "Weak"
    if length >= 12 and use_upper and use_digits and use_symbols:
        strength = "Strong"
    elif length >= 10:
        strength = "Medium"
    
    console.print(f"\n[cyan]Strength:[/cyan] [bold]{strength}[/bold]")
    pause()

def transform_menu():
    banner()
    console.print("\n[bold red]TEXT TRANSFORM[/bold red]\n")
    console.print("  1. Reverse")
    console.print("  2. Uppercase")
    console.print("  3. Lowercase")
    console.print("  4. ROT13")
    console.print("  5. Remove spaces")
    console.print()

    choice = Prompt.ask("[bold red]select[/bold red]", choices=["1","2","3","4","5"])
    text = Prompt.ask("\n[cyan]Input[/cyan]")

    if choice == "1":
        result = text[::-1]
    elif choice == "2":
        result = text.upper()
    elif choice == "3":
        result = text.lower()
    elif choice == "4":
        result = text.translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
        ))
    elif choice == "5":
        result = text.replace(" ", "")

    console.print(f"\n[bold green]Result:[/bold green]\n{result}")
    pause()

def main_menu():
    while True:
        banner()
        console.print("\n[bold red]MAIN MENU[/bold red]")
        console.print("[red]────────────────────────[/red]")
        console.print("  [cyan]1[/cyan]  Hash Generator")
        console.print("  [cyan]2[/cyan]  Encoder / Decoder")
        console.print("  [cyan]3[/cyan]  Password Generator")
        console.print("  [cyan]4[/cyan]  Text Transform")
        console.print("  [cyan]0[/cyan]  Exit")
        console.print()

        choice = Prompt.ask("[bold red]select[/bold red]", choices=["0","1","2","3","4"], default="1")

        if choice == "0":
            console.print("\n[bold red][[ SESSION CLOSED ]][/bold red]\n")
            break
        elif choice == "1":
            hash_menu()
        elif choice == "2":
            encode_menu()
        elif choice == "3":
            password_menu()
        elif choice == "4":
            transform_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red][[ TERMINATED ]][/bold red]\n")
