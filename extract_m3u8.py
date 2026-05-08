import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_network_m3u8():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # สำคัญ: สั่งให้ Chrome เก็บ Log ของ Network ทั้งหมด
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://dookeela4.live/live-tv/axn"
    print(f"Opening: {url}")
    
    driver.get(url)
    
    # รอให้สตรีมมิ่งโหลดและสร้าง Token (ปรับเวลาได้ตามความเหมาะสม)
    time.sleep(90)

    # ดึง Log ออกมาจากท่อ Network
    logs = driver.get_log('performance')
    
    found_urls = []
    for entry in logs:
        log = json.loads(entry['message'])['message']
        # คัดกรองเฉพาะตอนที่ได้รับ Response กลับมา (เหมือนแถบ Network ใน F12)
        if log['method'] == 'Network.responseReceived':
            res_url = log['params']['response']['url']
            status = log['params']['response']['status']
            
            # กรองหา .m3u8 ที่สถานะเป็น 200
            if '.m3u8' in res_url and status == 200:
                found_urls.append(res_url)

    if found_urls:
        print("\n[+] Found m3u8 links in Network Tab:")
        for link in set(found_urls):
            print(link)
    else:
        print("[-] No m3u8 links found.")

    driver.quit()

if __name__ == "__main__":
    get_network_m3u8()
