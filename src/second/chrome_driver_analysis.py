import chromedriver_binary
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from time import sleep
from getpass import getpass


def main():
    try:
        option = ChromeOptions()
        """
        option.add_argument("--headless")
        option.add_argument('--disable-gpu')
        option.add_argument("--app=https://www.google.com")
        option.add_argument("--incognito")
        """
        option.add_argument(r"--user-data-dir=E:\Profile")
        driver = Chrome(options=option)
        driver.set_window_size(1024, 768)
        al = Alert(driver)

        driver.get("https://www.youtube.com")
        sleep(1)
        box = driver.find_element_by_xpath('//*/input[@id="search"]')
        box.send_keys("ChromeDriver")
        box.submit()

        sleep(5)

        at = driver.find_elements_by_id("thumbnail")
        for b in at:
            b.click()
            break

        """
        av = driver.find_elements_by_id("video-title")
        for c in av:
            c.click()
            break
        """
        sleep(3)

        driver.get("https://www.google.com")
        sleep(1)
        box = driver.find_element_by_name("q")
        box.send_keys("ChromeDriver")
        box.submit()

        driver.execute_script(f"alert(\"{driver.title}\");")

        sleep(1)

        al.accept()

        sleep(5)

        driver.get("http://192.168.0.1")
        
        """
        driver.get("https://access.sit.ac.jp/portalv2/")
        user = driver.find_element_by_name("userID")
        user.send_keys(input("User:"))
        password = driver.find_element_by_name("password")
        password.send_keys(getpass("Pass:"))
        password.submit()

        sleep(1)

        logout = driver.find_element_by_class_name("logout_btn")
        logout.click()

        sleep(3)

        al.accept()
        """

        sleep(3)

        driver.close()
        driver.quit()
    except WebDriverException as e:
        print(e)


if __name__ == '__main__':
    main()
