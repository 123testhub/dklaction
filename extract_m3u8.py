import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_stream():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # เลียนแบบ User-Agent ของคนใช้จริงๆ
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # ขั้นตอนที่ 1: เปิดหน้าหลักก่อน (เหมือนที่คุณทำบน PC)
        print("Step 1: Opening main page...")
        driver.get("https://dookeela4.live/live-tv/")
        time.sleep(10) # รอให้หน้าหลักโหลด Cookies สักครู่

        # ขั้นตอนที่ 2: ไปหน้าช่อง TSP3
        print("Step 2: Moving to TSP3 page...")
        driver.get("https://dookeela4.live/live-tv/tsp3")
        
        # ขั้นตอนที่ 3: ดักฟังท่อ Network (รอ 60-90 วินาทีตามที่คุณตั้งไว้)
        print("Step 3: Sniffing Network Traffic for 90 seconds...")
        time.sleep(90)

        logs = driver.get_log('performance')
        found = False
        
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                status = log['params']['response']['status']
                
                # ดักทุกอย่างที่เป็น m3u8 และมีสถานะ 200
                if '.m3u8' in url and status == 200:
                    print(f"\n[!!!] FOUND STREAM (Status 200):\n{url}\n")
                    found = True
        
        if not found:
            print("\n[-] No m3u8 links found. Maybe need more wait time or the stream is down.")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_stream()
