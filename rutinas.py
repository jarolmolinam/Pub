#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:17:47 2021

@author: Jarol Molina Mosquera
         Sebastian Rudas
        Ary Alain Hoyos

Ajustes para el modelo de flujo de calor JAR

Valores de entrada:
Q Calor acomulado 
T Valores de tiempo correspondientes con el calor acomulado
q Flujo de calor
t Valores de tiempo correspondiente al flujo de calor

Salida

p4 Vector con los 6 paramestros del modelo distribuidos de la siguiente forma
    p4[0]   Q1
    p4[1]   tao1
    p4[2]   bata1
    p4[3]   Q2
    p4[4]   tao2
    p4[5]   beta2
err2 Vector de error de correlacion para cada parametro en igual orden al vector p4


"""

import numpy as np
import matplotlib.pyplot as plt
import xlrd # para leer archivos de excell
from scipy.optimize import curve_fit ## Ajuste de datos al modelo

def Ajuste(Q, T, q, t):
    (i_max1, i_max2, i_min) = criticos(t, q)
    p01 = [Q[i_min], t[i_max1], 0.9  ]
    b = [(0, p01[1], 0), (150, p01[1]*20, 3)]
    (p1, err1) = fit_p(p01, t[:i_min], Q[:i_min], b )
 
    p02 = [Q[len(Q)-1], t[i_max2], 0.9  ]
    b = [(0, p02[1], 0), (150, p02[1]*20, 3)]
    (p2, err2) = fit_p(p02, t[i_min:], Q[i_min:], b )
   
    p03 = [p1[0], p1[1], p1[2], p2[0], p2[1], p2[2]]
    b = [(p1[0], p1[1], 0, p2[0]*0.5, p1[1], 0), (p1[0]+100, p2[1]*20, 2, p2[0]*5, p2[1]*5, 2)]
    (p3, err2) = fit_t(p03, t, Q, b)
 
    p04 = [p3[0], p3[1], p3[2], p3[3], p3[4], p3[5]]
    b = [(p1[0], p1[1], 0, p2[0]*0.5, p1[1], 0), (p1[0]+100, p2[1]*20, 2, p2[0]*5, p2[1]*5, 2)]
    (p4, err2) = fit_ti(p04, t, q, b)
    return(p4, err2)

###############################################################################
def criticos(x, y):
    i_min = 0
    n = len(x)

    i_max1 = y.index(max(y))
    An = np.arange(i_max1+1, n, 1)
   
    for i in An:
        dev = y[i + 1] - y[i]
       
        if dev > 0:
            i_min = i
           
            break
    i = i_min
    i_max2 = y.index(max(y[i_min:n]))
    i_min = y.index(min(y[i_min:i_max2]))
    return(i_max1, i_max2, i_min)
###############################################################################

def fit_p(p, x, y, b):
    c, cov = curve_fit(JAR, x, y, p, maxfev=10000000, bounds=b)
    cov = np.sqrt(np.diag(cov))
    cov = cov/c
    return(c, cov)
###############################################################################
def fit_ti(p, x, y, b):
    c, cov = curve_fit(DARJ, x, y, p, maxfev=1000000, bounds=b)
    cov = np.sqrt(np.diag(cov))
    cov = cov/c
    return(c, cov)
###############################################################################
def fit_t(p, x, y, b):
    c, cov = curve_fit(ARJ, x, y, p, maxfev=1000000, bounds=b)
    cov = np.sqrt(np.diag(cov))
    cov = cov/c
    return(c, cov)
############################################################################### 

def JAR(x, Q, tao, beta):
    Q = np.array(Q, dtype=np.longdouble)
    tao = np.array(tao, dtype=np.longdouble)
    beta = np.array(beta, dtype=np.longdouble)
    E = pow(x,beta)
    y = Q*np.exp(-tao/E)
    return y 
###############################################################################
def ARJ(x, Q1, tao1, beta1, Q2, tao2, beta2 ):
    Q1 = np.array(Q1, dtype=np.longdouble)
    tao1 = np.array(tao1, dtype=np.longdouble)
    beta1 = np.array(beta1, dtype=np.longdouble)
    Q2 = np.array(Q2, dtype=np.longdouble)
    tao2 = np.array(tao2, dtype=np.longdouble)
    beta2 = np.array(beta2, dtype=np.longdouble)
    a = pow(x, beta1)
    b = pow(x, beta2)
    y = Q1*np.exp(-tao1/a) + Q2*np.exp(-tao2/b)
    return y
###############################################################################
def DARJ(x, Q1, tao1, beta1, Q2, tao2, beta2 ):
    x = np.array(x,dtype=np.longdouble)
    Q1 = np.array(Q1, dtype=np.longdouble)
    tao1 = np.array(tao1, dtype=np.longdouble)
    beta1 = np.array(beta1, dtype=np.longdouble)
    Q2 = np.array(Q2, dtype=np.longdouble)
    tao2 = np.array(tao2, dtype=np.longdouble)
    beta2 = np.array(beta2, dtype=np.longdouble)
    a = pow(x,-beta1)
    b = pow(x,-beta2)
    A = pow(x,beta1)
    B = pow(x,beta2)
    y = (Q1*tao1*beta1*np.exp(-tao1/A)*a +
         Q2*tao2*beta2*np.exp(-tao2/B)*b)/x 
    return y 
############################################################################
