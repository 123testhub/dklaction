import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_axn_expert():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # 1. ปิดสัญลักษณ์ที่บ่งบอกว่าเป็น Selenium (สำคัญมากในการหลบหลีก)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 2. ใช้ User-Agent ให้เหมือนกับที่แสดงใน Kiwi ของคุณ
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
    
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 3. ลบค่า webdriver ใน JavaScript เพื่อไม่ให้เว็บรู้ว่าเป็นบอท
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    try:
        # ขั้นตอนตามที่คุณแนะนำ: เปิดหน้าหลักก่อน
        print("Step 1: Visiting main list...")
        driver.get("https://dookeela4.live/live-tv/")
        time.sleep(15) 

        # ขั้นตอนที่ 2: เข้าหน้า AXN
        print("Step 2: Entering AXN page...")
        driver.get("https://dookeela4.live/live-tv/axn")
        
        # รอให้ระบบสร้างท่อ Network เหมือนในภาพที่คุณส่งมา
        print("Step 3: Sniffing network (90s)...")
        time.sleep(90)

        logs = driver.get_log('performance')
        found = False
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.responseReceived':
                url = log['params']['response']['url']
                status = log['params']['response']['status']
                
                # ค้นหา chunks.m3u8 ที่สถานะ 200 ตามรูปยืนยัน
                if 'chunks.m3u8' in url and status == 200:
                    print(f"\n[✔️] SUCCESS! FOUND STREAM:\n{url}\n")
                    found = True
        
        if not found:
            print("\n[-] Still not found. The site might have updated its protection.")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_axn_expert()
