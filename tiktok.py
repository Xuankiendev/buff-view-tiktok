import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class TikTokViewBot:
    TOOL_API_URL = "https://buf-view-tiktok-ayacte.vercel.app/tiktokview"
    MAX_WORKERS = 500

    def __init__(self, urls):
        self.urls = urls

    def _send_request(self, url):
        try:
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Referer": "https://buf-view-tiktok-ayacte.vercel.app/tiktokview",
                "Sec-Ch-Ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Linux"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            }
            cookies = {
                "_vcrcs": "1.17532602183.3600.ZjhkMzg5M...f9f253f4eda4036d29c89a6936d17f71"
            }
            response = requests.get(
                self.TOOL_API_URL,
                params={"video": url},
                headers=headers,
                cookies=cookies,
                timeout=30
            )
            if response.status_code == 200 and response.json().get("sent_success", 0) > 0:
                return True
        except:
            pass
        return False

    def _process_batch(self, url, batch_size):
        success, fail = 0, 0
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            futures = [executor.submit(self._send_request, url) for _ in range(batch_size)]
            for future in as_completed(futures):
                if future.result():
                    success += 1
                else:
                    fail += 1
        return success, fail

    def run(self, batch_size=1000, delay=5):
        while True:
            for url in self.urls:
                success, fail = self._process_batch(url, batch_size)
                print(f"URL: {url}\nThành công: {success} | Thất bại: {fail}\n")
            time.sleep(delay)

def load_urls(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip().startswith("http")]
    except:
        return []

if __name__ == "__main__":
    urls = load_urls("links.txt")
    if not urls:
        print("Không tìm thấy link hợp lệ trong links.txt")
    else:
        bot = TikTokViewBot(urls)
        bot.run()
