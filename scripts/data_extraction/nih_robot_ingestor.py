from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import re
import time

"""
Esta clase tiene:
    - El constructor

"""

class NIHFormIngestion:

    def __init__ (self, csv_path):
        self.driver= webdriver.Chrome()
        self.terms= csv_path

    def getKeyWords(self):
        for _, row in self.terms.iterrows():
            termino=row["term"]
            print(termino)

    def doASearch(self):
        patron = r' - (\d+)'

        for _, row in self.terms.iterrows():

            self.driver.get("https://accessgudid.nlm.nih.gov")

            termino = row["term"]

            try:
                search_box= self.driver.find_element(By.ID, "searchToolsQuery")
            except NoSuchElementException:
                try:
                    search_box= self.driver.find_element(By.ID, "searchQuery")
                except NoSuchElementException:
                    print("No se pudo encontrar el searchBox ni por el ID principal ni por el ID secundario")
            
            
            if search_box:
                search_box.send_keys(termino)
                search_box.send_keys(Keys.RETURN)
            else:
                print("No se encontró el search box")

            resultados= self.driver.find_elements(By.CSS_SELECTOR,".resultRow.no-padding h3 a")

            if resultados:
                id=re.findall(patron, resultados[0].text)
                print("El id del primer elemento: ", id)
                resultados[0].click()
                self.driver.implicitly_wait(40)
                total=len(resultados)
            else:
                total=0

            print("Total elementos encontrados: ",total)
            resultados.clear()


        self.driver.quit()

