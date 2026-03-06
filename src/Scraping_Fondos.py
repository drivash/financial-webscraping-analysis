'''
Este programa extrae datos relevantes de fondos cuyo principal sector es el tecnológico.
Después, los guarda en un archivo csv.
Busca dichos fondos en la página web de Morningstar.
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time
from fondo import Fondo_acciones
from typing import List
import pandas as pd


'''
FUNCIONES PROYECTO 
'''


def extractor_informacion(webElement) -> Fondo_acciones:
    '''
    Extrae información de un fondo. 
    Para ello, abre una pestaña nueva, se mueve por las zonas de interes obteniendo los datos que nos interesan
    y por último cierra la pesaña donde operaba.

    POST: Devuelve toda la información de interés de un fondo, como el ISIN, comisiones, rentabilidades en un rango de años
    hasta el actual y volatilidad. 
    '''
    # Abrimos una pestaña nueva con el fondo de interés
    driver.execute_script("window.open(arguments[0].href, '_blank');", webElement)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)

    # Saco el nombre del fondo
    nombre_fondo = driver.find_element(By.XPATH, '//div[@class="snapshotTitleBox"]/h1').text

    # Saco precio de accion (último precio al que se ha comprado la participación)
    precio_accion_sucio = driver.find_element(By.XPATH, '//*[@id="overviewQuickstatsDiv"]/table/tbody/tr[2]/td[3]').text
    precio_accion = precio_accion_sucio.replace('&nbsp;', ' ') # viene con otra codificación

    # Sacamos el ISIN (identificador)
    isin = driver.find_element(By.XPATH, '//*[@id="overviewQuickstatsDiv"]/table/tbody/tr[5]/td[3]').text    

    # me muevo al apartado de comisiones
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Comisiones"]'))).click()
    time.sleep(1.5)
    Gasto_de_gestion_max_anual = driver.find_element(By.XPATH, '//*[@id="managementFeesAnnualChargesDiv"]/table/tbody/tr[2]/td[2]').text
    Gastos_corrientes = driver.find_element(By.XPATH, '//*[@id="managementFeesAnnualChargesDiv"]/table/tbody/tr[3]/td[2]').text
    comisiones = {
        "Gasto De Gestión Max Anual" : Gasto_de_gestion_max_anual,
        "Gastos Corrientes" : Gastos_corrientes
        }
    
    # me muevo al apartado de rentabilidades
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Rentabilidad"]'))).click()
    time.sleep(1.5)

    # Capto la tabla donde obtener los datos de rentabilidad
    target_table = driver.find_element(By.XPATH, '//*[@id="returnsCalenderYearDiv"]/table') 

    # Obtengo las filas de mi tabla
    rows = target_table.find_elements(By.TAG_NAME, 'tr')
    fila_fechas = rows[1] # fechas aquí
    fila_rentab = rows[2] # datos aquí

    # Obtengo las celdas donde se encuentran los datos
    celdas_fechas = fila_fechas.find_elements(By.TAG_NAME, 'td')
    celdas_rentab = fila_rentab.find_elements(By.TAG_NAME, 'td')

    # Obtengo los datos de cada celda
    datos_fechas = [celda.text for celda in celdas_fechas]
    datos_rentab = [celda.text for celda in celdas_rentab]

    # Elimino la primera columna, ya que contiene datos innecesarios
    datos_fechas.pop(0)
    datos_rentab.pop(0)

    # Elimino datos vacíos
    datos_fechas_limpios  = [datos for datos in datos_fechas if datos != ""]
    datos_rentab_limpios = [datos for datos in datos_rentab if datos != ""]

    # Los agrupo en un diccionario
    dict_rentab = dict(zip(datos_fechas_limpios, datos_rentab_limpios))

    # Nos pueden salir diccionarios de diversas longitudes, así que vamos a hacer que todos tengan el mismo formato

    # Invierto el diccionario obtenido para sacar sus valores en el orden que me interesa
    inv_dict_rentab = dict(reversed(list(dict_rentab.items())))
    valores = iter(inv_dict_rentab.values())

    # Hago el diccionario plantilla.
    rentab_inv =  {"2024": "-", "2023": "-", "2022" : "-", "2021" : "-", "2020" : "-", "2019" : "-", "2018": "-", "2017" : "-"}
    
    # Cambio los valores "-" por los disponibles (si no hay más valores se quedará el guión)
    rentab = {
        clave : next(valores, valor) for clave, valor in rentab_inv.items()
    }
    
    # Accedo al apartado de Rating y Riesgo
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Rating y Riesgo"]'))).click()
    
    # Saco la volatilidad 
    time.sleep(random.uniform(1.5,2.5))
    dato_volat = driver.find_element(By.XPATH, '//*[@id="ratingRiskLeftDiv"]/table/tbody/tr[2]/td[2]').text
    
    # cierro la pagina actual y me muevo a la original
    driver.close()
    driver.switch_to.window(original_window)
    
    # Creo un elemento fondo y almaceno los datos en el
    result = Fondo_acciones(nombre_fondo, isin, precio_accion, comisiones, rentab, dato_volat)
    print(nombre_fondo, precio_accion, isin, comisiones, rentab, dato_volat)

    return result


def to_excel(num_file, Listado_fondos):
    '''
    Pasa a un archivo excel los datos recopilados.
    '''

    # Obtenemos un diccionario con todos los datos
    my_dict = {
        "Nombre del Fondo" : [], "ISIN" : [], "PRECIO PARTICIPACIÓN" : [], "rent 2024" : [], "rent 2023" : [], 
        "rent 2022" : [], "rent 2021" : [], "rent 2020" : [], "rent 2019" : [], "rent 2018" : [], "rent 2017" : [],
        "Gasto De Gestión Max Anual" : [], "Gastos Corrientes" : [], "Volatilidad" : []
    }

    for fondo in Listado_fondos:
        my_dict["Nombre del Fondo"].append(fondo.Nombre_fondo)
        my_dict["ISIN"].append(fondo.isin)
        my_dict["PRECIO PARTICIPACIÓN"].append(fondo.Precio_accion)
        for year in range(2024,2016, -1):
            my_dict[f"rent {year}"].append(fondo.Rentabilidad[str(year)])
        my_dict["Gasto De Gestión Max Anual"].append(fondo.Comisiones["Gasto De Gestión Max Anual"])
        my_dict["Gastos Corrientes"].append(fondo.Comisiones["Gastos Corrientes"])
        my_dict["Volatilidad"].append(fondo.Volatilidad)

    # Lo convierto a data frame
    df = pd.DataFrame(my_dict)

    # Lo paso a un excel
    df.to_excel(f"C:../../Outputs/DatosFondos{num_file}.xlsx", sheet_name="Datos Fondos")


'''
=================================================================================================================================
'''

'''
SCRIPT PROYECTO
'''

# Creo un servicio para localizar mi chromedriver
service = Service(executable_path="../../chromedriver.exe")

# Le pongo un User-agent
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

# Creo un driver con el servicio y las opciones 
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ejecuto pantalla completa en mi driver
driver.maximize_window()

# Accedo a la página deseada
driver.get("https://www.morningstar.es/es/")

try:
    wait = WebDriverWait(driver, 15)

    # reject cookies
    time.sleep(random.uniform(2, 3.5))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))).click()
    time.sleep(random.uniform(1,2.5)) # to humanize the code

    # indico a la página que soy un inversor particular
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_individual"]'))).click()

    # nos movemos al apartado de fondos de inversión
    time.sleep(random.uniform(1,2.5))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Navbar"]/nav/ul/li[3]/div/a'))).click()

    # seleccionamos el boton buscar fondos
    time.sleep(random.uniform(3, 3.5))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cmsgoLineupArticlesMiddleBottom_lineup"]/div[1]/div/a'))).click()

    # seleccionamos mostrar todos los filtros posibles
    time.sleep(random.uniform(3,3.5))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ec-screener-filters-securities-button-toggle-more-filters--caption"]'))).click()
    
    # le voy a añadir los filtros que nos interesan 
    time.sleep(random.uniform(4,4.5))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ec-screener-filters-securities-container-filter-group-section-panel-all"]/div[1]/ec-section[2]/div/div/div/div/ec-combo-box/div/span/span[1]/span/span[2]'))).click()
    time.sleep(random.uniform(4,4.5))

    morn_rating = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[1]/input'))) # 5 estrellas morningstar (rentabilidad en años pasados)
    morn_rating.send_keys("5 Estrellas", Keys.ENTER)
    time.sleep(random.uniform(4, 4.3))
    
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ec-screener-filters-securities-container-filter-group-section-panel-view-more"]/div[2]/ec-section[2]/div/div/div/div/ec-combo-box/div/span/span[1]/span/span[2]'))).click()
    time.sleep(random.uniform(4,3.8))
    sector_tecno = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[1]/input'))) # buscamos que inviertan en el sector tecnológico
    sector_tecno.send_keys("Tecnología", Keys.ENTER)
    time.sleep(random.uniform(4,5.8))
    time.sleep(1)


    # ahora vamos a coger los datos de los fondos que nos han salido con los filtros aplicados

    # scroll down (no es necesario, pero así vemos qué datos clicamos)
    elem_to_see = driver.find_element(By.XPATH, '//*[@id="ec-screener-view-tabs-dropdown-btn"]')
    driver.execute_script("arguments[0].scrollIntoView();", elem_to_see)
    time.sleep(2)


    # almacenamos los fondos que nos interesan
    enlaces_fondos : List = []
    Listado_fondos : List[Fondo_acciones] = []
    
    # Establezco mi ventana original
    original_window = driver.current_window_handle
    
    # indice de la página (cada página tiene unos 10 fondos aprox)
    i = 1 # parametro de recorrido

    while i < 29:
        # Buscamos los botones para acceder a los fondos
        enlaces_fondos.append(driver.find_elements(By.XPATH, '//a[@class="mds-link mds-link--no-underline ec-table__investment-link ng-binding"]'))

        # Hago map y obtengo la información de todos los fondos
        nuevos_fondos = list(map(extractor_informacion, enlaces_fondos[0]))
        
        # meto los fondos en el listado 
        for fondo in nuevos_fondos:
            Listado_fondos.append(fondo)

        # vacio la variable nuevos_fondos y enlaces_fondos 
        nuevos_fondos.clear()
        enlaces_fondos.clear()

        # Accedo a la siguiente página
        # Problema, hay dos botones que son prácticamente idénticos
        # Cojo los dos y me quedo con el segundo
        time.sleep(2)
        botones_siguiente = driver.find_elements(By.XPATH, '//a[@data-ng-click="setPage(parameters.page + 1)"]')
        assert(len(botones_siguiente) == 2), 'no hay la cantidad de botones siguiente esperada'
        botones_siguiente[1].click()
        time.sleep(4)
        
        # Pasamos a csv por tramos
        num_file = 1 # para dar un numero al archivo
        if i in(8, 19, 28):
            to_excel(num_file, Listado_fondos)
            num_file += 1
            Listado_fondos.clear()

        # Cambiamos de página
        i += 1

finally:

    driver.close()



