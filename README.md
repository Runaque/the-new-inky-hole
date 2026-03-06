# the-new-inky-hole 🚀

## Modernized eInk Display for Pi-hole v6

A 50% leaner, high-performance refactor of the classic Inky-Pihole script. Optimized for Pi-hole v6, Python 3.10+, and mobile battery-powered setups.

Default display / Simple display (using `--simple` option):  
<img src='https://github.com/Runaque/the-new-inky-hole/blob/main/preview.jpg?raw=true?v=1' width="300"/> 
<img src='https://github.com/Runaque/the-new-inky-hole/blob/main/preview_simple.jpg?v=1' width="300"/>


LCARS display (using `--lcars` option) / LCARS + Simple:  
<img src='https://github.com/Runaque/the-new-inky-hole/blob/main/preview_lcars.jpg?v=1' width="300"/> 
<img src='https://github.com/Runaque/the-new-inky-hole/blob/main//preview_lcars_simple.jpg?v=1' width="300"/>

## ✨ Why "the-new-inky-hole"?

The original project was a fantastic foundation, but Pi-hole v6 introduced major API changes and modern Python environments (like PEP 668) required a new approach.

Refactored Logic: Reduced the codebase from 203 lines to just 98 lines.

Modern REST API: Switched to the v6-native REST API. Unlike v5, no API token is required for standard statistics on most v6 installs.

Better Performance: Removed legacy dependencies like distutils and optimized font rendering for the Pi Zero 2W's CPU.

## 🛠️ Verified Hardware Setup

Raspberry Pi: Pi Zero 2W.

Display: Pimoroni Inky pHAT (Red/Black/White).

Power: Geekworm X306 UPS Shield + LiitoKala 18650 3500mAh battery.

Runtime: ~8–10 hours on battery with 5-minute refreshes.

## 📂 Project Structure

For the script to run correctly, ensure your repository contains these individual files:

main.py - The optimized 98-line script.

requirements.txt - Python dependencies.

background.png / lcars_black_red.png - Assets.

Signika-Bold.ttf / Signika-Light.ttf - Fonts.

## 📦 Installation

Virtual Environment: (Recommended for Raspberry Pi OS Bookworm+)

```
python -m venv ~/myvenv
source ~/myvenv/bin/activate
```

Install Requirements:

```
pip install -r requirements.txt
```

Clone & Setup:

```
git clone https://github.com/Runaque/the-new-inky-hole.git
cd the-new-inky-hole
```

Test your setup

```
python main.py -r --tz Europe/Brussels
```

## ⚙️ Options

--tz : Set your local TimeZone (e.g., Europe/Brussels, America/New_York, UTC).

-r, --rotate : Rotates the display 180 degrees.

--lcars : Enables the Star Trek inspired console layout.

-a, --apihosts : Comma separated list of Pi-Hole IPs (Defaults to 127.0.0.1).

-t, --token : Legacy/Optional. Only required in v6 if you have specifically configured a password-protected API.

## ⏰ Automatic Updates (Crontab)

To update every 5 minutes, add this to crontab -e:

```
*/5 * * * * /home/pi/myvenv/bin/python /home/pi/the-new-inky-hole/main.py -r --tz Europe/Brussels > /dev/null 2>&1
```

## 📜 Credits & Attribution

This project is a refactored fork of the original inky-pihole created by doublehelix21.

Original Maker: doublehelix21

Original Repository: hxxps://github.com/doublehelix/inky-pihole/

The-new-inky-hole aims to keep the original aesthetic alive while bringing the backend up to date for Pi-hole v6.
