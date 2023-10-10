from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

"""
Esta clase tiene:
    - El constructor

"""

class NIHFormIngestion:
    def __init__ (self, csv_path):
        self.driver= webdriver.Chrome()
        self.terms= csv_path
        self.driver.get("https://accessgudid.nlm.nih.gov")

    def getKeyWords(self):
        for _, row in self.terms.iterrows():
            termino=row["term"]
            print(termino)

    def doASearch(self):
        for _, row in self.terms.iterrows():
            termino = row["term"]
            search_box=self.driver.find_element(By.ID, "searchQuery")
            search_box.send_keys(termino)
            search_box.send_keys(Keys.RETURN)

            self.driver.implicitly_wait(10)

            resultados= self.driver.find_elements_by_css_selector(".resultRow.no-padding")

        for element in resultados:
            element.click()

        self.driver.quit()

