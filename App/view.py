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

from datetime import datetime
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time
from prettytable import PrettyTable
from DISClib.ADT import map as mp


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

def print_avistamientos_ciudad(lista,numero,tiempo):
    tabla = PrettyTable()
    tabla.field_names = ["Fecha y hora", "Ciudad", "Pais","Duración","Forma"]
    for avistamiento in lt.iterator(lista):
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"]])
    
    print("Hubo avistamintos en " + str(numero) + " ciudades diferentes.")
    print("Para esta ciudad, los 3 primeros y 3 últimos avistamientos fueron: ")
    print(tabla)
    print("Tiempo requerido " + str(tiempo)+ " mseg")

def print_datos(numero,primeros,ultimos):
    print("Se cargaron "+str(numero)+" avistamientos")

    print("Los primeros 5 datos cargados fueron: ")
    tabla = PrettyTable()
    tabla.field_names = ["Fecha y hora", "Ciudad", "Pais","Duración","Forma"]
    for avistamiento in lt.iterator(primeros):
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"]])
    print(tabla)

    print("Los últimos 5 fueron: ")
    tabla = PrettyTable()
    tabla.field_names = ["Fecha y hora", "Ciudad", "Pais","Duración","Forma"]
    for avistamiento in lt.iterator(ultimos):
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"]])
    print(tabla)

def print_avistamientos_hora(lista,llave_max,conteo_max):
    print("El número de avistamientos a la hora más tarde fue: ")
    tabla = PrettyTable()
    tabla.field_names = ["Hora", "Conteo"]
    tabla.add_row([str(llave_max[0])+":"+str(llave_max[1]),conteo_max])
    print(tabla)

    print("Hay un total de "+str(lt.size(lista))+" avistamientos en el rango de horas.")
    print("Los 3 primeros y 3 últimos avistamientos del rango son: ")
    tabla = PrettyTable()
    tabla.field_names = ["Fecha y hora", "Ciudad", "Pais","Duración","Forma"]

    for i in range(1,4):
        avistamiento = lt.getElement(lista,i)
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"]])

    for i in range(lt.size(lista)-2,lt.size(lista)+1):
        avistamiento = lt.getElement(lista,i)
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"]])
    print(tabla)
    
    

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Contar avistamientos en una ciudad")
    print("2- Contar avistamientos por duración")
    print("3- Contar avistamientos por Hora/Minutos del día")
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
        datos = loadData(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Se han cargado los datos exitosamente.")
        print_datos(datos[0],datos[1],datos[2])
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 1:
        ciudad = input("Ingrese la ciudad que se quiere consultar: ").strip()
        start_time = time.process_time()
        resultado = controller.avistamientos_ciudad(catalog,ciudad)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_avistamientos_ciudad(resultado[0],resultado[1],elapsed_time_mseg)
    
    elif int(inputs[0]) == 3:
        hora_menor = input("Ingrese la hora del límite inferior (HH:MM): ")+":00"
        hora_menor = datetime.strptime(hora_menor,"%X")
        hora_menor = (hora_menor.hour,hora_menor.minute)
        hora_mayor = input("Ingrese la hora del límite superior (HH:MM): ")+":00"
        hora_mayor = datetime.strptime(hora_mayor,"%X")
        hora_mayor = (hora_mayor.hour,hora_mayor.minute)

        start_time = time.process_time()
        resultado = controller.avistamientos_hora(catalog,hora_menor,hora_mayor)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_avistamientos_hora(resultado[0],resultado[1],resultado[2])
        print("Tiempo requerido "+str(elapsed_time_mseg)+" mseg")
        
        

    else:
        sys.exit(0)
sys.exit(0)
