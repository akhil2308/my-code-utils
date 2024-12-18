import asyncio
import httpx
import os
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
# from retry import retry

# Set max_batch_size from environment variable or default to 5
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", 5))

# Retry logic with tenacity
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_exception_type(Exception))
async def fetch(url, data):
    headers = {
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise error for bad status codes
        return response.json()  # Return JSON response

# Function to process API calls in batches
async def process_in_batches(urls, data):
    final_res = []
    
    # Divide the URLs into batches of size MAX_BATCH_SIZE
    for i in range(0, len(urls), MAX_BATCH_SIZE):
        batch = urls[i:i + MAX_BATCH_SIZE]
        print(f"Processing batch: {batch}")
        
        # Fetch all URLs in the current batch concurrently
        batch_results = await asyncio.gather(*[fetch(url, data) for url in batch])
        
        # Append the batch results to the final result
        final_res.extend(batch_results)
    
    return final_res

# Example usage
async def main():
    # Example API URL
    url = "http://localhost"
    
    # Sample data payload (replace with actual audio data)
    data = {}
    
    # Call the API
    final_res = await process_in_batches([url]*4, data)
    print("Final Result:", final_res)
    print("Final Result:", len(final_res))

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
