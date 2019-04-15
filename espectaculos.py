'''
LIBRERIAS
'''

import requests
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import random
import csv
import os       
import time     # Neceasrio para las fechas
import getpass  # Necesraio para detectar el user loggeado actualmente en el sistema


######## Parámetros de Conexión###############
proxy_on = False

sin_proxy = None
con_proxy = {
            "http": "http://nombre_usuario:pass@ip:puerto",
            "https": "http://nombre_usuario:pass@ip:puerto",
            }

if proxy_on:
    proxies = con_proxy
else:
    proxies = sin_proxy

headers={
    "Accept": "*/*",
    "Content-Encoding": "gzip",
    "Cache-Control": "max-age=1206531",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

reintentos = 5  # indica el número de intentos de conexión en caso de que se detecte algún fallo
delay = 30      # segundos del delay a incorporar entre llamada y llamada

######## Parámetros del site ATRAPALO ###############
ORIGEN = 'Atrapalo'    # Añadido en  v05
URL = "https://www.atrapalo.com/entradas/"       # Url de descarga del site Atrapalo
ROBOTS = "https://www.atrapalo.com/robots.txt"   # Url del fichero robots.txt

SECCIONES = {'teatro-y-danza' : 'Teatro y Danza', 
           'musica': 'Música', 
           'parques-tematicos': 'Parques temáticos', 
            'musicales': 'Musicales',
            'museos-y-exposiciones':'Museos y Exposiciones',
            'deportes':'Deportes',
            'circo': 'Circo',
            'cine': 'Cine',
            'ferias':'Ferias'}



atributos = ["Captura", "Web", "Evento", 
             "Titulo","Categoria","Novedad","Ubicación","Localidad","Precio","Descuento", 
             "Fechas", "Fecha_inicio", "Fecha_fin","Duracion","Idioma","Publico",
             "Puntuación","Valoración","Opiniones"]




######## Parámetros de la sesión de usuario ###############
fichero_csv = 'espectaculos.csv'
path = "C:/Users/" + getpass.getuser() + "/Desktop/" + fichero_csv  # Permite obviar el usuario con el que se haya loggeado el usuario en el sistema

espectaculos = []                    # Variable donde cargaremos inicialmente todos los registros que nos descargamos
espectaculos_pantalla_anterior = []  # Variable temporal que sirve para el flujo del programa
espectaculos_bbdd = []               # Variable donde cargaremos todos los registros acumulados en la bbdd actual (fichero .csv)
espectaculos_a_bbdd = []             # Variable donde almacenaremos todos los registros a volcar a la bbdd
espectaculos_nuevos = []             # Guardamos los registros nuevos descargados que no estaban en la bbdd

espectaculos_dataframe = pd.DataFrame()         # Dataframe de todos los espectaculos descargados
espectaculos_bbdd_dataframe = pd.DataFrame()    # Dataframe de todos los espectaculos de la bbdd actual, previo a la descarga
espectaculos_nuevos_dataframe = pd.DataFrame()  # Dataframe de todos los espectaculos estrictamente nuevos 
espectaculos_a_bbdd_dataframe= pd.DataFrame()   # Dataframe con todos los registros que escribiremos en la bbdd

######## Parámetros I+D ###############
# Estas variables sirven para controlar el número de registros a descargar
modo_prueba = False
pantallazos = 2  #100 registros de pruebas (5 pantallazos x 20 registros)

#########################################################################
#                                                                       #
#                           FUNCIONES                                   #
#                                                                       #
#########################################################################

'''
FUNCION: secciones_de_hoy()
    DESCRIPCIÓN: 
    Función que determina el listado de secciones a descargar cada día con el propósito de no sobrecargar las descargas diarias
    Se filtarn las secciones totales (SECCIONES) en función del dia de la semana de tal forma que al final de cada semana se hayan descargado todas
    las secciones existentes.
    Algoritmo. Se vuelca el listado de secciones total a una lista y cada día se eligen de acuerdo al siguiente algoritmo.
    Día 1 (lunes). Se descargarán las secciones que se encuentran en las posiciones (1+7n) (n>=0)  (1,8,15, etc)
    Día 2 (martes). Se descargarán las secciones que se encuentran en las posiciones (2+7n) (n>=0)  (2,9,16, etc)
    ..
    Día 7 (domingo). Se descargarán las secciones que se encuentran en las posiciones (0+7n) (n>=0)  (0,7,14,21, etc)

    INPUT: 
        Sin parámetros  
    
    OUTPUT: 
        Lista de secciones a descargar cada día
''' 
def secciones_de_hoy():
    
    dia_semana = int(time.strftime("%w"))  # 0-Domingo, 1-Lunes, 2-Martes , 3-Miercoles, 4-Jueves, 5-Viernes, 6-Sabado
    lista_secciones = sorted(list(SECCIONES.keys()))
    secciones_descargar = {}

    for cont,seccion in enumerate(lista_secciones):
        if (cont)%7 == dia_semana: # cont=0 (domingos), cont=1 (lunes),  .... cont=6 (sábado)
            secciones_descargar[seccion] = SECCIONES[seccion]
           
    return(secciones_descargar)


'''
FUNCION: licencia_robots()
    DESCRIPCIÓN: 
    Función que chequea el contenido del fichero robots.txt y avisa si comprueba que alguno de los directorios a descargar se encuentra
    referenciado en  dicho fichero

    INPUT: 
        url (string): Url del fichero hosts
        proxies (dicc): datos sobre el proxy de salida si lo hubiera
        headers (dicc): Información de la cabecera http   
    
    OUTPUT: 
        ! directorio_en_robots (Boolean): Indica si hay referencias de los ficheros o no
        directorios (list): Listado de dicrectorios chequeados
''' 
def licencia_robots(url, proxies=proxies, headers=headers):
    
    site = URL.split("//")[1].split("/")[0]   # Sacamos el directorio desde el que empezamos a realizar la búsqueda a partir de la url
    print(f"Comprobando el fichero robots.txt del site: {site}")
    directorio_en_robots = False
    
    # Leemos el fichero robots.txt en la url indicada
    robots = requests.get(url, proxies=proxies, headers=headers).text
    
    directorios = URL.split("//")[1].split("/")[1:]
    directorios = [directorio for directorio in directorios if directorio!=""] #Excluimos posibles directorios nulos
    
    for directorio_url in directorios:
        if directorio_url in robots:
            # Alguno de los directorios de la url de busqueda está referenciada en el fichero robots
            directorio_en_robots = True
            
            print(f"Atención se va a descargar algún contenido no permitido en el fichero robots.txt del site: {site}")
            print(f"Se recomienda consultar condiciones del site en el fichero: {ROBOTS}")
            print(f"Revisar política de los siguientes directorios: {directorios}")
            print("Se continúa proceso de descarga...")
            break

    if not directorio_en_robots:
        print("Parece que la descarga es compatible con la política del site")
    return(not directorio_en_robots, directorios)


    
'''
FUNCION: Sacar_espectaculos()
    DESCRIPCIÓN: 
    Función a la que se le pasa la URL de la web ATRAPALO para que se descargue todos los espectaculos que se listan
    en el apartado de 'entradas'.
    El código controla la sesión en el supuesto de que se identifique algún problema de conexión haciendo un máximo de N (varible reintentos)
    intentos espacidos N x DELAY ( variable delay) seg entre ellos. 
    Se pretende así implementar un mecanismo de evite los posibles bloqueos por parte del site  
    INPUT: 
        url (string) : URL de Atrapalo   
    
    OUTPUT: 
        nuevos_espectaculos (list): lista con todos los espectaculos encontrados
'''    

def Sacar_espectaculos(url):
    
    error = False
    descargado = False
    reintento = 1
    nuevos_espectaculos = []
    status = ""
    
    while not error and not descargado:
        
        
        try:
            #raise TimeoutError('')  #Linea para generar excepciones 
            
            # Leemos espectaculos de la url indicada
            respuesta = requests.get(url, proxies=proxies, headers=headers)
            
            if respuesta.status_code == 200:
            
                # En caso de que haya conexión y sea la primera descarga comprobamos el fichero robots.txt 
                if primera_tanda:
                    licencia_robots(ROBOTS, proxies=proxies, headers=headers)        # Chequeo del fichero robots.txt
                
                # Parseamos la respuesta para sacar los contenedores de cada espectaculo
                soup = BeautifulSoup(respuesta.content, "html.parser")
                nuevos_espectaculos = soup.find_all(class_="card-result-container")
                status = "Correcto"
                descargado = True
                
            
            elif respuesta.status_code == 404:
                status = "Url no encontrada"
                descargado = True
                
                
        except:
            
            print(f"Parece que hay problemas para conectar con el servidor. Intentando {reintentos} nuevos conexiones .... ")
            while reintento <= reintentos:
                
                espera = reintento * delay
                print(f"Persiste el problema: {reintento}º intento de conexión en {espera} segundos...")
                time.sleep(espera)
                reintento += 1
            else:
                print(f"Ha existido algún problema con la conexión. \nAbortando descarga de la url: {url}")
                status = "Problema de conexión"
                error = True
        
    
        finally:
            return(nuevos_espectaculos, status)  # Devolvemos los espectáculos y el estado de la operación




'''
FUNCION: Sacar_atributos()
    DESCRIPCIÓN: 
    Función a la que se le pasa el código html de cada uno de los espectaculos y devuelve una tupla con los atributos extraidos
    INPUT: 
        espectaculos[N]    donde N corresponde el N-ésimo espectáculo obtenido
    
    OUTPUT: 
        atributos (tupla) donde se entregan todos los atributos extráidos. Concretamente los siguientes atributos:
        captura, web, evento, titulo, categoria, novedad, ubicacion, localidad, precio, descuento, fechas, fecha_inicio, fecha_fin, duracion,
        idioma, publico, puntuacion, valoracion, opiniones
''' 

def Sacar_atributos(espectaculo):
    
     # vamos extrayendo los diferentes atributos
    
    # Captura  
    captura = time.strftime("%d/%m/%Y %H:%M")   #Fecha de hoy en formato dd/mm/aa  HH:MM
    
    # Web 
    web = ORIGEN
    
    # seccion  
    evento = seccion.replace('-y-','-')
    
    # Titulo
    try: titulo= espectaculo.find_all('h2')[0].text.strip('\n')
    except: titulo = ""
        
    # Categoria
    try:
        #categoria = espectaculo.find(class_="type large-loc").text.strip()
        categoria = espectaculo.find(class_="type large-loc").text.strip().split()[0]
    except: categoria = ""   
        
    # Novedad
    try: 
        novedad = espectaculo.find(class_="sticker-box sticker-new").text.strip() # Modificado en v06
        novedad = "" # Transitorio . Habría que borrarlo
    except: novedad = ""    
        
    # Ubicacion
    try: 
         ubicacion = espectaculo.find_all(class_="info")[0].span.text.strip("\n").strip().split("\n")[0] # v09
    except: ubicacion = ""    
    
    # Localidad 
    try:    
        localidad = espectaculo.find("p", class_="info").span.text.split()[2].strip('()')
    except: localidad = ""
        
    # Precio
    try: 
        valor = espectaculo.find(class_="value").text.strip()
        precio = re.sub('€', '', valor)
        
    except: precio = ""
        
    # Descuento
    try: 
        valor_desc = espectaculo.find(class_="status-label").span.text.strip()
        descuento = re.sub('€', '', valor_desc)
        
    except: descuento = ""                   
        
    # Fechas en cartel, inicial y final
    try:
        num = espectaculo.find_all(class_="info")[1].find_all('span')
        fechas = espectaculo.find_all(class_="info")[1].find_all('span')[0].text.strip()
        
        if len(num) >=3:
            fecha_inicio= espectaculo.find_all(class_="info")[1].find_all('span')[1].span['title'].strip()
            fecha_fin= espectaculo.find_all(class_="info")[1].find_all('span')[4]['title'].strip()
        else: 
            fecha_inicio = espectaculo.find_all(class_="info")[1].find_all('span')[1]['title'].strip()
            fecha_fin = fecha_inicio.strip()
    except: 
        fechas = ""
        fecha_inicio = ""
        fecha_fin = ""
        
    # Duracion 
    try: 
        if espectaculo.find(class_="icon-reloj_2"):
            duracion = espectaculo.find_all(class_="info")[2].text.strip()
        else:
            duracion ="NA"
    except: duracion = ""
    
    # Idioma
    try:
        if len(espectaculo.find_all(class_="info")) == 4:
            idioma = espectaculo.find_all(class_="info")[3].get_text().strip('\n').strip()
        else:
            idioma = ""
    except: idioma = ""
    
    # Publico
    try: publico = espectaculo.find(class_="item-tag").text.strip()
    except: publico = ""
    
    # Puntuacion
    try: puntuacion = espectaculo.find(class_="opi-rating").text.strip('\n').strip()
    except: puntuacion = ""
    
    # Valoracion
    try: valoracion = espectaculo.find(class_="opi-description").a.text.strip('\n').strip()
    except: valoracion = ""
    
    # Opiniones
    try: opiniones = espectaculo.find(class_="opi-description").span.text.strip('\n').strip()
    except: opiniones = ""    
            
    # Devolvemos valores
    
    atributos = (captura,
                 web,
                 evento,
                 titulo,
                 categoria,
                 novedad,
                 ubicacion,
                 localidad,
                 precio,
                 descuento,
                 fechas,
                 fecha_inicio,
                 fecha_fin,
                 duracion,
                 idioma,
                 publico,
                 puntuacion,
                 valoracion,
                 opiniones)
    
    return (atributos)



'''
FUNCION: Sacar_atributos_otras_webs()

    DESCRIPCIÓN: 

    Esta función actualmente está vacía porque para el presente proyecto sólo se descraga la web de Atrapalo.
    En el supuesto de querer añadir nuevas webs habría que incorporar una código similar al de Atrapalo pero paraticularizado
    al scrapeo de cada web. Habria que identificar igualmente los atributos a extraer y adapatarlos en número y formato a los 
    extraídos para Atrapalo
    
    INPUT: 
        espectaculos[N]    donde N corresponde el N-ésimo espectáculo obtenido
    
    OUTPUT: 
        atributos (tupla) donde se entregan todos los atributos extráidos. Concretamente los siguientes atributos:
        captura, web, evento, titulo, categoria, novedad, ubicacion, localidad, precio, descuento, fechas, fecha_inicio, fecha_fin, duracion,
        idioma, publico, puntuacion, valoracion, opiniones
''' 

def Sacar_atributos_otras_webs(espectaculo):

    atributos = ("","","","","","","","","","","","","","","","","","","")
    return (atributos)

''' 
FUNCION: crear_csv()
DESCRIPCIÓN: 
Función a la que se le pasa una ruta de localización de archivo, una n-tupla y la lista de atributos
y devuelve un archivo en formato .csv en la ruta pasada por parámetro.
    INPUT: 
        path: ruta de localización del archivo a generar
        rows: n-tupla generada por la iteración de la función Sacar_atributos[N] donde N corresponde el N-ésimo espectáculo obtenido
        atributos: lista de atributos    
    
    OUTPUT: 
        archivo en formato .csv con el contenido (header + rows)
''' 

def crear_csv(path, rows, atributos):
    with open(path, "w+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(atributos)
        for row in rows:
            writer.writerow(row)
            

#########################################################################
#                                                                       #
#                        PROGRAMA PRINCIPAL                             #
#                                                                       #
#########################################################################

print(f"Iniciando proceso de descarga.....\n")
primera_tanda = True


# Descargamos los espectaculos de las secciones diarias correspondientes
for seccion in secciones_de_hoy():
    cont = 1
    seguir_buscando = True
    while seguir_buscando:
        if cont == 0:
            url = URL + seccion + '/'
        else: 
            url = URL + seccion + '/' + 'p-' + str(cont) + '/'
        cont += 1
    
        
        # Controlamos si nos descargamos todos los registros de cada sección o solo unos de prueba. Modo I+D
        if modo_prueba and cont == (pantallazos + 1):
            
            seguir_buscando = False
        
        espectaculos_pantalla, status = Sacar_espectaculos(url) # Capturamos 2 valores de la función
        primera_tanda = False                                   # Impide que se vuelva a revisar el fichero robots.txt despues de la primera comprobacion
        
        if espectaculos_pantalla == espectaculos_pantalla_anterior:
            seguir_buscando = False
        else:
            
            print(f"Descargando URL: {url} | Espectaculos Leidos: {len(espectaculos_pantalla)} | Status: {status}") # v07 se saca de la fn
            
            
            for espectaculo in espectaculos_pantalla:
                
                
                # Identificamos la web
                if ORIGEN == 'Atrapalo':
                #La lista de espectaculos se compondrá de las tuplas correspondientes a cada espectaculo
                    espectaculos.append(Sacar_atributos(espectaculo))   
                else:
                    
                    # Este código se ejecutaría en el supuesto de que incluyéramos nuevas webs al desarrollo
                    # No disponible en la versión actual.
                    espectaculos.append(Sacar_atributos_otras_webs(espectaculo))
                

            espectaculos_pantalla_anterior = espectaculos_pantalla 
    


print(f"\nFinalizado proceso. Espectaculos descargados: {len(espectaculos)}")
espectaculos_original = espectaculos

# Procedemos a salvar la informacion a fichero
try: 
    
    # Leemos el historico de espectaculos existente en la bbdd
    
    espectaculos_bbdd_dataframe = pd.read_csv(path, encoding = "ISO-8859-1", keep_default_na=False)  # 
    print(f"\nCargando fichero histórico de espectáculos : {path}")
    
    
    for fila in espectaculos_bbdd_dataframe.iterrows():
        espectaculos_bbdd.append(tuple(fila[1])) # generamos una lista de tuplas. En el indice 0 se guarda el indice de fila
    
    
    # Sacamos los espectaculos nuevos que todavía no están en la bbdd
    # La unicidad de cada registro tanto en la bbdd existente como en el listado descargado se compone de 2 atributos: titulo + ubicacion
    titulo = 3
    ubicacion = 6
    
    espectaculos_uids = [atrib for atrib in ((espectaculo[titulo], espectaculo[ubicacion]) for espectaculo in espectaculos_original)]
    espectaculos_bbdd_uids = [atrib for atrib in ((espectaculo[titulo],espectaculo[ubicacion]) for espectaculo in espectaculos_bbdd)]
    
    total_nuevos_registros = len(set(espectaculos_uids) - set(espectaculos_bbdd_uids))

    # Identificamos los identificadores  que ya se encontraban en la bbdd pero no en el listado descargado
    # y que correspondería a los espectaculos antiguos
    for espectaculo in espectaculos_bbdd:
        
        identificador_registro = (espectaculo[titulo],espectaculo[ubicacion]) # id= Titulo + Ubicacion
        if identificador_registro not in espectaculos_uids:
            espectaculos_a_bbdd.append(tuple(espectaculo))
            
        
    # Identificamos el listado a cargar con los nuevos + la actualización de los que ya existían
    for espectaculo in espectaculos:
        espectaculo = [elem for elem in espectaculo]
        espectaculos_a_bbdd.append(tuple(espectaculo))
        
        #Extraemos el listado de registros nuevos exclusivamente 
        identificador_registro = (espectaculo[titulo],espectaculo[ubicacion]) # id= Titulo + Ubicacion
        if identificador_registro not in espectaculos_bbdd_uids: 
            espectaculos_nuevos.append(tuple(espectaculo))
    
    
    print(f"\nNuevos espectáculos agregados a bbdd: {total_nuevos_registros}")
    
    espectaculos_nuevos_dataframe = pd.DataFrame([espectaculo for espectaculo in espectaculos_nuevos], columns = atributos)
    
    espectaculos_a_bbdd_dataframe = pd.DataFrame([espectaculo for espectaculo in espectaculos_a_bbdd], columns = atributos)
    espectaculos_a_bbdd_dataframe.to_csv(path, index = False, encoding ="ISO-8859-1") # Modificado en v10    
        
except FileNotFoundError: 
    
    # El fichero csv no existe por lo que procedemos a generarlo
    # Guardamos la primera carga en archivo csv
    crear_csv(path, espectaculos, atributos) # Añadido en version-04
    print(f"\nCreando nuevo fichero de bbdd en : {path}")


# DataFrame donde se encuentra todo el listado de registros descaragado
espectaculos_dataframe = pd.DataFrame([espectaculo for espectaculo in espectaculos],
                                      columns = atributos)