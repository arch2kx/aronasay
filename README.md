# Aronasay

*A CLI program featuring talking Arona from Blue Archive!*

[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-green)](https://www.python.org/)

---

## About

Aronasay is a CLI program like cowsay, but instead of a talking cow, it's Arona from Blue Archive! Make Arona say anything you want with various ASCII art versions to choose from. Perfect for adding some Blue Archive energy to your terminal!

Inspired by [Momoisay](https://github.com/Mon4sm/momoisay) by Mon4sm.

## Features

* Talking ASCII art of Arona
* Animated ASCII art of Arona
* Multiple versions to choose from
* Pipe-friendly (works with stdin)

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/yourusername/aronasay.git
cd aronasay
chmod +x install/install.sh
sudo ./install/install.sh
```

### Manual Installation

```bash
git clone https://github.com/yourusername/aronasay.git
cd aronasay
sudo cp src/aronasay.py /usr/local/bin/aronasay
sudo chmod +x /usr/local/bin/aronasay
```


## Usage

### Basic Usage

```bash
# Simple message
aronasay "Hello, Sensei!"

# Multi-line message
aronasay "Hello, Sensei!
Welcome to Kivotos!
Let's have fun!"

# Pipe from other commands
echo "Good morning!" | aronasay
fortune | aronasay
```

### Animated Mode

```bash
# Show animated Arona (default version 1)
aronasay -a

# Show specific animation version
aronasay -a 2

# See all available versions
aronasay -l
```

This is perfect for terminal eye candy or ricing your setup!

### Customization

```bash
# Custom speech bubble width
aronasay -w 60 "This is a wider speech bubble!"

# Combine with other tools
date | aronasay
```

## Examples

```bash
# Morning greeting
echo "Good morning, Sensei!" | aronasay

# Random fortune
fortune | aronasay

# Git commit message
git log -1 --pretty=%B | aronasay

# System info
uname -a | aronasay

# Current date and time
date | aronasay

# Add to your .bashrc or .zshrc for login greeting
echo "Welcome back, Sensei!" | aronasay
```


## File Structure

```
aronasay/
├── src/
│   ├── art/
│   │   └── arona_art.py      # ASCII art collection
│   └── aronasay.py            # Main program
├── install/
│   └── install.sh             # Installation script
├── README.md
└── LICENSE
```

## Options

```
usage: aronasay [-h] [-a [VERSION]] [-f] [-l] [-w WIDTH] [message ...]

positional arguments:
  message               The message for Arona to say

options:
  -h, --help            show this help message and exit
  -a [VERSION], --animate [VERSION]
                        Show animated Arona (optionally specify version, default: 1)
  -l, --list            List all available versions
  -w WIDTH, --width WIDTH
                        Width of the speech bubble (default: 40)
```

## Requirements

- Python 3.6 or higher
- No external dependencies! Pure Python stdlib

## Contributing

Contributions are welcome! Feel free to:
- Add new ASCII art versions of Arona
- Improve animations
- Fix bugs
- Enhance features

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Credits

- **Arona** character from [Blue Archive](https://bluearchive.nexon.com/) by Nexon
- Inspired by [Momoisay](https://github.com/Mon4sm/momoisay) by Mon4sm
- Original concept based on the classic `cowsay` program

## Related Projects

- [Momoisay](https://github.com/Mon4sm/momoisay) - Momoi version by Mon4sm (C)
- [cowsay](https://github.com/piuccio/cowsay) - The original talking cow

