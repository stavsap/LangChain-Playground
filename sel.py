from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_eight_components():
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://medium.com/@ashukumar27/dolly2-and-langchain-a-game-changer-for-text-data-analytics-7518d48d0ad7")

    for elem in driver.find_elements(by=By.TAG_NAME, value="p"):
        try:
            print(elem.text)
        except Exception as e:
            continue


    driver.quit()

test_eight_components()