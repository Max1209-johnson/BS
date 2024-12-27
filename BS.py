from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import Counter 
import requests
import time
import re 
import os 

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
headers = {
    "x-rapidapi-key": "31d241f829mshe00f667c8856846p1b4b5bjsne99e18e8c7f9",
    "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
    "Content-Type": "application/json"
}

def save_image(url, save_folder='images'):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            
            image_name = os.path.join(save_folder, url.split('/')[-1].split('?')[0])
            with open(image_name, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {image_name}")
        else:
            print(f"Failed to retrieve the image from {url} (Status code: {response.status_code})")
    
    except Exception as e:
        print(f"Error saving images: {e}")

def translate_text(text, from_lang="es", to_lang="en"):
    payload = {"from": from_lang, "to": to_lang, "q": text}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        translation = response.json()
        return translation[0]
    else:
        print(f"Error during translation: {response.status_code}")
        return None
    
def image_url(src):
    image_sources = src.split(',')
    sorted_sources = sorted(image_sources, key=lambda x: int(x.split()[-1][:-1]), reverse=True)
    return sorted_sources[0].split()[0]

# Function to clean and tokenize text
def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()  # Now returns the list of words
    return words

try:
    driver.maximize_window()
   

    driver.get("https://elpais.com/")
    time.sleep(5)

    lang_attr = driver.find_element(By.TAG_NAME, 'html').get_attribute('lang')
    if 'es' in lang_attr:
        print('Language is Spanish')
    else:
        print(f'Language is {lang_attr}')


    accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button')))
    accept_button.click()

    opinion_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-mrf-link="https://elpais.com/opinion/"]')))
    opinion_button.click()

    time.sleep(5)

    opinion_section = wait.until(EC.visibility_of_element_located((By.XPATH, '//section[@data-dtm-region="portada_apertura"]')))
    articles = opinion_section.find_elements(By.TAG_NAME, 'article')[:5]
    
    tc_dict = {}
    img_scr_list = []


    for article in articles:
        title = article.find_element(By.XPATH, './/h2').text
        content = article.find_element(By.XPATH, './/p').text
        tc_dict[title] = content

        try:
            img_scr = article.find_element(By.TAG_NAME, 'img').get_attribute('srcset')
            if img_scr:
                img_scr_list.append(image_url(img_scr))
        except Exception as e:
            print(f"No image found in this article or error occurred: {title}")

    print(f"Article Titles and Contents: {tc_dict}")
    print(f"Image URLs: {len(img_scr_list)}")

    # Translate article titles
    translated_titles = []
    for title in tc_dict.keys():
        translated_title = translate_text(title)
        if translated_title:
            translated_titles.append(translated_title)
        else:
            print(f"Failed to translate title: {title}")

    print(f"Translated Titles: {translated_titles}")

    # Tokenize and count word occurrences in translated titles
    all_words = []
    for title in translated_titles:
        words = clean_and_tokenize(title)
        all_words.extend(words)

    word_counts = Counter(all_words)
    repeated_words = {word: count for word, count in word_counts.items() if count >= 2}

    print("Repeated words (Appearing more than twice):")
    for word, count in repeated_words.items():
        print(f"{word}: {count}")

    # Download images
    for url in img_scr_list:
        save_image(url)

finally:
    # Close the browser
    driver.quit()
