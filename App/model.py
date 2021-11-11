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
import datetime
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
    mp.put(catalog,"Duraciones",om.newMap())
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

    #Carga req 2

    add_list_in_om(mp.get(catalog,"Duraciones")["value"],mp.get(avistamiento,"Duracion")["value"],avistamiento)

    #Carga req 3
    fecha = mp.get(avistamiento,"Dia")["value"]
    llave = (fecha.hour,fecha.minute)
    add_list_in_om(mp.get(catalog,"Horas")["value"],llave,avistamiento)

    #Carga req 5
    add_or_create_om_in_om(mp.get(catalog,"Longitudes")["value"],mp.get(avistamiento,"Longitud")["value"],mp.get(avistamiento,"Latitud")["value"],avistamiento)

def newCatalog():
    catalog2 = {'maps': None,
               'ciudad' : None
    }
    catalog2['arbol'] = om.newMap(omaptype="RBT", comparefunction=Datos)
    catalog2['duraciones'] = om.newMap(omaptype="RBT", comparefunction=Datos) 
    catalog2['Fecha'] = om.newMap(omaptype="RBT", comparefunction=Datos) 
    return catalog2


def addavistamiento(catalog2,avistamiento):

    fecha = datetime.datetime.strptime(avistamiento["datetime"], "%Y-%m-%d %H:%M:%S")
    avistamiento['duration (seconds)'] = float(avistamiento['duration (seconds)']) 
    om.put(catalog2['arbol'], fecha, avistamiento)
    
    esta = om.contains(catalog2['duraciones'], avistamiento['duration (seconds)'])
    if not esta:
        orden = om.newMap(omaptype="BST", comparefunction=comparearbol)
        key = avistamiento['city'] + avistamiento['country']
        om.put(orden, key, avistamiento)
        om.put(catalog2['duraciones'], avistamiento['duration (seconds)'], orden)

    else:
        orden = om.get(catalog2['duraciones'], avistamiento['duration (seconds)'])['value']
        key = avistamiento['city'] + avistamiento['country']
        esta = om.contains(orden,key)
        if not esta:
            om.put(orden,key,avistamiento)
            om.put(catalog2['duraciones'], avistamiento['duration (seconds)'], orden)
        else:
            while esta:
                key = key + "a"
                esta = om.contains(orden,key)
                if esta: 
                    pass
                else:
                    om.put(orden,key,avistamiento)
                    om.put(catalog2['duraciones'], avistamiento['duration (seconds)'], orden)
    año = int(avistamiento["datetime"][0:4])    
    mes = int(avistamiento["datetime"][5:7])    
    dia = int(avistamiento["datetime"][8:10])
    fecha = datetime.date(año,mes,dia)
    esta2 = om.contains(catalog2["Fecha"],fecha)
    if not esta2:
        orden2 = om.newMap(omaptype="RBT", comparefunction=Datos)      
        om.put(orden2,fecha,avistamiento)
        om.put(catalog2["Fecha"], fecha, orden2)
    else:
        orden2 = om.get(catalog2["Fecha"], fecha)["value"]
        om.put(orden2,fecha,avistamiento)
        om.put(catalog2["Fecha"], fecha, orden2) 
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
    mp.put(avistamiento,"Dia",datetime.datetime.strptime(entrada["datetime"],"%Y-%m-%d %X"))
    mp.put(avistamiento,"Duracion",entrada["duration (seconds)"])
    if entrada["shape"] == "":
        mp.put(avistamiento,"Forma","*No especificado*")
    else:
        mp.put(avistamiento,"Forma",entrada["shape"])
    mp.put(avistamiento,"Pais",entrada["country"])
    mp.put(avistamiento,"Longitud",round(float(entrada["longitude"]),2))
    mp.put(avistamiento,"Latitud",round(float(entrada["latitude"]),2))

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

