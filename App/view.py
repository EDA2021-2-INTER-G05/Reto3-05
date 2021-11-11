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
from DISClib.ADT import orderedmap as mo
from prettytable import PrettyTable
from DISClib.ADT import map as mp
from prettytable.prettytable import ALL


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
    
def print_avistamientos_area(lista):
    print("El total de avistamientos en esa área es: " + str(lt.size(lista)))
    tabla = PrettyTable(hrules = ALL)
    tabla.field_names = ["Fecha y hora", "Ciudad", "Pais","Duración","Forma","Longitud","Latitud"]

    for i in range(1,6):
        avistamiento = lt.getElement(lista,i)
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"],mp.get(avistamiento,"Longitud")["value"],mp.get(avistamiento,"Latitud")["value"]])

    for i in range(lt.size(lista)-4,lt.size(lista)+1):
        avistamiento = lt.getElement(lista,i)
        tabla.add_row([mp.get(avistamiento,"Dia")["value"],mp.get(avistamiento,"Ciudad")["value"],mp.get(avistamiento,"Pais")["value"],mp.get(avistamiento,"Duracion")["value"],mp.get(avistamiento,"Forma")["value"],mp.get(avistamiento,"Longitud")["value"],mp.get(avistamiento,"Latitud")["value"]])
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
catalog2 = None

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
        catalog2 = controller.init2()
        datos = loadData(catalog)
        controller.loadData2(catalog2)
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

    elif int(inputs[0]) == 2:
        duracion1 = input("ingrese duracion minima: ")
        duracion2 = input("ingrese duracion maxima: ")
        start_time = time.process_time()
        datos = controller.avistamientos_duracion(catalog2,duracion1,duracion2)
        stop_time = time.process_time()
        timed = (stop_time - start_time)*1000
        print('se encuentra un total de ' + str(datos[0]) + ' segun los datos dados...')
        print('el avistamiento de ovnix mas largos es: ')
        print("-" * 50)
        print('|' + 'duracion'.center(40) + ' | ' + 'count'.center(10) + '|')
        print("=" * 50)
        for x in lt.iterator(datos[1]):
            print('|' + str(int(x["llave"])).center(40) + ' | ' + str(int(x["valor"])).center(10) + '|')
            print("-" * 50)
        print('hay ' + str(datos[2]) + ' avistamientos entre: ' + duracion1 + ' y ' + duracion2 )
        print('los primero 3 y ultimos 3 avistamientos son:')
        print("+"+("-"*143)+"+")
        print("|"+ "datetime".center(19)+" | "+ "city".center(30)+" | "+ "state".center(15)+" | "+"country".center(15)+"|"+"shape".center(20)+" | "+ str("duration (seconds)").center(30)+" | ")
        print("+"+("-"*143)+"+")
        for x in lt.iterator(datos[3]):
            print("|"+ str(x["datetime"]).center(19)+" | "+ x["city"].center(30)+" | "+ x["state"].center(15)+" | "+x["country"].center(15)+"|"+x["shape"].center(20)+" | "+ str(x["duration (seconds)"]).center(30)+" | ")
            print("+"+("-"*143)+"+")
        print("El tiempo para cargar los archivos fue de:", str(timed) , "s") 
   
    
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

    elif int(inputs[0]) == 4:
        inferior= input('Ingrese el limite inferior en formato AA-MM-DD: ')
        superior = input('Ingrese el limite superior en formato AA-MM-DD: ') 
        start_time = time.process_time()
        datos = controller.contar_rango_fecha(catalog2, inferior, superior)
        stop_time = time.process_time()
        timed = (stop_time - start_time)*1000
        ffinal=mo.size(catalog2["Fecha"])
        
       
        print("hay en total: : "+ str(ffinal)+" dias con avistamiento de ovnis: ")
        print('hay ' + str(datos[2]) + ' avistamientos entre: ' + inferior + ' y ' + superior )
        print('los primero 3 y ultimos 3 avistamientos son:')
        print("+"+("-"*140)+"+")
        print("|"+ "datetime".center(25)+" | "+ "city".center(35)+" | "+ "country".center(15)+" | "+"shape".center(30)+" | "+ str("duration (seconds)").center(40)+" | ")
        print("+"+("-"*140)+"+")
        for x in lt.iterator(datos[0]):                             
            print("|"+str(x["datetime"])+" | "+ x["city"].center(40)+" | "+ x["country"].center(25)+" | "+x["shape"].center(30)+" | "+ str(x["duration (seconds)"]).center(40)+" | ")
            print("+"+("-"*127)+"+")
        
        for x in lt.iterator(datos[1]):                             
            print("|"+ str(x["datetime"])+" | "+ x["city"].center(40)+" | "+ x["country"].center(25)+" | "+x["shape"].center(30)+" | "+ str(x["duration (seconds)"]).center(40)+" | ")
            print("+"+("-"*127)+"+") 
        print("El tiempo para cargar los archivos fue de:", str(timed) , "s") 
    
    elif int(inputs[0]) == 5:
        lon_min = round(float(input("Ingrese la longitud mínima: ")),2)
        lon_max = round(float(input("Ingrese la longitud máxima: ")),2)
        lat_min = round(float(input("Ingrese la latitud mínima: ")),2)
        lat_max = round(float(input("Ingrese la latitud máxima: ")),2)

        start_time = time.process_time()
        resultado = controller.avistamientos_area(catalog,lon_min,lon_max,lat_min,lat_max)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_avistamientos_area(resultado)
        print("Tiempo requerido "+str(elapsed_time_mseg)+" mseg")


    else:
        sys.exit(0)
sys.exit(0)
