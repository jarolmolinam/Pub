
import numpy as np
import matplotlib.pyplot as plt
import xlrd # para leer archivos de excell
from scipy.optimize import curve_fit ## Ajuste de datos al modelo
from rutinas import *

"""
Este es un ejemplo propio de un archivo de incio donde se cargan los datos de un archivo de excell
se limpian para pasarlo para pasarlo a la funcion ajuste que se encarga de realizar el ajuste completo
de los datos y entregar los parametros y las correlaciones de ajuste por cada variable. 

"""

###############################################################################
def read(Dat):
    var = []
    hojas = Dat.nsheets
    for i in range(hojas): 
        hoja = Dat.sheet_by_index(i)
        filas = hoja.nrows
        col = hoja.ncols
        var.append([])
        for ii in range(col):
            var[i].append([])
            for iii in range(filas):
                t = hoja.cell_type(iii,ii)
                if t == 2:
                    A = hoja.cell_value(iii,ii)
  
                    var[i][ii].append(A)
    vart = []
    varq = []
    for i in range(len(var)):
         vart.append([])
         varq.append([])
         for ii in range(0, len(var[i]), 2):
             n = len(var[i][ii])
             if n > len(var[i][ii+1]):
                 n = len(var[i][ii+1])
             vart[i].append([])
             varq[i].append([])
             for iii in range(n):
                 t = var[i][ii][iii]
                 q = var[i][ii+1][iii]
                 vart[i][ii-int(ii/2)].append(t)
                 varq[i][ii-int(ii/2)].append(q)
                 
    return(vart, varq)
###############################################################################

# Lectura de datos del archivo de excell
datos = xlrd.open_workbook("microcalorimetría-articulo.xls")
(time, heat) = read(datos)

# j  # Temp 0=25, 1=35, 2=45
# i  # Exp 0=1, 1=2, 2=3

Parm = []
Err = []

for j in range(3):
    for i in range(3):
        if j == 0: A = "25"
        if j == 1: A = "35"
        if j == 2: A = "45"
        if i == 0: B = "_Exp_1"
        if i == 1: B = "_Exp_2"
        if i == 2: B = "_Exp_3"
        nom = A+B

# Lectura de datos experimentales
        print("#############################################")
        print(" Ajustando curvas del caso   Temperatura "+nom)
        Q = heat[j][i+3]
        T = time[j][i+3]
        q = heat[j][i]
        t = time[j][i]
        (param, err ) = Ajuste(Q, T, q, t)
        print(param)
        print(err)




