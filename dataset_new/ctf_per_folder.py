#!/usr/bin/env python3
import os
import re
import time
from bs4 import BeautifulSoup
from curl_cffi import requests

OUTPUT_DIR = "writeups"
MIN_WRITEUP_ID = 25000   # Mốc đầu năm 2021
DELAY_PER_PAGE = 0.3

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[*] Bắt đầu cào writeup (ID >= {MIN_WRITEUP_ID}) -> thư mục = ID\n")

    page = 1
    total_saved = 0
    reach_end = False

    while not reach_end:
        url = f"https://ctftime.org/writeups?page={page}"
        try:
            resp = requests.get(url, impersonate="chrome", timeout=15)
        except Exception as e:
            print(f"[-] Lỗi kết nối trang {page}: {e}")
            break

        if resp.status_code != 200:
            print(f"[-] Dừng (Mã lỗi: {resp.status_code})")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table")
        if not table:
            print("[!] Hết dữ liệu.")
            break

        rows = table.find_all("tr")[1:]
        page_created = 0

        for row in rows:
            w_match = re.search(r'/writeup/(\d+)', str(row))
            if not w_match:
                continue

            w_id = int(w_match.group(1))

            if w_id < MIN_WRITEUP_ID:
                print(f"\n[✓] ID {w_id} < {MIN_WRITEUP_ID} (trước 2021). Dừng!")
                reach_end = True
                break

            # Tên thư mục = chính ID writeup
            item_dir = os.path.join(OUTPUT_DIR, str(w_id))
            if os.path.exists(item_dir):
                continue

            os.makedirs(item_dir, exist_ok=True)
            with open(os.path.join(item_dir, f"{w_id}.txt"), "w", encoding="utf-8") as f:
                f.write(f"https://ctftime.org/writeup/{w_id}\n")

            page_created += 1
            total_saved += 1

        print(f"[+] Trang {page:03d}: +{page_created:2d} thư mục | Tổng: {total_saved:,}")
        page += 1
        time.sleep(DELAY_PER_PAGE)

    print(f"\n[✓] XONG! Tổng: {total_saved:,} thư mục. Kiểm tra: ls {OUTPUT_DIR}/ | head")

if __name__ == "__main__":
    main()
