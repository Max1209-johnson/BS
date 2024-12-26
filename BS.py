import json
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

def download_image(img_url, file_name):
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Image saved as {file_name}")
        else:
            print(f"Failed to download image from {img_url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Setup Chrome options
options = ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # Navigate to the website
    driver.get('https://elpais.com/')

    # Check the page language
    page_language = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    if page_language != 'es-ES':
        print("The page is not in Spanish.")
    print(f"The language of the page is: {page_language}")

    # Accept cookies if the notice appears
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'didomi-notice-agree-button'))
    ).click()

    # Locate the opinion section
    opinion_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[1]/section[2]/div/div'))
    )

    # Get the first 6 articles
    articles = opinion_element.find_elements(By.TAG_NAME, "article")[:6]
    article_headers = []

    for i, article in enumerate(articles):
        try:
            # Get the article link text
            a_element = article.find_element(By.XPATH, ".//h2/a")
            link_text = a_element.text
            print(f"Article {i + 1} Link Text: {link_text}")
            article_headers.append(link_text)

            # Attempt to find an image
            img_element = None
            try:
                img_element = article.find_element(By.TAG_NAME, "img")
            except NoSuchElementException:
                try:
                    img_element = article.find_element(By.XPATH, ".//figure//img")
                except NoSuchElementException:
                    print(f"No image found for article {i + 1}")

            # Download the image if found
            if img_element:
                img_url = img_element.get_attribute("src")
                img_file_name = f"article_{i + 1}_image.jpg"
                download_image(img_url, img_file_name)

        except NoSuchElementException as e:
            print(f"Error processing article {i + 1}: {e}")

    # Translation API setup
    api_url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    headers = {
        "x-rapidapi-key": "add-your-key-here",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    word_count = {}

    # Translate each header and count word frequency
    for header in article_headers:
        payload = {
            "from": "es",
            "to": "en",
            "q": header
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            eng_header = response.json()[0]
            print(f"Translation of '{header}': {eng_header}")

            words = eng_header.split(' ')
            for word in words:
                word_lower = word.lower()
                word_count[word_lower] = word_count.get(word_lower, 0) + 1

        except Exception as e:
            print(f"Error translating header '{header}': {e}")

    # Print words repeated 2 or more times
    for word, count in word_count.items():
        if count >= 2:
            print(f"The word '{word}' is repeated {count} times")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
