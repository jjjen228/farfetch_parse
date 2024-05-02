from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import re
import time

def gpc(product_url, product_name):
    if "women" in product_url:
        if "dress" or "платье" in product_name.lower():
            return "1604"

def fetch_data(url):
    service = Service("C:/Users/User/Desktop/task_farfetch/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-testid="productCard"]')))
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-testid="productCard"]')))


    products = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="productCard"]')
    print(len(products))
    data = []
    count = 0
    count_scroll = 0
    for product in products:
        try:
            link = product.find_element(By.CSS_SELECTOR, 'a[data-component="ProductCardLink"]').get_attribute('href')
            if "women" in link:
                gender = "female"
            elif "men" in link:
                gender = "male"
            elif "kids" in link:
                gender = "kids"

            title = product.find_element(By.CSS_SELECTOR, 'a[data-component="ProductCardLink"]').get_attribute('aria-label').strip()

            image_element = product.find_element(By.CSS_SELECTOR, 'div[data-component="ProductCardImageContainer"] img')
            image_url = image_element.get_attribute('src') if image_element else None
            price_element = product.find_element(By.CSS_SELECTOR, 'p[data-component="Price"]')
            price = price_element.text.strip() if price_element else None
            brand_name = product.find_element(By.CSS_SELECTOR, 'p[data-component="ProductCardBrandName"]').text
            link_element = product.find_element(By.CSS_SELECTOR, 'a[data-component="ProductCardLink"]')
            link = link_element.get_attribute('href')
            item_group_id = re.search(r'item-(\d+)', link)
            item_group_id = item_group_id.group(1)
            availability = "Available" if product.find_element(By.CSS_SELECTOR, "div[data-is-loaded='true']") and price_element and price_element.text.strip() != "" else "Not available"
            google_category = gpc(link, title)

            ActionChains(driver).move_to_element(price_element).perform()
            time.sleep(0.2)
            # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'p[data-component="ProductCardSizesAvailable"]')))

            sizes_available_element = product.find_element(By.CSS_SELECTOR, 'p[data-component="ProductCardSizesAvailable"]')
            sizes_available = sizes_available_element.text
            # ActionChains(driver).move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), 0, 0)

            sizes_element = product.find_element(By.CSS_SELECTOR, 'p[data-component="ProductCardSizesAvailable"]')
            sizes_available = sizes_element.text.strip() if sizes_element else "No sizes available"
            print(sizes_available)


            
            breadcrumbs_elements = driver.find_elements(By.CSS_SELECTOR, "nav[aria-label='Breadcrumbs'] li")
            if breadcrumbs_elements:
                breadcrumbs = ' > '.join([crumb.text for crumb in breadcrumbs_elements])
                breadcrumbs += ' > ' + brand_name + ' > ' + title
            else:
                breadcrumbs = "Unknown"

            if sizes_available == 'Посмотреть размеры':
                sizes_available = ' '
                availability = 'Промо'
            sizes_list = sizes_available.split(", ")

            for size in sizes_list:
                unique_id = f"{item_group_id}_{size.replace(' ', '_')}"

                data.append({
                    'id': unique_id,
                    'item_group_id': item_group_id,
                    'link': link,
                    'title': title,
                    'gender': gender,
                    'brand': brand_name,
                    'image_link': image_url,
                    'price': price,
                    'availability': availability,
                    'product_type': breadcrumbs,
                    'size': size,
                    'google_product_category': google_category
                })
                count += 1
                if count >= 120:
                    break
            if count >= 120:
                break
            count_scroll += 1
            if count_scroll == 4:
                driver.execute_script(f"window.scrollBy(0, {500});")
                time.sleep(1)
                # wait_feed = WebDriverWait(driver, 10)
                # wait_feed.until(EC.presence_of_element_located(product))
                count_scroll = 0
        except Exception as e:
            print(e)

    driver.quit()
    return data

def create_google_merchant_feed(data):
    root = etree.Element('channel')
    for item in data:
        product = etree.SubElement(root, 'item')
        etree.SubElement(product, 'id').text = item.get('id')
        etree.SubElement(product, 'item_group_id').text = item.get('item_group_id')
        etree.SubElement(product, 'gender').text = item.get('gender')
        etree.SubElement(product, 'brand').text = item.get('brand')
        etree.SubElement(product, 'title').text = item.get('title')
        etree.SubElement(product, 'link').text = item.get('link')
        etree.SubElement(product, 'image_link').text = item.get('image_link')
        etree.SubElement(product, 'price').text = item.get('price')
        etree.SubElement(product, 'availability').text = item.get('availability')
        etree.SubElement(product, 'product_type').text = item.get('product_type')
        etree.SubElement(product, 'size').text = item.get('size')
        etree.SubElement(product, 'google_product_category').text = item.get('google_product_category')

    tree = etree.ElementTree(root)
    tree.write('google_merchant_feed.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')

url = 'https://www.farfetch.com/ca/shopping/women/dresses-1/items.aspx'
product_data = fetch_data(url)
create_google_merchant_feed(product_data)