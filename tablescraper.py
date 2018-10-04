import selenium
import openpyxl
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class Scrapie():
    def __init__(self):
        self.page_number = 1
        self.finished = False
        self.elem_id = "GridView1"
        self.url = "http://www.gamesdatabase.org/list.aspx?manual=1"
        self.js_script = "javascript:__doPostBack('" + \
            self.elem_id + \
            "','Page${0}')"

    def init_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)

    def aquire_table(self):
        self.table = self.browser.find_element_by_id("GridView1")

    def aquire_entries(self):
        self.entries = self.table.find_elements_by_tag_name('tr')[3:]

    def iterate_pages(self):
        self.page_number += 1
        self.browser.execute_script(self.js_script.format(self.page_number))

        delay = 2  # seconds
        try:
            self.table = WebDriverWait(self.browser, delay).until(
                EC.presence_of_element_located((By.ID, self.elem_id)))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time! Is it the last page?")
            if '404' in self.browser.title:
                self.finished = True

    def write_entry_to_database(self, row):
        cells = row.find_elements_by_tag_name('td')
        for cell in cells:
            print(cell)

    def aquire_cells(self):
        for row in self.entries[:-1]:
            self.write_entry_to_database(row)

    def run(self):
        self.init_browser()
        self.aquire_table()
        self.aquire_entries()
        self.iterate_pages()


if __name__ == "__main__":
    scraper = Scrapie()
    scraper.run()
