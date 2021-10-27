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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import datetime 

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog():
    catalog = mp.newMap(loadfactor=4)
    mp.put(catalog,"Ciudades",mp.newMap(loadfactor=4))
    return catalog


# Funciones para agregar informacion al catalogo

def subirAvistamiento(catalog,entrada):
    avistamiento = nuevoAvistamiento(entrada)
    añadirAvistamiento(avistamiento,catalog)

def añadirAvistamiento(avistamiento,catalog):
    add_or_create_in_om(mp.get(catalog,"Ciudades")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Dia")["value"],avistamiento)

def add_or_create_in_om(mapa,llave_mapa,llave_arbol,valor):
    if mp.contains(mapa,llave_mapa):
        arbol = mp.get(mapa,llave_mapa)["value"]
        lista = om.get(arbol,llave_arbol)["value"]
        lt.addLast(lista,valor)

    else:
        mp.put(mapa,llave_mapa,om.newMap())
        arbol = mp.get(mapa,llave_mapa)["value"]
        om.put(arbol,llave_arbol,lt.newList())
        lista = om.get(arbol,llave_arbol)["value"]
        lt.addLast(lista,valor)

# Funciones para creacion de datos

def nuevoAvistamiento(entrada):
    avistamiento = mp.newMap(loadfactor=4)
    mp.put(avistamiento,"Ciudad",entrada["city"])
    mp.put(avistamiento,"Dia",entrada["datetime"])
    mp.put(avistamiento,"Duracion",entrada["duration (seconds)"])
    mp.put(avistamiento,"Forma",entrada["shape"])
    return avistamiento


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