#req 2
def avistamientos_duracion(catalog2, duracion1, duracion2):
    min = float(duracion1)
    max = float(duracion2)
    duracion = catalog2['duraciones']
    size = om.size(duracion)
    ffinal = lt.newList()
    kmax = om.maxKey(duracion)
    maxi = om.get(duracion,kmax)["value"]
    sizemayor = om.size(maxi)
    dicct = {}
    dicct["llave"] = kmax
    dicct["valor"] = sizemayor
    lt.addLast(ffinal,dicct)
    datos = om.values(duracion,min,max)
    size2 = 0
    for x in lt.iterator(datos):
        size3 = om.size(x)
        size2 += size3
    keys = om.keys(duracion,min,max)
    minimax = lt.firstElement(keys)
    maximax = lt.lastElement(keys)
    aminima = om.get(duracion,minimax)["value"].copy()
    amaxima = om.get(duracion,maximax)["value"].copy()
    llfinal = lt.newList(datastructure="ARRAY_LIST")
    llmax= lt.newList()
    for x in range(3):
        kmin = om.minKey(aminima)
        minima = om.get(aminima,kmin)["value"]
        lt.addLast(llfinal,minima)
        om.deleteMin(aminima)
        kmax = om.maxKey(amaxima)
        maxima = om.get(amaxima,kmax)['value']
        lt.addFirst(llmax,maxima)
        om.deleteMax(amaxima)
    for i in lt.iterator(llmax):
        lt.addLast(llfinal,i)

    return (size,ffinal, size2,llfinal)
#fin req 2
def avistamientos_hora(catalog,hora_menor,hora_mayor):
    arbol = mp.get(catalog,"Horas")["value"]
    numero_hora_max = lt.size(om.get(arbol,om.maxKey(arbol))["value"])
    hora_menor = om.ceiling(arbol,hora_menor)
    hora_mayor = om.floor(arbol,hora_mayor)
    avistamientos = lt.newList("ARRAY_LIST")
    if hora_mayor != None and hora_menor != None:
        rango_horas = om.values(arbol,hora_menor,hora_mayor)
        contador = 0
        for hora in lt.iterator(rango_horas):
            contador += 1
            if contador < 4 or contador in range(lt.size(rango_horas)-2,lt.size(rango_horas)+1):
                mergesort.sort(hora,sort_time)

            for avistamiento in lt.iterator(hora):
                lt.addLast(avistamientos,avistamiento)
    
    return avistamientos,om.maxKey(arbol),numero_hora_max


#req 4
def contar_rango_fecha(catalog2, inferior, superior):
    añoinferior = int(inferior[0:4])
    mesinferior = int(inferior[5:7])
    diainferior = int(inferior[8:10])

    añosuperior = int(superior[0:4])
    mesuperior = int(superior[5:7])
    diasuperior = int(superior[8:10])

    dateinicio = datetime.date(añoinferior,mesinferior,diainferior)
    datefinal = datetime.date(añosuperior,mesuperior,diasuperior)
    
    
    obtener = om.keys(catalog2["Fecha"],dateinicio,datefinal)
    
    x = 0
    for z in lt.iterator(obtener):             
        a = om.get(catalog2["Fecha"],z)["value"]       
        x += om.size(a)

    
    ff1 = lt.newList(datastructure="ARRAY_LIST")

    for a in lt.iterator(obtener):
        puede = lt.size(ff1)
        if puede < 3:
            f = om.get(catalog2["Fecha"],a)["value"]["root"]["value"]
            lt.addLast(ff1,f)
        else:
            break
    
    ff2 = lt.newList(datastructure="ARRAY_LIST")
    ffinal = lt.size(obtener)

    for b in range(ffinal,0,-1):
        
        puede = lt.size(ff2)
        if puede < 3:
            j = lt.getElement(obtener,b)          
            h = om.get(catalog2["Fecha"],j)["value"]["root"]["value"]
            lt.addFirst(ff2,h)
        else:
            break
    return ff1,ff2,x
#fin req 4

def avistamientos_area(catalog,lon_min,lon_max,lat_min,lat_max):
    arbol_Lon = mp.get(catalog,"Longitudes")["value"]
    lista_retorno = lt.newList("ARRAY_LIST")
    
    lon_min = om.ceiling(arbol_Lon,lon_min)
    lon_max = om.floor(arbol_Lon,lon_max)

    if lon_min != None and lon_max != None:
        rango_lon = om.values(arbol_Lon,lon_min,lon_max)

        for arbol_Lat in lt.iterator(rango_lon):
            lat_min_in = om.ceiling(arbol_Lat,lat_min)
            lat_max_in = om.floor(arbol_Lat,lat_max)
            if lat_min_in !=None and lat_max_in != None:
                rango_lat = om.values(arbol_Lat,lat_min_in,lat_max_in)
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

def Datos(Datos1, Datos2):
   
    if (Datos1 == Datos2):
        return 0
    elif (Datos1>Datos2):
        return 1
    else:
        return -1

def comparearbol(date1,date2):
    x = min(date1,date2)
    if (date1 == date2):
        return 0
    elif x == date1:
        return -1
    elif x == date2:
        return 1

# Funciones de ordenamiento
