# Hago la petición HTTP al servidor e imprimo el codigo de la respuesta

url = "https://www.atrapalo.com/entradas/home_nacional/" 
r = requests.get(url)
print ("We got a {} response code from {}".format(r.status_code, url))

# Respuesta: We got a 403 response code from https://www.atrapalo.com/entradas/home_nacional/

# Por lo que hay que editar los headers

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
