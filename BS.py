import json
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

def save_image(image_url, image_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as image_file:
                image_file.write(response.content)
            print(f"Image saved to {image_path}")
        else:
            print(f"Failed to download image from {image_url}")
    except Exception as error:
        print(f"Error saving image: {error}")
        def translate_with_rapidapi(text_to_translate, api_key):url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    headers = {
        "x-rapidapi-key": "api_key",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    payload = {
        "from": "es",
        "to": "en",
        "q": "text_to_translate"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()[0]
def initialize_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=chrome_options)
def get_page_language(browser):
    return browser.find_element(By.TAG_NAME, "html").get_attribute("lang")

def translate_headers(headers, api_url, api_key):
    headers_count = {}
    api_headers = {
        "x-rapidapi-key": "31d241f829mshe00f667c8856846p1b4b5bjsne99e18e8c7f9",
	"x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
	"Content-Type": "application/json"
}



    for header in headers:
        payload = {
            "from": "es",
            "to": "en",
            "q": header
        }
        try:
            response = requests.post(api_url, json=payload, headers=api_headers)
            response.raise_for_status()
            translated_text = response.json()[0]
            print(f"Translated: '{header}' -> '{translated_text}'")
            for word in translated_text.split():
                word_lower = word.lower()
                headers_count[word_lower] = headers_count.get(word_lower, 0) + 1
        except Exception as e:
            print(f"Error translating header '{header}': {e}")
    return headers_count
def translate_headers(headers, api_url, api_key):
    headers_count = {}
    api_headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    for header in headers:
        payload = {
            "from": "es",
            "to": "en",
            "q": header
        }
        try:
            response = requests.post(api_url, json=payload, headers=api_headers)
            response.raise_for_status()
            translated_text = response.json()[0]
            print(f"Translated: '{header}' -> '{translated_text}'")
            for word in translated_text.split():
                word_lower = word.lower()
                headers_count[word_lower] = headers_count.get(word_lower, 0) + 1
        except Exception as e:
            print(f"Error translating header '{header}': {e}")
    return headers_count

def display_repeated_words(word_counts, min_count=2):
    for word, count in word_counts.items():
        if count >= min_count:
            print(f"The word '{word}' is repeated {count} times.")

def main():
    browser = initialize_browser()
    try:
        browser.get('https://elpais.com/')
        lang = get_page_language(browser)
        print(f"Website language: {lang}")
        if lang != 'es-ES':
            print("Website is not in Spanish.")
        handle_cookies(browser)
        articles = scrape_opinion_section(browser)
        headers = fetch_article_data(articles)

        translation_api_url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
        api_key = "your-rapidapi-key"

        word_counts = translate_headers(headers, translation_api_url, api_key)
        display_repeated_words(word_counts)
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
