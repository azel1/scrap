import pickle
from selenium import webdriver
import time
import platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
from nordvpn_switcher import initialize_VPN, rotate_VPN, terminate_VPN
from threading import Thread

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--log-level=3")
if platform.system() == "Linux":
    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
else:
    driver = webdriver.Chrome(executable_path=r'E:\Python\chromedriver', options=chrome_options)

rotate = initialize_VPN(area_input=['random countries europe 30'])

all_cookies = os.listdir("cookies/")
print(all_cookies)
print(len(all_cookies))

driver.get('https://scrap.tf')

terminal_on = True
load_cookie = "None"
title = "None"
titletext = "--- loading ---"


def terminal():
    refresh_rate = 1
    while terminal_on is True:
        print("\n" * 10)
        print(f">> [{load_cookie}] | Wins: {won_per_acc} | Total: {won} | [{cookie_index}/{len(all_cookies)}] <<")
        print("-------------------")
        try:
            print(titletext)
        except:
            print("--- loading --- hiba")
        print("-------------------")
        print(f"Wins: {winnings}")
        print(f"Not Claimed: {won_itemsclean}")
        # print("\n" * 2)
        time.sleep(refresh_rate)


t1 = Thread(target=terminal)


def close_ad():
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]'))).click()
    except Exception as ex:
        pass
        # print(f"Failed closing ad: {ex}")


def scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        try:
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="raffles-inline-1"]')))
        except:
            pass
        driver.execute_script("""
        var element = document.querySelector(".inline-raffle-ad");
        if (element)
            element.parentNode.removeChild(element);
        """)
    except Exception as ex:
        print("HIBA SCROLL()" + str(ex))


def main():
    global titletext
    list = []
    already_done_raffle = 0
    index = 0
    justdid_raffle = 0
    scroll()
    raffles_list = driver.find_elements_by_xpath("//*[@id='raffles-list']/div")
    for title in raffles_list:
        index += 1
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        if title.get_attribute("class") == "panel-raffle raffle-entered":
            already_done_raffle += 1
            continue
        else:
            justdid_raffle += 1
        total = (len(raffles_list))
        # print(f"--- ({str(load_cookie)})")
        # print("Total: " + str(total) + "\nRemain: " + str(total - justdid_raffle - already_done_raffle))
        # print("Total: " + str(total))
        # print(title.text)
        titletext = title.text
        # print(title.get_attribute("class"))
        list.append(title.text)
        try:
            href = driver.find_element_by_xpath(
                '//*[@id="raffles-list"]/div[' + str(index) + ']/div[1]/div[1]/a').get_attribute('href')
        except:
            href = driver.find_element_by_xpath(
                '//*[@id="raffles-list"]/div[' + str(index - 1) + ']/div[1]/div[1]/a').get_attribute('href')
        # print(href)
        ####
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        driver.get(href)
        var = driver.find_elements_by_css_selector('button.btn.btn-embossed.btn-info.btn-lg')
        close_ad()
        for btn in var:
            try:
                btn.click()
                WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(
                        (By.ID, 'raffle-leave')))
                # raffle-leave

            except Exception as ex:
                pass

        driver.close()
        time.sleep(2)
        print("---")
        ####
    # print(list)
    # print(str(len(list)) + " rafflebe belépve")
    # print(str(already_done_raffle) + " már kész volt")


winnings = []
won_items = []
won = 0
won_per_acc = 0
cookie_index = -1
# won_items = []
remove_content = ["'", "[", "]"]
if __name__ == "__main__":
    global won_itemsclean
    won_itemsclean = []
    # global winnings
    t1.start()
    while True:
        if cookie_index < (len(all_cookies)) - 1:
            cookie_index += 1
        else:
            cookie_index = 0

        # areas = ["Austria", "Slovenia", "Slovakia", "Hungary", "Croatia", "Netherlands"]
        # area = [areas[cookie_index]]
        # rotate = initialize_VPN(area_input=area)
        try:
            rotate_VPN(rotate)
        except:
            time.sleep(5)
            rotate_VPN(rotate)


        load_cookie = all_cookies[cookie_index]
        cookies = pickle.load(open("cookies/" + load_cookie, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        try:
            driver.get('https://scrap.tf/raffles')
        except Exception as error:
            print(f"Error: {error}")
            time.sleep(3)
        print("Loaded: " + str(load_cookie))
        ####### LIST ITEMS WON #######
        try:
            x = driver.find_element_by_xpath('//*[@id="main-container"]/div[3]')
        except:
            x = False
        if x:
            i = 0
            for i in range(5):
                i += 1
                try:
                    item = driver.find_element_by_xpath(
                        '//*[@id="main-container"]/div[2]/div[2]/div[' + str(i) + ']/div[4]/div/div/div')
                    won_items.append((item.get_attribute('data-title')) + "(" + str(cookie_index) + ")")
                except Exception as ex:
                    print(ex)
                    # pass
            won_itemsclean = repr(won_items)
            for content in remove_content:
                won_itemsclean = won_itemsclean.replace(content, '')
            # print(my_str)
        ####### LIST ITEMS WON #######
        try:
            won = won + int(driver.find_element_by_xpath('//*[@id="main-container"]/div[3]/div[2]/div/div[3]/h1').text)
            won_per_acc += int(driver.find_element_by_xpath('//*[@id="main-container"]/div[3]/div[2]/div/div[3]/h1').text)
        except Exception as kurva:
            # print("Hiba az eddig nyert kiirasaban" + str(kurva))
            try:
                won = won + int(
                    driver.find_element_by_xpath('//*[@id="main-container"]/div[2]/div[2]/div/div[3]/h1').text)
                won_per_acc += int(
                    driver.find_element_by_xpath('//*[@id="main-container"]/div[2]/div[2]/div/div[3]/h1').text)
            except:
                pass
        finally:
            # won = won + int(driver.find_element_by_xpath('//*[@id="main-container"]/div[1]/div[2]/div/div[3]/h1').text)
            pass
        main()
        try:
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        except:
            pass

        driver.refresh()
        if won_per_acc != 0:
            winnings.append(f"{all_cookies[cookie_index]}: {won_per_acc}")
        # print("Total winnings: " + str(won) + " raffles.")
        # print(f"Won on this acc: {won_per_acc}")
        won_per_acc = 0
        # print("Ended: " + all_cookies[cookie_index])
        if cookie_index >= (len(all_cookies)) - 1:
            print("SLEEPING...")
            print(winnings)
            winnings = []
            won = 0
            won_items = []
            terminate_VPN(instructions=None)
            time.sleep(0)
