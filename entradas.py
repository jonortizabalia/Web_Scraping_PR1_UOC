# Importamos librerías
from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib.request import urlopen
from urllib.error import URLError
import re

# Editamos los parámetros de los "headers" para hacer la petición  de HTTP
import requests
headers={
    "Accept": "*/*",
    "Content-Encoding": "gzip",
    "Cache-Control": "max-age=1206531",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

# Hacemos la petición HTTP al servidor 
r = requests.get("https://www.atrapalo.com/entradas/home_nacional/", headers=headers)
#print ("We got a {} response code from {}".format(r.status_code, url))
#print (r.text)

# Utilizamos la librería BeautifulSoup para parsear el HTML y convertirlo en DOM (Document Object Model)
soup = BeautifulSoup(r.text, "html.parser")
