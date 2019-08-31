# -*- coding: utf-8 -*-
"""
Spyder Editor

Obtención de datos
"""

import csv
import os
import pandas as pd
import re
import unicodedata
import codecs

# Abrimos los ficheros GTFS (stops.txt) de cada tipo de transporte:
archivo_metro_ligero = open("files/google_transit_M10/stops.txt", "r")
archivo_metro = open("files/google_transit_M4/stops.txt", "r")

# Abrimos/creamos para escritura dos ficheros vacios por cada tipo 
# de transporte:
stops_metro = open('files/input/stops_metro.csv', 'w')
stops_ML = open('files/input/stops_ML.csv', 'w')

# Función para pasar a csv los ficheros txt arriba mencionados:
def txt2csv(inp, output):
    try:
        stripped = (line.strip() for line in inp)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(output)
        writer.writerows(lines)
    finally:
        inp.close()
        output.close()

# Pasamos a csv los dos ficheros GTFS:
txt2csv(archivo_metro, stops_metro)
txt2csv(archivo_metro_ligero, stops_ML)

# Función para quitar acentos, unificando el formato de nombre de 
# estación a minúsculas y primera mayúscula.
def cambio_acentos(df, str):
	df[str] = df[str].str.lower()
	df[str]= df[str].str.replace("á", "a")
	df[str]= df[str].str.replace("é", "e")
	df[str]= df[str].str.replace("í", "i")
	df[str]= df[str].str.replace("ó", "o")
	df[str]= df[str].str.replace("ú", "u")
	df[str] = df[str].str.title()

# Fución que rellena con estacios en blanco aquellas filas que 
# no tengan info, por ejemploi en el caso de las paradas 
# (caso metro), o estaciones (caso de metro ligero).
def add_data(data):
	columnas = pd.DataFrame(data) 
	
	columnas.loc[:,'line'] = ' '
	columnas.loc[:,'stop_name'] = ' '
	columnas.loc[:,'station_sequence'] = ' '
	columnas.loc[:,'stop_url'] = ' '
	columnas.loc[:,'elevator'] = ' '
	columnas.loc[:,'escalator'] = ' '
	columnas.loc[:,'transport_type'] = ' '
	columnas.to_csv('files/output/DATOS.csv', mode='a', index=True, header=False,sep=',')

# Definimos el orden de las columnas del fichero resultado DATA.csv
columnsTitles = [
	'transport_type',
	'line',
	'stop_name',
	'stop_id',
	'stop_code',
	'stop_desc',
	'station_sequence',
	'stop_url',
	'stop_lat',
	'stop_lon',
	'stop_timezone',
	'zone_id',
	'location_type',
	'parent_station',
	'wheelchair_boarding',
	'elevator',
	'escalator'
]

# PREPROCESADO LINEAS.CSV
df_lineas = pd.read_csv("./files/output/lineas.csv")
# Creamos una columna para el tipo de transpore y le damos valor "Metro":
df_lineas.loc[:,'transport_type'] = 'Metro'
# Unificamos las minúsculas y los acentos del nombre de estación/parada:
cambio_acentos(df_lineas, 'stop_name')

# PREPROCESADO STOPS.CVS
df_stops_csv = pd.read_csv('files/input/stops_metro.csv')
# Unificamos las minúsculas y los acentos del nombre de estación/parada:
cambio_acentos(df_stops_csv, 'stop_name')
# Corregimos estaciones renombradas últimamente:
df_lineas['stop_name'] = df_lineas['stop_name'].str.replace("VICENTE ALEIXANDRE","Estadio Metropolitano")
df_lineas['stop_name'] = df_lineas['stop_name'].str.replace("ESTACIÓN DEL ARTE","Atocha Renfe")
cambio_acentos(df_stops_csv, 'stop_name')
# Nos quedamos solo con los datos de estaciones en el caso de Metro:
df_estaciones = df_stops_csv[df_stops_csv['stop_id'].str.startswith('est')]

# RESULTADO INTERMEDIO DE METRO
# Creamos un fichero intermedio para la escritura de resultado de Metro:
df_estaciones.to_csv('files/output/df_estaciones.csv', sep=',')
# Eliminamos la columna "stop_url" proveniente del fichero GTSF y creamos  
# una columna similar con la URL de cada parada/estación completa con el 
# dato de URL realtiva proveniente de scrapy.
df_estaciones.drop('stop_url', axis=1, inplace=True)
df_lineas.to_csv('files/output/df_lineas.csv', sep=',')
df_lineas['stop_url'] = "https://www.crtm.es" + df_lineas['stop_url'].map(str)
# Unificamos ambos ficheros por columna stop_name que es común en ambos 
# ficheros.
metro = df_lineas.merge(df_estaciones, on='stop_name')
# Ordenamos las lineas del fichero por orden de itinerario dentro de cada línea.
metro['line'] = metro['line'].astype(int)
metro = metro.sort_values(by=['line', 'station_sequence'])
metro = metro.reindex(columns=columnsTitles)


# PREPROCESADO LINEAS_ML.CSV
# Creamos un fichero intermedio para la escritura de resultado de Metro ligero:
df_lineas_ML = pd.read_csv("./files/output/lineas_ML.csv")
# Creamos una columna para el tipo de transpore y le damos valor "Metro Ligero"
df_lineas_ML.loc[:,'transport_type'] = 'Metro Ligero'
# Unificamos las minúsculas y los acentos del nombre de estación/parada:
cambio_acentos(df_lineas_ML, 'stop_name')

# PREPROCESADO ML_STOPS.CVS
df_stops_csv_ML = pd.read_csv('files/input/stops_ML.csv')
# Unificamos las minúsculas y los acentos del nombre de estación/parada:
cambio_acentos(df_stops_csv_ML, 'stop_name')
# Nos quedamos solo con los datos de paradas en el caso de Metro ligero:
df_estaciones_ML = df_stops_csv_ML[df_stops_csv_ML['stop_id'].str.startswith('par')]

# RESULTADO INTERMEDIO DE METRO LIGERO
# Creamos un fichero intermedio para la escritura de resultado de Metro ligero:
df_estaciones_ML.to_csv('files/output/df_estaciones_ML.csv', sep=',')
# Eliminamos la columna "stop_url" proveniente del fichero GTSF y creamos  
# una columna similar con la URL de cada parada/estación completa con el 
# dato de URL realtiva proveniente de scrapy.
df_estaciones_ML.drop('stop_url', axis=1, inplace=True)
df_lineas_ML.to_csv('files/output/df_lineas_ML.csv', sep=',')
df_lineas_ML['stop_url'] = "https://www.crtm.es" + df_lineas_ML['stop_url'].map(str)
# Unificamos ambos ficheros por columna stop_name que es común en ambos 
# ficheros.
metro_ML = df_lineas_ML.merge(df_estaciones_ML, on='stop_name')
# Ordenamos las lineas del fichero por orden de itinerario dentro de cada línea.
metro_ML['line'] = metro_ML['line'].astype(int)
metro_ML = metro_ML.sort_values(by=['line', 'station_sequence'])
metro_ML = metro_ML.reindex(columns=columnsTitles)

# Escribimos el fichero final:
DATOS_CSV = pd.concat([metro, metro_ML], ignore_index=True)
DATOS_CSV.to_csv('files/output/DATOS.csv', index=True, header=True,sep=',')


