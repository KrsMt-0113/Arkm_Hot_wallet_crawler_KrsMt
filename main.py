# 2025.7.24
# version: 2.0
# 自行获取cURL存入curl.txt即可。
# num不建议超过1500，后续可加入翻页(offset)方法

import re
import time
import requests
import csv
import os
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # macOS / Linux
    title = "========= Arkham Entity Hot Wallet Crawler @ KrsMt. =========\n"
    print(title)

def parse_curl(curl_text):
    headers = dict(re.findall(r"-H\s+'([^:]+):\s*(.*?)'", curl_text))

    cookie_match = re.search(r"-b\s+'([^']+)'", curl_text)
    cookie_str = cookie_match.group(1) if cookie_match else headers.pop('cookie', headers.pop('Cookie', ''))

    cookies = {}
    if cookie_str:
        for pair in cookie_str.split('; '):
            if '=' in pair:
                k, v = pair.split('=', 1)
                cookies[k] = v

    return headers, cookies

def extract_hot_wallet(addr_info, target, name):
    if (
        addr_info.get('arkhamEntity', {}).get('name') == name and
        addr_info.get('arkhamLabel', {}).get('name') == 'Hot Wallet'
    ):
        address = addr_info['address']
        chain = addr_info.get('chain')
        label = addr_info['arkhamLabel']['name']
        arkm_url = f"https://intel.arkm.com/{address}"

        key = f"{address}@{chain}"
        target[key] = {
            'chain': chain,
            'address': address,
            'arkm_url': arkm_url,
            'label': label
        }

with open("curl.txt", "r", encoding="utf-8") as f:
    curl_text = f.read()

headers, cookies = parse_curl(curl_text)

clear_console()
Entity = input('Entity:')
entity = input('entity:')
num = input('num:')
clear_console()

Chain = [
    'bitcoin',
    'ethereum',
    'solana',
    'tron',
    'bsc',
    'arbitrum_one',
    'ton',
    'polygon',
    'dogecoin',
    'base',
    'sonic',
    'optimism',
    'mantle',
    'avalanche',
    'linea',
    'blast',
    'manta',
    'flare'
]

def fetch_chain_data(chain, entity, num, headers, cookies, Entity):
    url = f'https://api.arkm.com/transfers?base={entity}&flow=out&usdGte=1&sortKey=time&sortDir=desc&limit={num}&offset=0&tokens=&chains={chain}'
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=100)
        data = response.json()
        partial_result = {}
        if data.get('transfers') is not None:
            for tx in data['transfers']:
                extract_hot_wallet(tx.get('fromAddress', {}), partial_result, Entity)
        return partial_result
    except Exception as e:
        print(f"Error fetching data for {chain}: {e}")
        return {}

result = {}

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_chain_data, chain, entity, num, headers, cookies, Entity): chain for chain in Chain}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Chains", ncols= 80):
        partial = future.result()
        result.update(partial)

result = list(result.values())

time.sleep(1)
clear_console()

with open(f"{Entity}.csv", mode="w", encoding="utf-8", newline="") as file:
    fieldnames = ['chain', 'address', 'arkm_url', 'label']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(result)
    print(f"结果已保存为{Entity}.csv")