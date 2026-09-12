# CIPHER

Interactive toolkit for cryptography, encoding, and password generation.

A simple, clean and nice-looking terminal tool with a menu that lets you quickly hash text, encode/decode data, generate strong passwords, and perform basic text transformations.

---

## Features

### 1. Hash Generator
Supports popular algorithms:
- MD5
- SHA1
- SHA256
- SHA512
- BLAKE2b

Just enter any text and get all hashes in a clean table.

### 2. Encoder / Decoder
- Base64 (encode / decode)
- Hex (encode / decode)
- URL encode / decode

### 3. Password Generator
- Custom password length
- Option to include/exclude uppercase letters, digits and special symbols
- Automatic strength evaluation (Weak / Medium / Strong)

### 4. Text Transform
- Reverse string
- Uppercase
- Lowercase
- ROT13
- Remove spaces

---

## Installation

You only need the `rich` library:

```bash
pip install rich
```

---

## Usage

```bash
python3 cipher.py
```

After launching, you’ll see the main menu. Navigation is done with numbers.

---

## How to use

1. Run the script
2. Select the desired menu option (1–4)
3. Follow the on-screen prompts
4. After getting the result, press Enter to return to the menu
5. To exit, select `0`

---

## Menu Structure

```
1  Hash Generator
2  Encoder / Decoder
3  Password Generator
4  Text Transform
0  Exit
```

---

## Examples

**Password generation:**
- Select option 3
- Enter desired length (e.g. 18)
- Choose whether to include uppercase, digits and symbols
- Get a generated password + strength rating

**Hashing:**
- Select option 1
- Enter any text
- Instantly see all major hashes

---

## Requirements

- Python 3.8 or newer
- `rich` library

---

## Note

This tool was created for convenience, learning and everyday tasks. Use it responsibly.
