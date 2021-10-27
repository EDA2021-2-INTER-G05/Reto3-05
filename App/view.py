"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    return controller.loadData(catalog)


def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Contar avistamientos en una ciudad")
    print("2- Contar avistamientos por duración")
    print("3- Contar avistamientos por Hora/Minutos del día (info arbol para lab 8)")
    print("4- Contar los avistamientos en un rango de fechas")
    print("5- Contar los avistamientos de una zona geográfica")
    print("6- Visualizar los avistamientos de una zona geográfica")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        start_time = time.process_time()
        catalog = initCatalog()
        numero = loadData(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Se han cargado los datos exitosamente.")
        print("Se cargaron "+ str(numero)+ " avistamientos")
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 2:
        pass
    
    elif int(inputs[0]) == 3:
        print("Para este requerimiento se creo una tabla de hash como llave cada ciudad y valor un arbol ordenado con llaves el datetime y valores los avistamientos. Por lo tanto no se puede mostrar una única altura, ya que hay un árbol por ciudad.")
        print("De esta manera se combina la búsqueda O(1) de las tablas de hash, y la eficiencia de la organización de los árboles.")

    else:
        sys.exit(0)
sys.exit(0)
