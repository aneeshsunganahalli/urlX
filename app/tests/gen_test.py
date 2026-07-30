import time
from datetime import datetime
import urllib.request
import urllib.error



ENDPOINT = "http://localhost:8000/url/generate"
DELAY_BETWEEN_REQUESTS = 0.05  # 200 requests per second

print(f"Starting GET loop against {ENDPOINT}...")
print("Press Ctrl+C to stop.\n")

req_counter = 1

try:
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        try:
            # Default is GET request
            req = urllib.request.Request(ENDPOINT)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                result = response.read().decode('utf-8').strip()
                print(f"[{timestamp}] Req #{req_counter:04d} -> Response: {result}")
                
        except urllib.error.HTTPError as e:
            print(f"[{timestamp}] Req #{req_counter:04d} -> HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            print(f"[{timestamp}] Req #{req_counter:04d} -> Connection Error: {e.reason}")
            
        req_counter += 1
        time.sleep(DELAY_BETWEEN_REQUESTS)

except KeyboardInterrupt:
    print("\nTest stopped by user.")