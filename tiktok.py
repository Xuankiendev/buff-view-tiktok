import time
import httpx
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class TikTokViewBot:
    TOOL_API_URL = "https://buf-view-tiktok-ayacte.vercel.app/tiktokview"
    MAX_WORKERS = 500

    def __init__(self, urls, proxies=None):
        self.urls = urls
        self.proxies = proxies

    def _random_headers(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Connection": "keep-alive",
        }

    def _send_request(self, url):
        proxy = random.choice(self.proxies) if self.proxies else None
        proxies = {
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}",
        } if proxy else None

        try:
            with httpx.Client(http2=True, proxies=proxies, timeout=30) as client:
                response = client.get(
                    self.TOOL_API_URL,
                    headers=self._random_headers(),
                    params={"video": url, "time": int(time.time())},
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

    def run(self, batch_size=100, delay=5):
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

def load_proxies(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

if __name__ == "__main__":
    urls = load_urls("links.txt")
    proxies = load_proxies("proxy.txt")
    if not urls:
        print("Không tìm thấy link hợp lệ trong links.txt")
    else:
        bot = TikTokViewBot(urls, proxies)
        bot.run()
