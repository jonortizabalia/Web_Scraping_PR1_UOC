'''
LIBRERIAS
'''

import requests
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import datetime
import random
import re
import csv
import os
import time   # v05 
import getpass #v05 Necesraio para detectar el user loggeado actualmente en el sistema

# ahora = datetime.datetime.now()
# ahora.year

'''
VARIABLES
'''

######## Codigo PERSONAL###############
proxy_on = False

proxies_home = None
proxies_work = {
    "http": (removed) ,
    "https": (removed),
}

if proxy_on:
    proxies = proxies_work
else:
    proxies = proxies_home
########################################

headers={
    "Accept": "*/*",
    "Content-Encoding": "gzip",
    "Cache-Control": "max-age=1206531",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

URL = "https://www.atrapalo.com/entradas/"

SECCIONES = {'teatro-y-danza' : 'Teatro y Danza', 
           'musica': 'Música', 
           'parques-tematicos': 'Parques temáticos', 
            'musicales': 'Musicales',
            'museos-y-exposiciones':'Museos y Exposiciones',
            'deportes':'Deportes',
            'circo': 'Circo',
            'cine': 'Cine',
            'ferias':'Ferias'}


#SECCIONES = {'teatro-y-danza' : 'Teatro y Danza'}
#SECCIONES = {'teatro-y-danza' : 'Teatro y Danza', 'circo' : 'Circo','musica': 'Música'}
SECCIONES = {'circo' : 'Circo'}

#atributos = ["Titulo","Categoria","Novedad","Ubicación","Localidad","Precio","Descuento", # -Añadida en v04
#                     "Fechas", "Fecha_inicio", "Fecha_fin","Duracion","Idioma","Publico",
#                     "Puntuación","Valoración","Opiniones"]

# v05  Añadidos nuevos atributos Captura, Web, Evento
atributos = ["Captura", "Web", "Evento", 
             "Titulo","Categoria","Novedad","Ubicación","Localidad","Precio","Descuento", 
             "Fechas", "Fecha_inicio", "Fecha_fin","Duracion","Idioma","Publico",
             "Puntuación","Valoración","Opiniones"]

origen = 'Atrapalo'    # Añadido en  v05

# path = "C:/Users/Usuario/Desktop/output.csv" # -Añadida en v04

fichero_csv = 'output.csv'
# v05. Permite obviar el usuario con el que se haya loggeado el usuario en el sistema
path = "C:/Users/" + getpass.getuser() + "/Desktop/" + fichero_csv  # Añadido v05

# Estas variables sirven para controlar el número de registros a descargar
modo_prueba = False
pantallazos = 2  #100 registros de pruebas (5 pantallazos x 20 registros)

'''
FUNCIONES
'''

'''
DESCRIPCIÓN: 
Función a la que se le pasa la URL de la web ATRAPALO para que se descargue todos los espectaculos que se listan
en el apartado de 'entradas' 

    INPUT: 
        url (string) : URL de Atrapalo   
    
    OUTPUT: 
        nuevos_espectaculos (list): lista con todos los espectaculos encontrados

''' 

def Sacar_espectaculos(url):
    
    # Leemos espectaculos de la url indicada
    respuesta = requests.get(url, proxies=proxies, headers=headers)
    status = "Correcto" if respuesta.status_code else "Error"
    # print("Rta:",respuesta.status_code)  # -Obseleto v02
    
    
    # Parseamos la respuesta para sacar los contenedores de cada espectaculo
    soup = BeautifulSoup(respuesta.content, "html.parser")
    url_espectaculos = soup.find_all(class_="card-result-container")    
    
    # Mostramos msg y devolvemos resultado
    #print(f"Descargando URL: {url} | Espectaculos Leidos: {len(nuevos_espectaculos)} | Status: {status}")  #Obsoleto v07
    return(url_espectaculos, status)  # v07. Devolvemos tb el estado de la operación
    
    
'''
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
    
    # Captura  v05
    captura = time.strftime("%d/%m/%Y %H:%M")   #Fecha de hoy en formato dd/mm/aa  HH:MM
    
    # Web v05
    web = origen
    
    # seccion  v05
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
    try: #ubicacion = espectaculo.find_all(class_="info")[0].find('a').text.strip()
         ubicacion = espectaculo.find_all(class_="info")[0].span.text.strip("\n").strip().split("\n")[0] # v09
    except: ubicacion = ""    
    
    # Localidad (Modificada en v06)
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
        
    # Duracion (modificada en versión v06)
    try: #duracion = espectaculo.find_all(class_="info")[2].get_text().strip('\n').strip() 
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

# Función añadida en -version 04
''' 
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
            
'''
PROGRAMA PRINCIPAL
'''

espectaculos = []  # Variable donde cargaremos inicialmente todos los registros que nos descargamos
espectaculos_pantalla_anterior = []  #Variable temporal que sirve para el flujo del programa
espectaculos_bbdd = []    # Variable donde cargaremos todos los registros acumulados en la bbdd actual (fichero .csv)
espectaculos_a_bbdd = []  #  Variable donde almacenaremos todos los registros a volcar a la bbdd
espectaculos_nuevos = []  # Guardamos los registros nuevos descargados que no estaban en la bbdd

#espectaculos_dataframe   Variable donde tenemos el dataframe de todos los espectaculos descargados
#espectaculos_bbdd_dataframe Variable donde tenemos el dataframe de todos los espectaculos de la bbdd actual, previo a la descarga
#espectaculos_nuevos_dataframe  Variable donde tenemos el dataframe de todos los espectaculos estrictamente nuevos 
#espectaculos_a_bbdd_dataframe  Variable con todos los registros que escribiremos en la bbdd

print(f"Iniciando proceso de descarga.....\n")
for seccion in SECCIONES:
    cont = 1
    seguir_buscando = True
    while seguir_buscando:
        if cont == 0:
            url = URL + seccion + '/'
        else: 
            url = URL + seccion + '/' + 'p-' + str(cont) + '/'
        cont += 1
    
        
        # Controlamos si nos descargamos todos los registros de cada sección o solo unos de prueba
        if modo_prueba and cont == (pantallazos + 1):
            
            seguir_buscando = False
        
        espectaculos_pantalla, status = Sacar_espectaculos(url) # v07 capturamos 2 valores de la función
        
        if espectaculos_pantalla == espectaculos_pantalla_anterior:
            seguir_buscando = False
        else:
            
            print(f"Descargando URL: {url} | Espectaculos Leidos: {len(espectaculos_pantalla)} | Status: {status}") # v07 se saca de la fn
            
            
            for espectaculo in espectaculos_pantalla:
                
                #La lista de espectaculos se compondrá de las tuplas correspondientes a cada espectaculo
                espectaculos.append(Sacar_atributos(espectaculo))   # - Nuevo v07. Quitamos el campo Captura
            
            espectaculos_pantalla_anterior = espectaculos_pantalla 
    


print(f"\n Finalizado proceso. Espectaculos descargados: {len(espectaculos)}")
espectaculos_original = espectaculos

# Procedemos a salvar la informacion a fichero
try: 
    
    # Leemos el historico de espectaculos existente en la bbdd
    
    
    espectaculos_bbdd_dataframe = pd.read_csv(path, encoding = "ISO-8859-1", keep_default_na=False)  # 
    print(f"\n Cargando fichero histórico de espectáculos : {path}")
    
    
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
            
            #print(tuple(espectaculo))
            
        
    # Identificamos el listado a cargar con los nuevos + la actualización de los que ya existían
    for espectaculo in espectaculos:
        espectaculo = [elem for elem in espectaculo]
        espectaculos_a_bbdd.append(tuple(espectaculo))
        
        #Extraemos el listado de registros nuevos exclusivamente 
        identificador_registro = (espectaculo[titulo],espectaculo[ubicacion]) # id= Titulo + Ubicacion
        if identificador_registro not in espectaculos_bbdd_uids: 
            espectaculos_nuevos.append(tuple(espectaculo))
            #print(identificador_registro)
    
    
    print(f"\n Nuevos espectáculos agregados a bbdd: {total_nuevos_registros}")
    
    espectaculos_nuevos_dataframe = pd.DataFrame([espectaculo for espectaculo in espectaculos_nuevos], columns = atributos)
    
    espectaculos_a_bbdd_dataframe = pd.DataFrame([espectaculo for espectaculo in espectaculos_a_bbdd], columns = atributos)
    espectaculos_a_bbdd_dataframe.to_csv(path, index = False, encoding ="ISO-8859-1") # Modificado en v10    
        
except FileNotFoundError: 
    
    # El fichero csv no existe por lo que procedemos a cargarlo
    # Guardamos la primera carga en archivo csv
    crear_csv(path, espectaculos, atributos) # Añadido en version-04
    print(f"\n Creando nuevo fichero de bbdd en : {path}")


# DataFrame donde se encuentra todo el listado de registros descaragado
espectaculos_dataframe = pd.DataFrame([espectaculo for espectaculo in espectaculos],
                                      columns = atributos)
