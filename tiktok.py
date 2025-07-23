import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class TikTokViewBot:
    TOOL_API_URL = "https://buf-view-tiktok-ayacte.vercel.app/tiktokview"
    MAX_WORKERS = 1000

    def __init__(self, urls):
        self.urls = urls

    def _send_request(self, url):
        try:
            response = requests.get(
                self.TOOL_API_URL,
                params={"video": url},
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
