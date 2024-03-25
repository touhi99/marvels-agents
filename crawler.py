from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment if you don't want the browser window to open
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_page_source(url, driver):
    driver.get(url)
    time.sleep(3)  # Adjust sleep time as necessary to ensure the page loads
    return driver.page_source

def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        full_link = link['href']
        if full_link.startswith('/'):
            full_link = base_url + full_link
        elif full_link.startswith('http'):
            full_link = full_link
        else:
            continue  # Skip any other types of links
        links.add(full_link)
    return links

def save_to_csv(data, filename='crawl_results.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main(start_url):
    driver = setup_driver()
    base_url = "https://marvelstrikeforce.com"
    html = fetch_page_source(start_url, driver)
    
    # Initialize CSV file with headers
    save_to_csv(['URL', 'Content'], 'crawl_results.csv')
    
    first_child_links = extract_links(html, base_url)
    for link in first_child_links:
        try:
            child_html = fetch_page_source(link, driver)
            child_soup = BeautifulSoup(child_html, 'html.parser')
            text_content = child_soup.get_text(separator=' ', strip=True)
            # Here, we're extracting the text content. Adjust as needed.
            print(f"Visited {link}, content extracted")
            # Save only the first 500 characters for brevity, adjust as needed
            save_to_csv([link, text_content[:3000]], 'crawl_results.csv')
        except Exception as e:
            print(f"Error visiting {link}: {str(e)}")
    
    driver.quit()

main("https://marvelstrikeforce.com/en/characters")
