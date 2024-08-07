# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nVWFkL2R6DQN0YYimQqbKKhEFfreaSJb

**SCRAPING TEXT,LINKS AND IMAGES FROM WEB PAGES**
"""

import requests
from bs4 import BeautifulSoup

# Function to fetch HTML content from a URL
def fetch_html(url):
    response = requests.get(url)
    return response.content if response.status_code == 200 else None

# Function to scrape data from a webpage
def scrape_webpage(url):
    html_content = fetch_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract text
        paragraphs = soup.find_all('p')
        print("Paragraphs:")
        for paragraph in paragraphs:
            print(paragraph.get_text())

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        print("\nHeadings:")
        for heading in headings:
            print(heading.get_text())

        # Extract links
        links = soup.find_all('a', href=True)
        print("\nLinks:")
        for link in links:
            print(link['href'])

        # Extract images
        images = soup.find_all('img', src=True)
        print("\nImage Sources:")
        for image in images:
            print(image['src'])
    else:
        print(f"Failed to fetch {url}")

# URL of the webpage to scrape
url = 'https://www.amazon.in/'

# Scrape data from the webpage
scrape_webpage(url)