from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from accion import Accion
import os
from dotenv import load_dotenv
import random, time, re
from datetime import datetime
import pandas as pd

load_dotenv()

'''
FUNCIONES UTILIZADAS
'''

def to_excel(listado_acciones, num_archivo):
    '''
    Función para pasar una lista de acciones a excel
    '''
    # Obtenemos las fechas
    fechas = set()
    for accion in listado_acciones:
        fechas.update(accion.valores.keys())

    meses = {
        'ene': 'Jan',
        'feb': 'Feb',
        'mar': 'Mar',
        'abr': 'Apr',
        'may': 'May',
        'jun': 'Jun',
        'jul': 'Jul',
        'ago': 'Aug',
        'sep': 'Sep',
        'oct': 'Oct',
        'nov': 'Nov',
        'dic': 'Dec'
    }

    # Convertir el set a una lista y reemplazar los meses
    fechas_lista = list(fechas)
    fechas_lista = [fecha.replace(fecha.split()[1], meses[fecha.split()[1][:3]]) for fecha in fechas_lista]

    # Ordenamos las fechas con la librería datetime
    fechas_ordenadas = sorted(fechas_lista, key=lambda x: datetime.strptime(x, '%d %b %Y'))

    # Creamos las columnas
    columnas = ['Acción', 'Rentabilidad 5 años', 'Rentabilidad acumulada', 'Margen de beneficios'] + fechas_ordenadas
    data = []

    # Volvemos a cambiar el idioma del mes
    meses_traduccion = {
        'Jan': 'ene',
        'Feb': 'feb',
        'Mar': 'mar',
        'Apr': 'abr',
        'May': 'may',
        'Jun': 'jun',
        'Jul': 'jul',
        'Aug': 'ago',
        'Sep': 'sept',
        'Oct': 'oct',
        'Nov': 'nov',
        'Dec': 'dic'
    }
    fechas_ordenadas_esp = [fecha.replace(fecha.split()[1], meses_traduccion[fecha.split()[1]]) for fecha in fechas_ordenadas]
    # Creamos la fila. Se genera una fila por acción
    for accion in listado_acciones:
        fila = [
            accion.nombre,
            accion.rent_5a,
            accion.rent_acu,
            accion.margen_beneficios
        ]
        # Rellenar la fila con los precios o None si la fecha no está en los datos de la acción
        for fecha in fechas_ordenadas_esp:
            fila.append(accion.valores.get(fecha, None))  # None se verá como celda en blanco en Excel
        
        # Metemos la fila completa en nuestro conjunto de datos
        data.append(fila)

    # Crear el DataFrame final
    df = pd.DataFrame(data, columns=columnas)

    # Guardar en un archivo Excel
    df.to_excel(f'../data/Datos_Acciones{num_archivo}.xlsx', sheet_name="Datos Acciones", index=False)


def click_xpath(xpath: str, time1:float, time2:float, driver: webdriver):
    """
    Espera a que el elemento sea clickeable y luego hace click en él
    """
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    time.sleep(random.uniform(time1, time2))


'''
SACAMOS LOS DATOS DE LAS ACCIONES
'''

# Create a Service object with the path to the chromedriver
service = Service("../chromedriver.exe")

# Pass the Service object to the Chrome WebDriver
driver = webdriver.Chrome(service=service)

driver.maximize_window()

driver.get("https://es.finance.yahoo.com/")


