# Web_Scraping_PR1_UOC

## Autores: Gabriel Peso Bañuelos, Jon Ortiz Abalia

## Descripción

Práctica 1 (Web Scraping) enmarcada dentro de la asignatura "Tipología y ciclo de vida de los datos" (Máster de Ciencia de Datos, UOC, 2019). Consiste en extraer datos sobre espectáculos a partir de plataformas *online* de venta de entradas mediante la técnica de *Web Scraping*. Como prueba de concepto se ha generado el código para extraer los datos de la plataforma **Atrapalo.com**.

## Ficheros

**espectaculos.py**: documento con el código necesario para realizar el web scraping
**espectaculos.csv**: fichero csv con el dataset obtenido a partir de Atrapalo
**PR1_Peso_Ortiz.pdf**: documento pdf con las respuestas de la Práctica
**nube_palabras.png**: imagen incluida en el documento pdf

## Consideraciones

El código sería extrapolable a otras páginas Web, en cuyo caso habría que modificar el código que identifica los distintos atributos en el mapa HTML de la página, además del propio nombre de los atributos.

El código se ha diseñado pensando en una primera carga inicial de datos y unas cargas posteriores de periodicidad diaria. En cada una de éstas se realiza una carga parcial de las secciones (o tipos de espectáculo) disponibles en la página web.

## Recursos

* Subirats, L., Calvo, M. (2018). **Web Scraping**. Editorial UOC.
* Lawson, R. (2015). **Web Scraping with Python**. Packt Publishing Ltd. Chapter 2. Scraping the Data.
* Brody, H (2017). **The Ultimate Guide to Web Scraping**. Leanpub


