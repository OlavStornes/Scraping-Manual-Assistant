from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class Scrapie():
    def __init__(self, entry, database, m_game):
        self.page_number = 1
        self.target_system = entry.name
        self.target_id = entry.sys_id
        self.db = database
        self.m_game = m_game
        self.finished = False
        self.elem_id = "GridView1"
        self.system_dropid = "DropSys"
        self.url = "http://www.gamesdatabase.org/list.aspx?manual=1"
        self.js_script = "javascript:__doPostBack('" + \
            self.elem_id + \
            "','Page${0}')"

    def init_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)

    def setup_browser_table(self):
        selector = Select(self.browser.find_element_by_id(self.system_dropid))
        selector.select_by_visible_text(self.target_system)

        delay = 2  # seconds
        try:
            self.table = WebDriverWait(self.browser, delay).until(
                EC.presence_of_element_located((By.ID, self.elem_id)))
        except TimeoutException:
            print("Loading took too much time! Is it the last page?")
            if '404' in self.browser.title:
                self.finished = True

    def aquire_table(self):
        self.table = self.browser.find_element_by_id("GridView1")

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

    def aquire_entries(self):
        entries = self.table.find_elements_by_tag_name('tr')[3:]
        self.aquire_cells(entries)

    def save_page_to_table(self, rows):

        data_source = []

        for x in rows:
            y = {
                "game": x[0],
                "system": self.target_id,
                "publisher": x[1],
                "developer": x[2],
                "category": x[3],
                "year": x[4] or 0
            }
            try:
                q = self.m_game.get(self.m_game.game == y["game"])
            except Exception as e:
                data_source.append(y)

        with self.db.atomic():
            for data_dict in data_source:
                self.m_game.create(**data_dict)

        print("Done! Added {} rows to the table!".format(len(data_source)))

    def aquire_cells(self, entries):
        tmp = []
        for row in entries[:-2]:
            tmp.append(self.transform_to_row(row))

        self.save_page_to_table(tmp)

    def transform_to_row(self, row):
        rawcell = row.find_elements_by_tag_name('td')
        # Only extract relevant bois
        cell_pos = [1, 5, 7, 8, 9]

        output = []

        for cell in cell_pos:
            output.append(rawcell[cell].text)

        return output

    def scrape_all(self):
        self.aquire_table()
        while not self.finished:
            self.aquire_entries()
            self.iterate_pages()

    def cleanup(self):
        print("Finished with system {}.".format(
            self.target_system,
        ))
        self.browser.stop_client()
        self.browser.quit()

    def run(self):
        self.init_browser()
        self.setup_browser_table()
        self.scrape_all()

        self.cleanup()


if __name__ == "__main__":
    scraper = Scrapie('Amstrad CPC')
    scraper.run()
