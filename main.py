from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
import random
from datetime import datetime
import pickle

def get_url(url):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--proxy-server=%s' % '212.81.36.197:9091')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        links = []
        driver.get(url)
        iteration = int(driver.find_element(By.CLASS_NAME, 'page-title-count-wQ7pG').text)
        # math
        if iteration < 50:
            iteration = 1
        else:
            iteration = iteration//50
        if iteration % 100 != 0:
            iteration += 1
        # math
        for _ in range(iteration):
            basic_arr_links = driver.find_elements(By.CSS_SELECTOR, ("a[class*='iva-item-sliderLink']"))
            for link in basic_arr_links:
                if link.get_attribute("href") not in links:
                    links.append(link.get_attribute("href"))
            time.sleep(3)
            driver.find_element(By.XPATH, "//span[text()='След. →']").click()

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        parse_link(links)

def parse_link(links):

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--proxy-server=%s' % '212.81.36.197:9091')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    result_list = []
    try:
        driver.get("https://avito.ru")
        for cookie in pickle.load(open("cookie", "rb")):
            driver.add_cookie(cookie)


        for i in range(len(links)):
            driver.get(links[i])
            title = driver.find_element(By.CLASS_NAME, 'title-info-title-text').text
            price = driver.find_element(By.CSS_SELECTOR, "span[class*='js-item-price']").get_attribute("content")
            shop = driver.find_element(By.CLASS_NAME, "text-text-1PdBw.text-size-ms-23YBR").text
            shows = driver.find_element(By.CLASS_NAME, 'item-metadata-views-item-metadata-views-zfzAR').text

            try:
                rate = driver.find_element(By.CLASS_NAME, 'style-seller-info-rating-score-KA-Kw').text
                reviews = driver.find_element(By.CLASS_NAME, 'style-root-3hVnU').text #try
            except:
                rate = 'Нет'
                reviews = 'Нет'
            try:
                driver.find_element(By.CLASS_NAME, 'css-79nocf')
                delivery = 'Включена'
            except:
                delivery = 'Выключена'

            result_list.append(
                {
                    "link": links[i],
                    "title": title,
                    "price": price,
                    "shop": shop,
                    "shows": shows,
                    "rate": rate,
                    "reviews": reviews,
                    "delivery": delivery,
                }
            )
            print(f'[+] {i} page is successfully parsed!')
        with open("result.json", 'w', encoding="utf-8") as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_url(input())

if __name__ == "__main__":
    main()