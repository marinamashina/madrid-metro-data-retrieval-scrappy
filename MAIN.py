# -*- coding: utf-8 -*-
"""
Spyder Editor

Obtención de datos
"""
import csv
import subprocess
import json
import codecs
import os
import os.path

subprocess.run('scrapy crawl lineas -t csv -o - > files/output/lineas.csv', shell=True)
subprocess.run('scrapy crawl lineas_ML -t csv -o - > files/output/lineas_ML.csv', shell=True)
subprocess.run('python PROCESSOR.py', shell=True)
