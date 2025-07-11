#!/usr/bin/env python3
"""
search_part.py  —  Google Programmable Search Edition
=====================================================

Search the web for a specific electronic part number and print the top N
results (title, URL, snippet).

Requirements:
-------------
1. Python 3.8+
2. pip install requests
3. Environment variables:
   - GOOGLE_API_KEY="your Google Cloud API key"
   - GOOGLE_CX="your Programmable Search Engine ID"

Usage:
-------
$ python search_part.py STM32F103C8T6 --top_k 10
"""

import argparse
import os
import textwrap
import requests


def google_search(query: str, api_key: str, cx: str, top_k: int = 10) -> list[dict]:
    """Query Google Custom Search and return results."""
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": f'"{query}"',
        "num": min(top_k, 10)  # max per request
    }

    response = requests.get(endpoint, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    return [
        {
            "title": item["title"],
            "url": item["link"],
            "snippet": item.get("snippet", "")
        }
        for item in data.get("items", [])
    ]


def print_results(results: list[dict]):
    """Pretty-print search results."""
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   {result['url']}")
        print(f"   {textwrap.shorten(result['snippet'], width=100)}\n")


def main():
    parser = argparse.ArgumentParser(description="Search for a part number using Google Custom Search API.")
    parser.add_argument("part_number", help="Part number to search for (e.g., STM32F103C8T6)")
    parser.add_argument("--top_k", type=int, default=10, help="Number of results to return (max 10 per query)")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")

    if not api_key or not cx:
        print("❌ Error: You must set GOOGLE_API_KEY and GOOGLE_CX environment variables.")
        print("Example:\n  export GOOGLE_API_KEY='your-key'\n  export GOOGLE_CX='your-cx-id'")
        return

    try:
        results = google_search(args.part_number, api_key, cx, args.top_k)
        if results:
            print_results(results)
        else:
            print("No results found.")
    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}\n{e.response.text[:200]}")
    except requests.RequestException as e:
        print(f"Network error: {e}")


if __name__ == "__main__":
    main()
