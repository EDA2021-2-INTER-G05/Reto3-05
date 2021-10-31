﻿"""
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


from DISClib.DataStructures.bst import select
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort 
from DISClib.Algorithms.Sorting import mergesort
from DISClib.Algorithms.Sorting import insertionsort 
assert cf
from datetime import datetime 
from DISClib.Algorithms.Trees import traversal as tra
from DISClib.ADT import queue as que

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog():
    catalog = mp.newMap(loadfactor=4)
    mp.put(catalog,"Ciudades",mp.newMap(loadfactor=4))
    mp.put(catalog,"Horas",om.newMap())
    mp.put(catalog,"Longitudes",om.newMap())
    return catalog


# Funciones para agregar informacion al catalogo

def subirAvistamiento(catalog,entrada,numero,primeros_5,ultimos_5):
    avistamiento = nuevoAvistamiento(entrada)
    añadirAvistamiento(avistamiento,catalog)
    if numero <6:
        lt.addLast(primeros_5,avistamiento)
    else:
        if que.size(ultimos_5) < 5:
            que.enqueue(ultimos_5,avistamiento)
        else:
            que.dequeue(ultimos_5)
            que.enqueue(ultimos_5,avistamiento)

def añadirAvistamiento(avistamiento,catalog):
    
    #Carga req 1
    add_or_create_in_om(mp.get(catalog,"Ciudades")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Dia")["value"],avistamiento)

    #Carga req 3
    fecha = mp.get(avistamiento,"Dia")["value"]
    llave = (fecha.hour,fecha.minute)
    add_list_in_om(mp.get(catalog,"Horas")["value"],llave,avistamiento)

    #Carga req 5
    add_or_create_om_in_om(mp.get(catalog,"Longitudes")["value"],mp.get(avistamiento,"Longitud")["value"],mp.get(avistamiento,"Latitud")["value"],avistamiento)

def add_or_create_in_om(mapa,llave_mapa,llave_arbol,valor):
    if mp.contains(mapa,llave_mapa):
        arbol = mp.get(mapa,llave_mapa)["value"]
        lista = om.get(arbol,llave_arbol)
        if lista == None:
            om.put(arbol,llave_arbol,lt.newList("ARRAY_LIST"))
            lista = om.get(arbol,llave_arbol)
        lista = lista["value"]
        lt.addLast(lista,valor)

    else:
        mp.put(mapa,llave_mapa,om.newMap())
        arbol = mp.get(mapa,llave_mapa)["value"]
        om.put(arbol,llave_arbol,lt.newList("ARRAY_LIST"))
        lista = om.get(arbol,llave_arbol)["value"]
        lt.addLast(lista,valor)

def add_list_in_om(arbol,llave_arbol,valor):
    if om.contains(arbol,llave_arbol):
        lista = om.get(arbol,llave_arbol)["value"]
        lt.addLast(lista,valor)
    else:
        om.put(arbol,llave_arbol,lt.newList())
        lista = om.get(arbol,llave_arbol)["value"]
        lt.addLast(lista,valor)

def add_or_create_om_in_om(arbol,llave_arbol1,llave_arbol2,valor):
    if om.contains(arbol,llave_arbol1):
        arbol2 = om.get(arbol,llave_arbol1)["value"]
        if om.contains(arbol2,llave_arbol2):
            lista = om.get(arbol2,llave_arbol2)["value"]
            lt.addLast(lista,valor)
        else:
            om.put(arbol2,llave_arbol2,lt.newList("ARRAY_LIST"))
            lista = om.get(arbol2,llave_arbol2)["value"]
            lt.addLast(lista,valor)
    
    else:
        om.put(arbol,llave_arbol1,om.newMap())
        arbol2=om.get(arbol,llave_arbol1)["value"]
        om.put(arbol2,llave_arbol2,lt.newList("ARRAY_LIST"))
        lista = om.get(arbol2,llave_arbol2)["value"]
        lt.addLast(lista,valor)
        


# Funciones para creacion de datos

def nuevoAvistamiento(entrada):
    avistamiento = mp.newMap(loadfactor=4)
    mp.put(avistamiento,"Ciudad",entrada["city"])
    mp.put(avistamiento,"Dia",datetime.strptime(entrada["datetime"],"%Y-%m-%d %X"))
    mp.put(avistamiento,"Duracion",entrada["duration (seconds)"])
    if entrada["shape"] == "":
        mp.put(avistamiento,"Forma","*No especificado*")
    else:
        mp.put(avistamiento,"Forma",entrada["shape"])
    mp.put(avistamiento,"Pais",entrada["country"])
    mp.put(avistamiento,"Longitud",format(round(float(entrada["longitude"]),2),".2f"))
    mp.put(avistamiento,"Latitud",format(round(float(entrada["latitude"]),2),".2f"))

    return avistamiento


# Funciones de consulta

def avistamientos_ciudad(catalog,ciudad):
    datos = mp.get(catalog,"Ciudades")["value"]
    numero_ciudades = lt.size(mp.keySet(datos))
    arbol = mp.get(datos,ciudad)["value"]

    fechas = tra.inorder(arbol)
    avistamientos = lt.newList("ARRAY_LIST")
    for fecha in lt.iterator(fechas):
        for avistamiento in lt.iterator(fecha):
            lt.addLast(avistamientos,avistamiento)

    lista = lt.newList("ARRAY_LIST")

    if lt.size(avistamientos) > 6:
        for i in range(1,4):
            elemento = lt.getElement(avistamientos,i)
            lt.addLast(lista,elemento)
        
        for i in range(lt.size(avistamientos)-2,lt.size(avistamientos)+1):
            elemento = lt.getElement(avistamientos,i)
            lt.addLast(lista,elemento)
    
    else:
        lista = avistamientos

    return lista, numero_ciudades

def avistamientos_hora(catalog,hora_menor,hora_mayor):
    arbol = mp.get(catalog,"Horas")["value"]
    numero_hora_max = lt.size(om.get(arbol,om.maxKey(arbol))["value"])

    hora_menor = om.ceiling(arbol,hora_menor)
    hora_mayor = om.floor(arbol,hora_mayor)
    rango_horas = om.values(arbol,hora_menor,hora_mayor)
    avistamientos = lt.newList("ARRAY_LIST")

    contador = 0
    for hora in lt.iterator(rango_horas):
        contador += 1
        if contador < 4 or contador in range(lt.size(rango_horas)-2,lt.size(rango_horas)+1):
            mergesort.sort(hora,sort_time)

        for avistamiento in lt.iterator(hora):
            lt.addLast(avistamientos,avistamiento)
    
    return avistamientos,om.maxKey(arbol),numero_hora_max


def avistamientos_area(catalog,lon_min,lon_max,lat_min,lat_max):
    arbol_Lon = mp.get(catalog,"Longitudes")["value"]
    lon_min = om.ceiling(arbol_Lon,lon_min)
    lon_max = om.floor(arbol_Lon,lon_max)

    lista_retorno = lt.newList("ARRAY_LIST")
    rango_lon = om.values(arbol_Lon,lon_min,lon_max)
    for arbol_Lat in lt.iterator(rango_lon):
        lat_min = om.ceiling(arbol_Lat,lat_min)
        lat_max = om.floor(arbol_Lat,lat_max)
        rango_lat = om.values(arbol_Lat,lat_min,lat_max)
        for latitud in lt.iterator(rango_lat):
            for avistamiento in lt.iterator(latitud):
                lt.addLast(lista_retorno,avistamiento)
    
    return lista_retorno
        

# Funciones utilizadas para comparar elementos dentro de una lista

def sort_time(av1,av2):
    if mp.get(av1,"Dia")["value"] <mp.get(av2,"Dia")["value"]:
        return True
    else:
        return False

# Funciones de ordenamiento