try:
    wait = WebDriverWait(driver, 30)


    # Aceptamos cookies
    wait.until(EC.element_to_be_clickable((By.ID, "scroll-down-btn"))).click()
    time.sleep(random.uniform(0.5,1))
    click_xpath("//*[@id='consent-page']/div/div/div/form/div[2]/div[2]/button[1]", 2.5, 3, driver)
    time.sleep(3)

    # Iniciamos sesión
    click_xpath("/html/body/div[2]/header/div/div/div/div[2]/div/div[3]/div[2]/div/div/a", 1, 2, driver)
    
    yahoo_user = os.getenv("YAHOO_USER")
    yahoo_password = os.getenv("YAHOO_PASSWORD")

    if not yahoo_user or not yahoo_password:
        raise ValueError("Define YAHOO_USER y YAHOO_PASSWORD como variables de entorno antes de ejecutar el script.")

    barra_usuario = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/form/div[1]/div[3]/input')))
    barra_usuario.click()
    barra_usuario.send_keys(yahoo_user)
    click_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/form/div[2]/input', 1, 2, driver)

    barra_contraseña = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/form/div[2]/input')))
    barra_contraseña.click()
    barra_contraseña.send_keys(yahoo_password)
    click_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/form/div[3]/div[1]/button', 1, 2, driver)
    
    # Poso el ratón sobre "Paneles" para que aparezca el botón "Paneles de acciones".
    elemento_hover = driver.find_element(By.XPATH, "//*[@id='ybar-navigation']/div/ul/li[2]/a")
    action = ActionChains(driver)
    action.move_to_element(elemento_hover).perform()
    # Selecciono el panel de acciones
    click_xpath("//*[@id='ybar-navigation']/div/ul/li[2]/div/ul/li[2]", 0.5, 1.5, driver)

    # Una vez hemos entrado, seleccionamos dos filtros: 
    # --> seleccionamos acciones con Large & Mega Cap (tipo de capitalización de mercado)
    click_xpath("//*[@id='screener-criteria']/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/button[3]", 0.5, 1.5, driver)
    click_xpath("//*[@id='screener-criteria']/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/button[4]", 0.5, 1.5, driver)
    # --> acciones del sector tecnológico, pues es el foco de nuestro proyecto
    click_xpath("//*[@id='screener-criteria']/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[2]/ul/li/button", 0.5, 1.5, driver)    
    click_xpath("//*[@id='dropdown-menu']/div/div[2]/ul/li[11]/label/span", 3, 4, driver)
    # Buscamos las acciones con dichos filtros
    click_xpath("//*[@id='screener-criteria']/div[2]/div[1]/div[3]/button[1]", 1, 2, driver)

    click_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/section/div/div[2]/div[2]/button[3]',1.5, 2.5, driver )
    click_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/section/div/div[2]/div[2]/button[3]',1.5, 2.5, driver )


    x: int = 1 # índice para llamar a la clase única de cada acción
    for n in range(1,3):
        listado_acciones = []
        z = 0
        k = 1
        while z < 2:
            # Entramos en la acción en una ventana nueva
            enlace = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/section/div/div[2]/div[1]/table/tbody/tr[{k}]/td[1]/a")))
            time.sleep(random.uniform(1,2))
            driver.execute_script("window.open(arguments[0].href, '_blank');", enlace)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.uniform(2,3))

            # Extraemos el nombre de la acción
            nombre = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='nimbus-app']/section/section/section/article/section[1]/div[1]/div/div/section/h1"))).text
            # Extraemos la rentabilidad de los ultimos 5 años
            time.sleep(random.uniform(1,2))
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/section/section/section/article/div[1]/div/section/div[1]/button[7]"))).click()
            rent_5a = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section/section/section/article/div[1]/div/section/div[1]/button[7]/div/span/div/h3"))).text
            # Estudiamos la Rentabilidad hasta la fecha (desde inicio de año):
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/section/section/section/article/div[1]/div/section/div[1]/button[6]"))).click()
            rent_acu = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section/section/section/article/div[1]/div/section/div[1]/button[6]/div/span/div/h3"))).text
            
            # Extraemos el margen de beneficios de la empresa
            margen_beneficios = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section/section/section/article/section[6]/div[1]/section[2]/div[1]/ul/li[1]/p[2]"))).text

            # Entramos en los datos históricos para ver la evolución del precio de la acción
            click_xpath("//*[@id='nimbus-app']/section/section/aside/section/nav/ul/li[5]",3, 4, driver)
            # Filtramos por los últimos 5 años y valor mensual
            click_xpath("//*[@id='nimbus-app']/section/section/section/article/div[1]/div[1]/div[1]/button", 3, 4, driver)
            click_xpath("//*[@id='nimbus-app']/section/section/section/article/div[1]/div[1]/div[1]/div/div/section/div[1]/button[7]", 2, 3, driver)
            click_xpath("//*[@id='nimbus-app']/section/section/section/article/div[1]/div[1]/div[3]/button", 0.5, 1.5, driver)
            click_xpath("//*[@id='nimbus-app']/section/section/section/article/div[1]/div[1]/div[3]/div/div[4]", 0.5, 1.5, driver)

            # Cogemos los datos de la tabla
            valores = {}
            filas = driver.find_elements(By.XPATH, "//*[@id='nimbus-app']/section/section/section/article/div[1]/div[3]/table/tbody/tr")
            numfilas = len(filas)
            fecha_pattern = re.compile(r"1 \w{3,4} \d{4}")
            for i in range(1, numfilas + 1):
                texto = driver.find_element(By.XPATH, f"//*[@id='nimbus-app']/section/section/section/article/div[1]/div[3]/table/tbody/tr[{i}]/td[1]").text
                if fecha_pattern.match(texto):
                    try:
                        valor = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/main/section/section/section/article/div[1]/div[3]/table/tbody/tr[{i}]/td[6]"))).text
                        valores[texto] = valor
                    except Exception as e:
                            valores[texto] = "NA"
            
            # Creamos la clase de la acción
            exec(f"accion{x} = Accion(nombre, rent_5a, rent_acu, margen_beneficios, valores)")
            exec(f"listado_acciones.append(accion{x})")
            x += 1
            
            # Volvemos a la página principal
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if k != 25:
                k += 1
            else:
                k = 1
                z += 1
                click_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/section/div/div[2]/div[2]/button[3]',1.5, 2.5, driver )       

        to_excel(listado_acciones= listado_acciones, num_archivo= n)

    

finally:
    time.sleep(3)
    driver.quit()



