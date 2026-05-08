import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_capture_axn():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # ใช้ User-Agent ตามรูปที่คุณส่งมา
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Step 1: Visiting main site...")
        driver.get("https://dookeela4.live/live-tv/")
        time.sleep(10)

        print("Step 2: Visiting AXN...")
        driver.get("https://dookeela4.live/live-tv/axn")
        
        print("Step 3: Waiting for stream to load (90s)...")
        time.sleep(90)

        logs = driver.get_log('performance')
        found = False
        
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                status = log['params']['response']['status']
                
                # ตรวจสอบ chunks หรือ playlist และสถานะ 200
                if ('chunks.m3u8' in url or 'playlist.m3u8' in url) and status == 200:
                    print(f"\n[!!!] SUCCESS! FOUND M3U8 LINK:")
                    print(f"URL: {url}")
                    print(f"Status Code: {status}\n")
                    found = True
        
        if not found:
            print("[-] No m3u8 found. WARP IP might still be blocked.")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_capture_axn()
