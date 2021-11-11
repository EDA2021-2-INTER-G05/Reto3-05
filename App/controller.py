"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import queue as que


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def initCatalog():
    catalog = model.initCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    numero = Cargaravisamientos(catalog)
    return numero

def Cargaravisamientos(catalog):
    file = cf.data_dir + "UFOS-utf8-small.csv"
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    numero = 0
    primeros_5 = lt.newList()
    ultimos_5 = que.newQueue()
    for avistamiento in input_file:
        numero += 1
        model.subirAvistamiento(catalog,avistamiento,numero,primeros_5,ultimos_5)
    
    return numero, primeros_5,ultimos_5

def init2():
    catalog = model.newCatalog()
    return catalog



def loadData2(catalog2):
    archivo = cf.data_dir + "UFOS-utf8-small.csv"
    input_file = csv.DictReader(open(archivo, encoding="utf-8"),
    delimiter = ",")
    for ufo in input_file:
        model.addavistamiento(catalog2,ufo)
    return catalog2

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def avistamientos_ciudad(catalog,ciudad):
    return model.avistamientos_ciudad(catalog,ciudad)

def avistamientos_duracion(catalog2,duracion1,duracion2):
    return model.avistamientos_duracion(catalog2,duracion1,duracion2)

def avistamientos_hora(catalog,hora_menor,hora_mayor):
    return model.avistamientos_hora(catalog,hora_menor,hora_mayor)

def contar_rango_fecha(catalog2, inferior, superior):
    return model.contar_rango_fecha(catalog2, inferior, superior)
    
def avistamientos_area(catalog,lon_min,lon_max,lat_min,lat_max):
    return model.avistamientos_area(catalog,lon_min,lon_max,lat_min,lat_max)
