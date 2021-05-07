# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
import time
import re
from tqdm import tqdm
import argparse
import warnings
from user_agents import parse
warnings.simplefilter("ignore")

# SCRIPT USAGE:
### without user-agent:
# python Personalization/script_AH.py
#     --exp_name AH_first_exp1
#     --items_list shampoo boter toiletpapier pizza brood wafels ijsbergsla kefir waspoeder kattenbakvulling melk rijst bier frisdrank bananen kaas luiers tandpasta tofu
#     --web_page https://www.ah.nl/
#     --exec_path Personalization/geckodriver.exe

### with user-agent:
# python Personalization/script_AH.py
#     --exp_name AH_second_exp2
#     --items_list shampoo boter toiletpapier pizza brood wafels ijsbergsla kefir waspoeder kattenbakvulling melk rijst bier frisdrank bananen kaas luiers tandpasta tofu
#     --web_page https://www.ah.nl/
#     --exec_path Personalization/geckodriver.exe
#     --ua_string "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

# LIST OF UA STRING:
### iPhone's user agent string
# ua_string = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
### Samsung Galaxy S3
# ua_string = 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
###  non touch Blackberry device
# ua_string = 'BlackBerry9700/5.0.0.862 Profile/MIDP-2.1 Configuration/CLDC-1.1 VendorID/331 UNTRUSTED/1.0 3gpp-gba'
### iPad's user agent string
# ua_string = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'
### Kindle Fire's user agent string
# ua_string = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.1.0-80) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true'
### Touch capable Windows 8 device
# ua_string = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)'

def get_parser():
    # parse parameters
    parser = argparse.ArgumentParser(description='Scrape AH website')
    parser.add_argument("--exp_name", type=str, default="", help="Experiment name")
    parser.add_argument("--items_list", nargs='+', default="", help="List of products to search")
    parser.add_argument("--web_page", type=str, default="", help="Website url")
    parser.add_argument("--exec_path", type=str, default="", help="Path to execute the webdriver")
    parser.add_argument("--ua_string", type=str, default="", help="User agent string to specify to identify/detect devices and browsers")
    parser.add_argument("--proxy", type=str, default="", help="Proxy to mimic IP Address Geolocation")

    return parser

def iteration(driver, item, delays, collected_data):
    # banner button AH click to update the search bar
    banner_button = driver.find_element_by_xpath('//*[@title="Ga naar home pagina"]')
    # randomly choose a delay and freeze the execution to mimic a person usage
    delay = np.random.choice(delays)
    time.sleep(delay)
    # press ENTER
    banner_button.click()

    # put a query in the search bar
    delay = np.random.choice(delays)
    time.sleep(delay)
    search_button = driver.find_element_by_class_name("button-or-anchor_root__2Y4Da").click()
    search = driver.find_element_by_class_name("search-input_input__3qbvV")
    search.send_keys(item)  # put an item in the search field
    search.send_keys(Keys.RETURN)  # press ENTER

    time.sleep(5)

    timeout = 30
    try:
        main = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "search-lane-wrapper")))

        time.sleep(5)

        articles = main.find_elements_by_tag_name("article")                                # get all products from the page

        for article in tqdm(articles):
            price_header = article.find_elements_by_class_name("price-amount_root__37xv2")  # get a price object

            if len(price_header) == 0:                                                      # filter garbage from the scraped list of products
                pass

            else:
                _price_header = price_header[0].text                                        # get a price text
                price = re.sub(r'[\n\r]+', '', _price_header)                               # remove new line characters from the price string
                details = article.find_elements_by_class_name("price_unitSize__8gRVX")      # get details about the product
                product_name = article.find_elements_by_class_name('line-clamp_root__1FX_J')# get a product name

                try:
                    details_description = details[0].text                                   # if a product has a description
                except:
                    details_description = 'NaN'                                             # if it doesn't have a description

                # temporary dictionary of the product data
                temp = {
                    'item': item,
                    'product': product_name[0].text,
                    'description': details_description,
                    'price': price}

                collected_data.append(temp)                                                 # append the data

    except TimeoutException:
        # driver.quit()
        print("driver has not found products on the webpage")


def main(params):
    # initialize a list of the possible delays to mimic user interaction with websites
    delays = [1, 2, 3, 4, 5]

    # initialize a list where we store all collected data
    collected_data = []

    # list of items to search
    items_list = params.items_list

    # initalize the webdriver options
    profile = webdriver.FirefoxProfile()
    if params.ua_string != '':
        #user agent string
        ua_string = params.ua_string
        # initialize user agent
        user_agent = parse(ua_string)
        print(f"Current user-agent: {user_agent}")
        profile.set_preference("general.useragent.override", ua_string)

    PROXY = params.proxy
    if PROXY != '':
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }
    # initialize a webdriver
    driver = webdriver.Firefox(profile, executable_path=params.exec_path)
    # get the url
    driver.get(params.web_page)

    # time to wait a response from the page
    timeout = 30
    # press the button to accept cookies
    try:
        cookies = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "accept-cookies")))
        # randomly choose a delay and freeze the execution to mimic a person usage
        delay = np.random.choice(delays)
        time.sleep(delay)
        # press ENTER
        cookies.send_keys(Keys.RETURN)

    except TimeoutException:
        print("Didn't found the button accept cookies.")

    # initialize a list with failed items
    skipped_items = []

    # collect the data
    for item in tqdm(items_list):
        print("================")
        print(item)
        print("================")
        print("\n")

        try:
            try:
                try:
                    _ = iteration(driver, item, delays, collected_data)

                except:
                    _ = iteration(driver, item, delays, collected_data)

            except:
                try:
                    _ = iteration(driver, item, delays, collected_data)

                except:
                    _ = iteration(driver, item, delays, collected_data)

        except:
            print(f"{item} was skipped")
            skipped_items.append(item)
            pass

    print("Writing csv file...")
    df = pd.DataFrame(collected_data)
    df.to_csv(f'{params.exp_name}.csv', index=False)
    print("Writing finished.")

    # close the driver
    driver.quit()

if __name__ == '__main__':
    parser = get_parser()
    params, unknown = parser.parse_known_args()

    # run the script
    main(params)
