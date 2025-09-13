import requests
import time

def main():
    start_time = time.time()
    
    # Test sync endpoints sequentially
    urls = [
        "http://localhost:8000/sync-delay/2",
        "http://localhost:8000/sync-delay/2",
        "http://localhost:8000/sync-delay/2"
    ]
    
    results = []
    for url in urls:
        start = time.time()
        response = requests.get(url)
        end = time.time()
        results.append({"url": url, "status": response.status_code, "time": end - start})
    
    for result in results:
        print(f"URL: {result['url']}, Time: {result['time']:.2f}s")
    
    total_time = time.time() - start_time
    print(f"Total time for {len(urls)} requests: {total_time:.2f}s")

if __name__ == "__main__":
    main()
