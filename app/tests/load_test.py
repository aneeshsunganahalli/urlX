import requests
import concurrent.futures
from collections import Counter

# Update this to the IP or domain where Nginx is listening
TARGET_URL = "http://localhost" 
TOTAL_REQUESTS = 1000
CONCURRENT_WORKERS = 10

def fetch_server_id():
    """Hits the endpoint and extracts the server_id from the JSON response."""
    try:
        response = requests.get(TARGET_URL, timeout=3)
        # Raise an error for bad HTTP status codes (4xx or 5xx)
        response.raise_for_status() 
        
        data = response.json()
        return str(data.get("workerID", "missing_id_in_response"))
        
    except requests.exceptions.RequestException as e:
        return f"Failed: {type(e).__name__}"

def run_test():
    print(f"Firing {TOTAL_REQUESTS} requests at {TARGET_URL}...")
    
    # Fire requests concurrently to mimic real-world load
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        # Schedule the requests
        futures = [executor.submit(fetch_server_id) for _ in range(TOTAL_REQUESTS)]
        
        # Wait for all requests to finish and collect results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
    # Count how many times each server responded
    distribution = Counter(results)
    
    print("\n--- Load Balancing Results ---")
    for server, count in distribution.items():
        percentage = (count / TOTAL_REQUESTS) * 100
        print(f"Backend [{server}]: {count} requests ({percentage:.1f}%)")

    # Basic Health Check
    unique_servers = [s for s in distribution.keys() if not s.startswith("Failed")]
    
    print("\n--- Summary ---")
    if len(unique_servers) > 1:
        print(f"✅ Load balancing is WORKING across {len(unique_servers)} servers.")
    elif len(unique_servers) == 1:
        print("⚠️ All traffic went to a SINGLE server. Nginx might only see one upstream.")
    else:
        print("❌ All requests failed. Is Nginx running?")

if __name__ == "__main__":
    run_test()