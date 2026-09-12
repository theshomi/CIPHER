#!/usr/bin/env python3
"""
CIPHER — Interactive Crypto & Encoding Toolkit
+ Hash Cracker (dictionary + simple brute)
"""

import os
import sys
import hashlib
import base64
import binascii
import secrets
import string
import itertools
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich import box

console = Console(highlight=False)

# Небольшая встроенная база частых паролей
DEFAULT_WORDLIST = [
    "123456", "password", "123456789", "12345678", "12345", "qwerty", "abc123",
    "password1", "1234567", "1234567890", "123123", "admin", "letmein", "welcome",
    "monkey", "login", "princess", "dragon", "master", "hello", "freedom", "whatever",
    "qazwsx", "trustno1", "jordan", "harley", "hunter", "buster", "thomas", "tigger",
    "robert", "soccer", "batman", "test", "pass", "passw0rd", "1q2w3e4r", "lovely",
    "shadow", "michael", "jennifer", "jordan23", "superman", "123qwe", "qwerty123",
    "1qaz2wsx", "qwertyuiop", "asdfgh", "zxcvbnm", "111111", "000000", "aaaaaa",
    "password123", "admin123", "root", "toor", "guest", "user", "test123", "love",
    "iloveyou", "sunshine", "princess1", "football", "charlie", "aa123456", "donald",
    "password!", "qwe123", "123456a", "666666", "121212", "1234", "123", "letmein1"
]

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
    logo.append("\n  CRYPTO • HASH • ENCODING • CRACKER\n", style="bold white")
    console.print(logo)
    console.print(Panel(
        Align.center("[bold red]INTERACTIVE TOOLKIT[/bold red]"),
        style="red",
        box=box.HEAVY
    ))

def pause():
    console.print()
    Prompt.ask("[dim]press enter to return[/dim]", default="")

def get_hash_function(name: str):
    name = name.lower()
    if name == "md5":
        return hashlib.md5
    elif name == "sha1":
        return hashlib.sha1
    elif name == "sha256":
        return hashlib.sha256
    elif name == "sha512":
        return hashlib.sha512
    elif name == "blake2b":
        return hashlib.blake2b
    return None

def detect_hash_type(h: str):
    h = h.lower().strip()
    length = len(h)
    if length == 32:
        return "md5"
    elif length == 40:
        return "sha1"
    elif length == 64:
        return "sha256"
    elif length == 128:
        return "sha512"
    return None

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
    
    strength = "Weak"
    if length >= 14 and use_upper and use_digits and use_symbols:
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

def load_wordlist(path: str | None) -> list[str]:
    if path and os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                words = [line.strip() for line in f if line.strip()]
            console.print(f"[green]Loaded {len(words)} words from {path}[/green]")
            return words
        except Exception as e:
            console.print(f"[red]Failed to load wordlist: {e}[/red]")
    
    console.print(f"[yellow]Using built-in wordlist ({len(DEFAULT_WORDLIST)} words)[/yellow]")
    return DEFAULT_WORDLIST.copy()

