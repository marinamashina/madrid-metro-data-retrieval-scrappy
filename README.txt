1. Prerrequisitos.
Para ejecutar este programa hemos usado los siguientes import de paquetes de Python:
	import csv
	import subprocess
	import json
	import codecs
	import os
	import pandas as pd
	import re
	import unicodedata
	import codecs
Los sistemas operativos que soporta este programa son Linux y Mac.

2. Ejecución.
Para ejecutar el programa, lanzar el código MAIN.py mediante el siguiente comando en la shell 
en el mismo directorio donde se encuentra este README. Dicho programa MAIN.py a su vez lanza 
un subproceso por cada tipo de scrapy y finalmente el código de postprocesado de los 
resultados de scrapy y ficheros GTFS.

$ python MAIN.py

3. Resultados.
En la carpeta files/output se generará un archivo DATOS.csv que será el resultado de esta práctica. 
Los ficheros lineas.csv y lineas_ML.csv de resultado de scrapy se generarán como resultado intermedio en la misma carpeta.
El diagrama UML se encuentra dentro de la misma carpeta que este README.
