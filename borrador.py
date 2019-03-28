## Petición HTTP al servidor

# Sin editar "headers":
url = "https://www.atrapalo.com/entradas/home_nacional/" 
r = requests.get(url)
print ("We got a {} response code from {}".format(r.status_code, url))

# Respuesta: We got a 403 response code from https://www.atrapalo.com/entradas/home_nacional/

# Editando "headers":
headers={
    "Accept": "*/*",
    "Content-Encoding": "gzip",
    "Cache-Control": "max-age=1206531",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

r = requests.get("https://www.atrapalo.com/entradas/home_nacional/", headers=headers)
print ("We got a {} response code from {}".format(r.status_code, url))

# Respuesta: We got a 200 response code from https://www.atrapalo.com/entradas/home_nacional/

## Web crawling
# Saco la lista de los tipos de espectáculo
categories = soup.find_all("option", {"class":"category"})
list_cat = []
for category in categories:
    list_cat.append(category.text.strip())
print(list_cat)

# Generamos los links con las categorías extraídas en el paso anterior
queue = []
for term in list_cat:
    url="https://www.atrapalo.com/entradas/home_nacional/%s/#buscador" % term
    queue.append(url)
print(queue)

# @Gabi, después de hacer esto del web crawling he visto que los links generados no funcionan ya que en vez de extraer el texto dentro de cada atributo "classs"
# habría que extraer el contenido del atributo "value"...y aún no lo he conseguido
