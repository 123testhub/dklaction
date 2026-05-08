import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_axn_manual_logic():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # ปลอม User-Agent ให้เหมือน Chrome PC
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 1. ทำตามที่คุณบอก: เปิดหน้าหลักก่อน (จำลองการเปิด F12 รอ)
        print("Step 1: Opening https://dookeela4.live/live-tv/")
        driver.get("https://dookeela4.live/live-tv/")
        time.sleep(10) 

        # 2. เปิดหน้า AXN ตามที่คุณต้องการ
        print("Step 2: Opening https://dookeela4.live/live-tv/axn")
        driver.get("https://dookeela4.live/live-tv/axn")
        
        # 3. ดักฟังท่อ Network (รอ 60 วินาทีเพื่อให้สถานะ 200 ปรากฏ)
        print("Step 3: Sniffing network for AXN stream...")
        time.sleep(60)

        logs = driver.get_log('performance')
        found_any = False

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                res_url = log['params']['response']['url']
                status = log['params']['response']['status']
                
                # เช็ค chunks หรือ playlist และต้อง Status 200
                if ('chunks.m3u8' in res_url or 'playlist.m3u8' in res_url) and status == 200:
                    print("\n" + "="*50)
                    print(f"[FOUND AXN] Status: {status}")
                    print(f"URL: {res_url}")
                    print("="*50 + "\n")
                    found_any = True
        
        if not found_any:
            print("[-] No AXN m3u8 found. The server might be blocking GitHub's IP.")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_axn_manual_logic()
