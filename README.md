# Web_Scraping_PR1_UOC

## Autores: Gabriel Peso Bañuelos, Jon Ortiz Abalia

## Descripción

Práctica 1 (Web Scraping) enmarcada dentro de la asignatura "Tipología y ciclo de vida de los datos" (Máster de Ciencia de Datos, UOC, 2019). Consiste en extraer datos sobre espectáculos a partir de plataformas *online* de venta de entradas mediante la técnica de *Web Scraping*. Como prueba de concepto se ha generado el código para extraer los datos de la plataforma **Atrapalo.com**.

## Ficheros

- **espectaculos.py**: documento con el código necesario para realizar el web scraping
- **espectaculos.csv**: fichero csv con el dataset obtenido a partir de Atrapalo
- **PR1_Peso_Ortiz.pdf**: documento pdf con las respuestas de la Práctica

## Consideraciones

* Conceptualmente el código está diseñado para poder **extrapolar** el mecanismo de *web scraping* a otros sites de venta online  y así conseguir una base de datos (bbdd) global actual e histórica de todo el panorama de espectáculos a nivel nacional .

* En cada descarga la bbdd obtenida mantiene toda la **información histórica** descargada hasta el momento, al tiempo que **actualiza** la vigente y **añade** los nuevos espectáculos detectados. 

* El código implementa diferentes aspectos que pretenden evitar los posibles bloqueos del *site* al tiempo que es respetuoso con el mismo para que nuestras descargas sean lo menos intrusivas posible. Así, desde el punto de vista de **antibloqueo** se modifican las cabeceras http con el parámetro super-agent y se implementa un mecanismo de N reintentos espaciados en intervalos de X segundos en el supuesto de que el site nos bloquee temporalmente.

* En paralelo, y desde el punto de vista del respeto al que hacíamos mención,  se incluye durante la descarga un mecanismo de **supervisión del fichero *robots.txt*** para asegurar que nuestra actividad no es contraria a la política del site y nos alerte en caso contrario. 

* Las descargas masivas se han evitado mediante una rutina automática de **descargas diarias incrementales** que aseguran que cada día de la semana se descarguen sólo ciertas secciones de espectáculos completando toda la cartelera cada siete días.

## Recursos

* Subirats, L., Calvo, M. (2018). **Web Scraping**. Editorial UOC.
* Lawson, R. (2015). **Web Scraping with Python**. Packt Publishing Ltd. Chapter 2. Scraping the Data.
* Brody, H (2017). **The Ultimate Guide to Web Scraping**. Leanpub


