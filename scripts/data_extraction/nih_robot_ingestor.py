from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import csv

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

            self.resultsPerPage(50)

            self.getAllResults(termino)

        self.driver.quit()

    def resultsPerPage(self, number):
        try:
            # Espera hasta que el enlace "Results Per Page" sea clickeable y hágale clic
            results_per_page_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "results-per-page"))
            )
            results_per_page_link.click()

            # Espera hasta que la opción "50" sea clickeable y hágale clic
            option_50 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ul#page-size-options li a[href*='page_size=50']"))
            )
            option_50.click()
        except TimeoutException:
            # Maneja la excepción si se lanza
            print("No hubo resultados de búsqueda")

    def getAllResults(self, termino):
        self.driver.refresh()
        resultados= self.driver.find_elements(By.CSS_SELECTOR,".resultRow.no-padding h3 a")
        total=len(resultados)

        # Primero hay que saber cuantas páginas
        print("Término de búsqueda: ", termino)
        print("Total elementos encontrados en la primera página: ",total)
        self.driver.refresh()
        pagination=self.driver.find_elements(By.CSS_SELECTOR,".bottom-pagination a")

    
        valor_maximo = 0

        for enlace in pagination:
            texto = enlace.text
            try:
                numero = int(texto)
                if numero > valor_maximo:
                    valor_maximo = numero
            except ValueError:
                pass

        if(valor_maximo==0):
            valor_maximo=1
            self.getAllCodesBySearchTerm(valor_maximo,termino)
        else:
            self.getAllCodesBySearchTerm(valor_maximo, termino)
        
        resultados.clear()

    def obtener_valor(elemento):
        try:
            return int(elemento.text)  # Intenta convertir el texto a un entero
        except ValueError:
            return 0  # Si no es un número, devuelve 0
    
    def getAllCodesBySearchTerm(self, valor_maximo, termino):
        timeout = 30  # Tiempo máximo de espera en segundos
        wait = WebDriverWait(self.driver, timeout)

        print("Total páginas", valor_maximo)
        
        self.printResults(termino)

        if valor_maximo>1:
            for i in range(2, valor_maximo + 1):
                print("Navegando a la página:", i)
                enlace_siguiente = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination-button.right-arrow")))
                enlace_siguiente.click()
                self.driver.implicitly_wait(20)
                self.printResults(termino)
                

    def printResults(self, termino):
        resultados = None 
        # Espera hasta que todos los elementos se carguen
        timeout = 30  # Tiempo máximo de espera en segundos
        wait = WebDriverWait(self.driver, timeout)
        self.driver.refresh()
        try:
            resultados = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resultRow.no-padding h3 a")))
        except StaleElementReferenceException:
            # Si se produce el error, esperar un breve momento y volver a intentar
            time.sleep(2)  # Esperar 2 segundos
            resultados = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resultRow.no-padding h3 a")))
        except TimeoutException:
            # Maneja la excepción si se lanza
            print("No hubo resultados de búsqueda")
        
        if resultados:
            for result in resultados:
                
                with open('data/primary_di_numbers.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)

                    partes = result.text.rsplit(" - ", 1)
                    if len(partes) == 2:
                        id = partes[1]
                        print("El id : ", str(id))
                        writer.writerow([str(id),termino])
                    else:
                        print("No se encontró un código en la cadena:", result.text)



   
