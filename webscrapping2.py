from selenium import webdriver
import time
import csv
import sys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get("https://directoriosancionados.funcionpublica.gob.mx/SanFicTec/jsp/Ficha_Tecnica/SancionadosN.htm")
    time.sleep(1)

    alert_obj = driver.switch_to.alert  #Cambiondo control del driver al alert
    alert_obj.accept() #acptando alert
    time.sleep(3)

    driver.switch_to.frame(0)
    time.sleep(1)
    select = Select(driver.find_element_by_name('cmdsan'))
    select.select_by_value("INHABILITA")
    time.sleep(3)
    links=driver.find_elements_by_tag_name("a")
    links=links[1:]

    cv=["infractor","num exp","fecha notificacion de resolucion","publicacion en el dof","monto de la multa","plazo de inhanilitacion","inicia","termina"]

    myFile = open('example2.csv', 'w',encoding="utf-8",newline='')
    writer = csv.writer(myFile,dialect='excel')
    writer.writerow(cv)
    driver.switch_to.default_content()
    anterior_data = []
    for link in links:
        driver.switch_to.default_content()
        driver.switch_to.frame(0)
        print(link.text)
        link.click()
        time.sleep(2)

        driver.switch_to.default_content()
        driver.switch_to.frame(1)

        parrafos = driver.find_elements_by_tag_name("p")
        parrafos = parrafos[0:3]

        data=[]

        for parrafo in parrafos:
            aux=parrafo.text.split("\n")
            for item in aux:
                aux2=item.split(":",1)
                data.append(aux2[1])

        if data == anterior_data:
            driver.switch_to.default_content()
            driver.switch_to.frame(0)
            print("excepcion")
            print(data, "==", anterior_data)
            elem = driver.find_element_by_tag_name('body')
            elem.send_keys(Keys.PAGE_DOWN)
            continue

        anterior_data = data
        writer.writerow(data)
        #print(data)
        driver.switch_to.default_content()
        driver.switch_to.frame(0)



    myFile.close()
    driver.close()
except :
    print(sys.exc_info())
    sys.exit()