def crack_hash(target_hash: str, algo: str, wordlist: list[str]) -> str | None:
    func = get_hash_function(algo)
    if not func:
        return None

    target_hash = target_hash.lower().strip()
    found = None

    with Progress(
        SpinnerColumn(style="red"),
        TextColumn("[bold red]Cracking..."),
        BarColumn(bar_width=40, style="red", complete_style="green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        task = progress.add_task("crack", total=len(wordlist))

        def check(word: str):
            if func(word.encode()).hexdigest() == target_hash:
                return word
            return None

        # Многопоточный перебор
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(check, word): word for word in wordlist}
            for future in as_completed(futures):
                progress.advance(task)
                result = future.result()
                if result:
                    found = result
                    # Отменяем остальные
                    for f in futures:
                        f.cancel()
                    break

    return found

def simple_brute(target_hash: str, algo: str, max_length: int = 4) -> str | None:
    """Простой брутфорс только для очень коротких паролей (до 4 символов)"""
    func = get_hash_function(algo)
    if not func:
        return None

    target_hash = target_hash.lower().strip()
    charset = string.ascii_lowercase + string.digits

    console.print(f"[yellow]Starting brute-force (length 1-{max_length})... This can take time.[/yellow]")

    for length in range(1, max_length + 1):
        total = len(charset) ** length
        with Progress(
            SpinnerColumn(style="red"),
            TextColumn(f"[bold red]Brute length {length}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("brute", total=total)

            for combo in itertools.product(charset, repeat=length):
                word = "".join(combo)
                if func(word.encode()).hexdigest() == target_hash:
                    return word
                progress.advance(task)

    return None

def cracker_menu():
    banner()
    console.print("\n[bold red]HASH CRACKER[/bold red]")
    console.print("[dim]Dictionary attack + optional short brute-force[/dim]\n")

    target_hash = Prompt.ask("[cyan]Enter hash[/cyan]").strip()
    if not target_hash:
        console.print("[red]No hash provided[/red]")
        pause()
        return

    # Автоопределение типа
    detected = detect_hash_type(target_hash)
    if detected:
        console.print(f"[green]Detected hash type: {detected.upper()}[/green]")
        algo = detected
    else:
        console.print("[yellow]Could not auto-detect hash type[/yellow]")
        algo = Prompt.ask(
            "Choose algorithm",
            choices=["md5", "sha1", "sha256", "sha512", "blake2b"],
            default="md5"
        )

    console.print("\n[bold]Wordlist options:[/bold]")
    console.print("  1. Use built-in wordlist (fast)")
    console.print("  2. Load external wordlist (recommended)")
    wl_choice = Prompt.ask("Select", choices=["1", "2"], default="1")

    wordlist = []
    if wl_choice == "2":
        path = Prompt.ask("[cyan]Path to wordlist[/cyan]", default="wordlist.txt")
        wordlist = load_wordlist(path)
    else:
        wordlist = load_wordlist(None)

    # Добавляем простые мутации
    if Confirm.ask("Apply simple mutations? (capitalize, add numbers)", default=True):
        mutated = set(wordlist)
        for w in wordlist:
            mutated.add(w.capitalize())
            mutated.add(w.upper())
            mutated.add(w + "1")
            mutated.add(w + "123")
            mutated.add(w + "!")
            mutated.add(w + "2023")
            mutated.add(w + "2024")
            mutated.add(w + "2025")
        wordlist = list(mutated)
        console.print(f"[green]Wordlist expanded to {len(wordlist)} candidates[/green]")

    console.print()
    start = time.time()
    result = crack_hash(target_hash, algo, wordlist)
    elapsed = time.time() - start

    if result:
        console.print(Panel(
            f"[bold green]CRACKED[/bold green]\n\nPassword: [bold white]{result}[/bold white]\nTime: {elapsed:.2f}s",
            style="green",
            box=box.HEAVY
        ))
    else:
        console.print(f"\n[red]Not found in wordlist ({elapsed:.2f}s)[/red]")

        if Confirm.ask("\nTry short brute-force (length 1-4)?", default=False):
            brute_result = simple_brute(target_hash, algo, max_length=4)
            if brute_result:
                console.print(Panel(
                    f"[bold green]CRACKED BY BRUTE[/bold green]\n\nPassword: [bold white]{brute_result}[/bold white]",
                    style="green",
                    box=box.HEAVY
                ))
            else:
                console.print("[red]Brute-force failed. Password is probably longer/complex.[/red]")

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
        console.print("  [cyan]5[/cyan]  Hash Cracker")
        console.print("  [cyan]0[/cyan]  Exit")
        console.print()

        choice = Prompt.ask("[bold red]select[/bold red]", choices=["0","1","2","3","4","5"], default="1")

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
        elif choice == "5":
            cracker_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red][[ TERMINATED ]][/bold red]\n")
