### VARIABLES ###

## Novedad
novedad = []
for espectaculo in espectaculos:
    if espectaculo.find(class_="sticker-box sticker-new"):
        novedad.append("NOVEDAD")
    else:
        novedad.append("NA")
# Comprobación: el espectáculo nº31 tiene que salir como "NOVEDAD"
print(novedad[0:35])

## Nombre espectáculo
nombreEspectaculo = []
for espectaculo in espectaculos:
    nombre = espectaculo.find(class_="clear nombre").text.strip()
    NombreEspectaculo.append(nombre)
# Compruebo las primeras 20
print(NombreEspectaculo[0:20])

## Localidad 
localidad = []
for espectaculo in espectaculos:
    a = espectaculo.find("p", class_="info").span.text.strip()
    b = re.findall("\(.*\)",a)
    c = b[0]
    d = re.sub('[(){}<>]', '', c)
    localidad.append(d)
# Compruebo las primeras 20
print(localidad[0:20])

## Categoría
categoria = []
for espectaculo in espectaculos:
    nombre = espectaculo.find(class_="type large-loc").text.strip() 
    categoria.append(nombre)                  
# Compruebo las primeras 20
print(categoria[0:20])

## Público
publico = []
for espectaculo in espectaculos:
    nombre = espectaculo.find(class_="item-tag").text.strip() 
    publico.append(nombre)                  
# Compruebo las primeras 20
print(publico[0:20])

## Precio
precio = []
for espectaculo in espectaculos:
    valor = espectaculo.find(class_="status-label").text.strip() 
    #num = re.sub('€', '', valor)
    precio.append(valor)                 
# Compruebo las primeras 20
print(precio[0:20])

## Descuento
descuento = []
for espectaculo in espectaculos:
    if espectaculo.find(class_="status-label"):
        desc = espectaculo.find(class_="status-label").span.text
        descuento.append(desc)
    else:
        descuento.append("NA")
# Compruebo las primeras 20
print(descuento[0:20])

## Puntuacion, valoración y número de opiniones
# NO ESTAN DISPONIBLES EN LA RESPUESTA DEL SERVIDOR!!
# class ="opi-rating", class="opi-title" y class="show-ratings"

