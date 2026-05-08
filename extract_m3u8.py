import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_tsp3_step_by_step():
    options = Options()
    options.add_argument("--headless") # GitHub ต้องรันแบบไม่มีหน้าจอ
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # ปลอมตัวเป็น Chrome PC เพื่อให้เว็บยอมปล่อย Status 200
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # ขั้นตอนที่ 1: เปิดหน้าหลัก (เหมือนที่คุณกด F12 รอไว้)
        print("Step 1: Opening main list page...")
        driver.get("https://dookeela4.live/live-tv/")
        time.sleep(10) # รอให้ Session ทำงาน

        # ขั้นตอนที่ 2: เปิดหน้าช่องเป้าหมาย (TSP3)
        print("Step 2: Navigating to TSP3...")
        driver.get("https://dookeela4.live/live-tv/tsp3")
        
        # ขั้นตอนที่ 3: ดักฟังท่อ Network (รอให้สตรีมเริ่มโหลด)
        print("Step 3: Sniffing network for 60 seconds...")
        time.sleep(60)

        logs = driver.get_log('performance')
        found_any = False

        for entry in logs:
            log = json.loads(entry['message'])['message']
            # เช็คเฉพาะตอนที่ได้รับ Response จากเซิร์ฟเวอร์
            if log['method'] == 'Network.responseReceived':
                res_url = log['params']['response']['url']
                status = log['params']['response']['status']
                
                # เช็คคำสำคัญตามที่คุณระบุ: chunks หรือ playlist และต้อง Status 200
                if ('chunks.m3u8' in res_url or 'playlist.m3u8' in res_url) and status == 200:
                    print("-" * 30)
                    print(f"[FOUND] Status: {status}")
                    print(f"URL: {res_url}")
                    print("-" * 30)
                    found_any = True
        
        if not found_any:
            print("[-] No matching m3u8 found with Status 200.")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_tsp3_step_by_step()
