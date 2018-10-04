import selenium
from selenium import webdriver

browser = webdriver.Chrome()
url = "http://www.gamesdatabase.org/list.aspx?manual=1" 
browser.get(url)

table = browser.find_element_by_id("GridView1")

entries = table.find_elements_by_tag_name('tr')[3:]

for row in entries:
    cells = row.find_elements_by_tag_name('td')
    for cell in cells:

        print(cell)