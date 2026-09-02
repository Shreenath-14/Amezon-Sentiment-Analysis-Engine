import requests
import re
from bs4 import BeautifulSoup
import os
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_product_details(amazon_url):
    # 1. Define your browser fingerprint
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    try:
        # 2. Execute the secure request
        response = requests.get(amazon_url, headers=headers)
        
        # 3. Check for security blocks (200 means success, 503 means blocked)
        if response.status_code != 200:
            print(f"Amazon blocked the request. Status: {response.status_code}")
            return None
            
        # 4. Initialize BeautifulSoup to read the raw HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Page Title fetched:", soup.title.text if soup.title else "No Title Tag")
        # Find the specific span tag containing the title
        title_element = soup.find('span', id='productTitle')
        
        if title_element:
            # .text gets the inner text, .strip() removes extra spaces and newlines
            return title_element.text.strip()
        else:
            print("Title tag not found in the HTML.")
            return None
        

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_product_reviews(amazon_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'cookie': os.getenv("AMAZON_COOKIE")  # Load the cookie from the .env file
    }

    # Extract ASIN and build the dedicated reviews URL
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", amazon_url)
    if not asin_match:
        print("Could not find ASIN in URL")
        return None
        
    asin = asin_match.group(1)
    reviews_url = f"https://www.amazon.in/product-reviews/{asin}"
    
    try:
        # Request the dedicated reviews page, not the product page
        response = requests.get(reviews_url, headers=headers)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Page Title fetched:", soup.title.text if soup.title else "No Title Tag")
        reviews_list = []
        
        # Find all review containers using the data-hook attribute
        review_elements = soup.find_all('div', {'data-hook': 'reviewRichContentContainer'})

        # Fallback if the primary container is empty
        if not review_elements:
            review_elements = soup.find_all('span', {'data-hook': 'review-body'})
        
        for element in review_elements:
            # .text grabs all text inside the div (including the nested span)
            review_text = element.text.strip()
            
            # Only add non-empty strings to our list
            if review_text:
                reviews_list.append(review_text)
                
        return reviews_list
        

    except Exception as e:
        print(f"An error occurred: {e}")
        return None