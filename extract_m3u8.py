import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_axn_stream():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # ปลอมตัวเป็น Browser ปกติเพื่อไม่ให้โดนบล็อก
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 1. เข้าหน้าหลักก่อนเพื่อรับ Cookies/Session (เหมือนตอนคุณเปิด F12 รอ)
        print("Step 1: Visiting main site...")
        driver.get("https://dookeela4.live/live-tv/")
        time.sleep(10) 

        # 2. เข้าหน้าช่อง AXN ที่คุณต้องการ
        print("Step 2: Accessing AXN stream page...")
        driver.get("https://dookeela4.live/live-tv/axn")
        
        # 3. รอให้วิดีโอโหลดและสร้างลิงก์ในท่อ Network (90 วินาทีตามที่คุณต้องการ)
        print("Step 3: Sniffing network for 90 seconds. Please wait...")
        time.sleep(90)

        logs = driver.get_log('performance')
        found_links = []
        
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                status = log['params']['response']['status']
                
                # กรองเอาเฉพาะ .m3u8 ที่มีสถานะ 200 OK
                if '.m3u8' in url and status == 200:
                    # ป้องกันการพิมพ์ลิงก์ซ้ำ
                    if url not in found_links:
                        print(f"\n[✔️] FOUND AXN STREAM (Status 200):\n{url}\n")
                        found_links.append(url)
        
        if not found_links:
            print("\n[-] No m3u8 links with Status 200 found. Check if the site is still up.")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_axn_stream()
