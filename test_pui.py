import pytest, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

_base_url = os.getenv('BASE_URL')
# print(driver.page_source)

def test_main_page_reachable(driver):
	driver.get(str(_base_url))
	title = driver.title
	print(title)
	assert title == 'Hollis Archival Collection Guides | HOLLIS for'

def test_search_by_keyword(driver):
	# assumes the existance of "Test Resource 123" collection (which is on dev. Better way to do this?)
	driver.get(str(_base_url))
	search_field = element = driver.find_element(By.ID, "q0")
	search_field.send_keys("Test Resource 123")
	assert search_field.get_attribute('value') == 'Test Resource 123'
	search_field.send_keys(Keys.RETURN)
	results = driver.find_elements(By.CLASS_NAME, "recordrow")
	assert len(results) == 1
	abstract = results[0].find_element(By.CLASS_NAME, "abstract").text
	assert abstract == "Overview:\nTest Resource Abstract"


@pytest.fixture(scope='session', autouse=True)
def driver():
	# Will be executed before the first test
	options = webdriver.ChromeOptions()
	options.add_argument('--no-sandbox')
	options.add_argument('--window-size=1920,1080')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(options=options)
	driver.maximize_window()
	yield driver
	# Will be executed after the last test
	driver.quit()
