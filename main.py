import argparse
import json
import os
import pytz
from datetime import datetime
from urllib.request import urlopen, Request
from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--apihosts', help='API host names')
parser.add_argument('-r', '--rotate', action='store_true', help='Rotate 180 deg')
parser.add_argument('-s', '--simple', action='store_true', help='Simple mode')
parser.add_argument('--lcars', action='store_true', help='LCARS mode')
parser.add_argument('--tz', help='Timezone (e.g., Europe/Brussels)')
parser.add_argument('-t', '--token', help='v6 token')
args = parser.parse_args()

display = auto()
WHITE, BLACK, RED = display.WHITE, display.BLACK, display.RED
if args.lcars: BLACK, RED = display.WHITE, display.WHITE

tzLocal = pytz.timezone(args.tz or 'UTC')
now = datetime.now(tzLocal)
font = ImageFont.truetype('./Signika-Bold.ttf', 22)
smallfont = ImageFont.truetype('./Signika-Light.ttf', 14)

data = {'clients': 0, 'domains': 0, 'queries': 0, 'blocked': 0}

def get_data(host):
    try:
        url = f'http://{host}/api/stats/summary'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            res = json.loads(response.read())
        
        c, d = res['clients']['active'], res['gravity']['domains_being_blocked']
        data['clients'] = max(data['clients'], c)
        data['domains'] = max(d, data['domains'])
        data['queries'] += res['queries']['total']
        data['blocked'] += res['queries']['blocked']
    except Exception as e:
        print(f"API Error: {e}")

def draw_t(pos, pre, txt, suf, col):
    bg = display.WHITE if args.lcars else display.BLACK
    w, h = pos
    if pre:
        draw.text((w, h+6), pre, bg, smallfont)
        w += smallfont.getlength(pre) + 4
    if txt:
        draw.text((w, h), txt, col, font)
        w += font.getlength(txt) + 4
    if suf:
        draw.text((w, h+6), suf, bg, smallfont)

for h_item in (args.apihosts or "127.0.0.1").split(","):
    get_data(h_item.split(":")[0])

total = data['queries']
ratio = "{:.1f}".format((data['blocked'] / total * 100) if total > 0 else 0)
b_full = f"{data['blocked']:,} ({ratio}%)"

img_p = "./lcars_black_red.png" if args.lcars else "./background.png"
display.set_border(display.BLACK if args.lcars else display.WHITE)
try:
    img = Image.open(img_p)
except:
    img = Image.new("P", (display.WIDTH, display.HEIGHT), display.WHITE)
draw = ImageDraw.Draw(img)

x = 60 if args.lcars else 10
c_m = WHITE if args.lcars else BLACK
draw_t((x, 5 if args.lcars else -3), now.strftime("%b-%d %H:%M"), "", "- blocked:", c_m)
draw_t((x, 24 if args.lcars else 19), "", b_full, "", RED)
draw_t((x, 46 if args.lcars else 42), "of", f"{total:,}", "requests", c_m)
draw_t((x, 68 if args.lcars else 75), "protecting", f"{data['clients']:,}", "clients", c_m)
draw_t((x, 88 if args.lcars else 95), "@", f"{data['domains']:,}", "domains", c_m)

if args.rotate: img = img.rotate(180)
display.set_image(img)
display.show()