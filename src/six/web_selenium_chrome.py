# noinspection PyUnresolvedReferences
import chromedriver_binary
from selenium.webdriver import Chrome


def main():
    with Chrome() as driver:
        driver.get("https://www.google.com")


if __name__ == '__main__':
    main()
