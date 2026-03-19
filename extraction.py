from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import pandas as pd
import random

def get_price(driver):
    xpaths = [
        "//span[@data-testid='ldp-text-price']",   
        "//p[contains(text(),'Rp') and contains(@class,'font-bold')]"     
    ]

    for xp in xpaths:
        try:
            el = driver.find_element(By.XPATH, xp)
            text = el.text.strip()
            if text:
                return text
        except:
            continue

    return None

def get_loc(driver, url):
    xpath = [
        "//span[@data-testid='ldp-address']",
        "//p[contains(@class,'text-gray') and contains(text(),'Jakarta')]",
        "//span[contains(@class,'font-bold') and contains(text(),'Jakarta')]"
    ]

    for xp in xpath:
        try:
            el = driver.find_element(By.XPATH, xp)
            text = el.text.strip()
            if text and len(text) < 100:
                return text
        except:
            continue

    try:
        slug = url.split("/properti/")[1].split("/")[0]
        parts = slug.replace("-", " ").title()
        return parts
    except:
        return None

def get_specs (driver):
    specs = {}

    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-test-id = 'pdp-expanded-specification']")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btn
        )
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)
    except TimeoutException:
        pass

    rows =  driver.find_elements(
        By.XPATH,
        "//div[.//p[contains(@class,'text-greyText')] and .//p[contains(@class,'text-accent')]]"
    )

    for row in rows:
        try:
            label = row.find_element(
                By.XPATH, ".//p[contains(@class, 'text-greyText')]"
            ).text.strip()

            value = row.find_element(
                By.XPATH,
                ".//p[contains(@class, 'text-accent')]"
            ).text.strip()

            if label and value:
                specs[label] = value
        except:
            continue

    return specs


city_listing = {
    "jakarta-selatan": "Jakarta Selatan",
    "jakarta-barat": "Jakarta Barat",
    "jakarta-timur": "Jakarta Timur",
    "jakarta-utara": "Jakarta Utara",
    "jakarta-pusat": "Jakarta Pusat",
    "bogor": "Bogor",
    "depok": "Depok",
    "tangerang": "Tangerang",
    "bekasi": "Bekasi"
}
def scrape_listings(cities):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = (WebDriverWait(driver, 20))
    all_data = []

    for city_slugs, city_name in cities.items():
        print(f"\nScrapping {city_name}...")

        search_url = f"https://www.rumah123.com/jual/{city_slugs}/rumah/"
        driver.get(search_url)
        
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/properti/')]"))
        )

        time.sleep(3)

        cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/properti/')]")

        clean_urls = []

        for card in cards:
            try:
                href = card.get_attribute("href")
                if not href:
                    continue

                if "/properti/" not in href:
                    continue

                if "/perumahan-baru/" in href:
                    continue

                if "/apartement/" in href:
                    continue

                clean_urls.append(href)
            except:
                pass
        # Deduplicate urls    
        urls = list(dict.fromkeys(clean_urls))
        urls = urls[:15]
        print(f" Found {len(urls)} listings")


        for url in urls:
            try:
                driver.set_page_load_timeout(25)
                driver.get(url)
                if "/perumahan-baru/" in url or "/apartemen/" in url:
                    print("Skipped project", url)
                    continue

            except TimeoutException:
                print(f" Timeout loading page, skipped {url}")
                continue
            
            except WebDriverException as e:
                print(f"Webdriver error, skipped: {url}")
                continue

            time.sleep(random.uniform(2.5, 4.5))
            title = price = location = specs= None

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text.strip()
                if "rumah123" in title.lower():
                    continue
                location = get_loc(driver, url)
                price =get_price(driver)
                specs = get_specs(driver) or {}
            except Exception as e:
                specs = {}
    
                

            all_data.append({
                "title" : title,
                "price" : price,
                "location" : location,
                "luas_tanah": specs.get("Luas Tanah"),
                "luas_bangunan": specs.get("Luas Bangunan"),
                "kamar_tidur": specs.get("Kamar Tidur"),
                "kamar_mandi": specs.get("Kamar Mandi"),
                "garasi": specs.get("Garasi"),
                "carport": specs.get("Carport"),
                "sertifikat": specs.get("Sertifikat"),
                "jumlah_lantai": specs.get("Jumlah Lantai"),
                "url" : url
            })

            # time.sleep(4)
        
    driver.quit()
    return pd.DataFrame(all_data)


df = scrape_listings(city_listing)
df.to_csv("house_listing.csv")
print(df.head())
print(df.shape)
