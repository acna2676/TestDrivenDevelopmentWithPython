from selenium import webdriver

browser = webdriver.Chrome()
# driver = webdriver.Chrome(options=options, executable_path='chromedriver.exeの場所')
browser.get('http://localhost:8000')
assert 'install' in browser.title
