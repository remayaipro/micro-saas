#!/usr/bin/env python3
"""URL Shortener with AI Summarization - CLI Tool"""

import argparse
import random
import string
import json
import re
from urllib.parse import urlparse

# Simple in-memory storage (use Redis in production)
short_codes = {}
url_data = {}

def generate_short_code(length=6):
    """Generate a random short code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def fetch_page_title(url):
    """Simulate fetching page title (in production, use requests + BeautifulSoup)"""
    # In production, you'd use: requests.get(url).text and parse with BeautifulSoup
    parsed = urlparse(url)
    return f"Page from {parsed.netloc}"

def summarize_content(url):
    """AI summary of target page (simplified - in production use OpenAI/Claude API)"""
    title = fetch_page_title(url)
    # Simulated AI summary - replace with actual API call
    summary = f"Content from {url}: {title} - A web page with various content."
    return summary

def shorten_url(url):
    """Create a short URL with AI summary"""
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return None, "Invalid URL format"
    
    # Generate unique short code
    short_code = generate_short_code()
    while short_code in short_codes:
        short_code = generate_short_code()
    
    # Get AI summary
    summary = summarize_content(url)
    
    # Store data
    short_codes[short_code] = url
    url_data[short_code] = {
        "original_url": url,
        "short_code": short_code,
        "summary": summary
    }
    
    return short_code, summary

def resolve_url(short_code):
    """Resolve a short code to original URL"""
    return short_codes.get(short_code)

def main():
    parser = argparse.ArgumentParser(description='URL Shortener with AI Summarization')
    parser.add_argument('command', choices=['shorten', 'resolve', 'list'], help='Command to execute')
    parser.add_argument('--url', '-u', help='URL to shorten')
    parser.add_argument('--code', '-c', help='Short code to resolve')
    
    args = parser.parse_args()
    
    if args.command == 'shorten':
        if not args.url:
            print("Error: --url required")
            return 1
        short_code, summary = shorten_url(args.url)
        if short_code:
            print(f"Short URL: {short_code}")
            print(f"AI Summary: {summary}")
            return 0
        else:
            print(f"Error: {summary}")
            return 1
    
    elif args.command == 'resolve':
        if not args.code:
            print("Error: --code required")
            return 1
        url = resolve_url(args.code)
        if url:
            print(f"Original URL: {url}")
            return 0
        else:
            print("Error: Short code not found")
            return 1
    
    elif args.command == 'list':
        print(json.dumps(url_data, indent=2))
        return 0
    
    return 0

if __name__ == '__main__':
    exit(main())