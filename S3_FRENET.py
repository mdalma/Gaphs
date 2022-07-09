#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:06:59 2020

@author: Miquel Monge Dalmau - 1565230
@author: Oriol Prat Font - 1565096
"""


# Calcular Triedre de Frenet, Torsió i Curvatura a partir de les tres derivades de la corba

#Importem llibreries

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def Norm(x):
    norm=np.sqrt(np.sum(x**2))
    return norm

def param_t(_from,_to,_size):
    _step=(_to-_from)/_size
    t=np.arange(_from,_to+_step,_step)
    return t


# vt: Vector Tangent 
def vt(t):
    return dx1(t)/Norm(dx1(t))

# vb:Vector Binormal
def vb(t):
    return np.cross(dx1(t),dx2(t))/Norm(np.cross(dx1(t),dx2(t)))

# vn: Vector  Normal
def vn(t):
    return np.cross(vb(t),vt(t))

def k(t):
    return Norm(np.cross(dx1(t),dx2(t)))/Norm(dx1(t))**3

def T(t):
    return -np.dot(np.cross(dx1(t),dx2(t)),dx3(t))/Norm(np.cross(dx1(t),dx2(t)))**2

def dibuixar(mat):
    xx, yy, zz=mat
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.plot(xx, yy, zz, label='parametric curve')
    plt.show()

# PRIMERA CORBA:

#HELIX CILÍNDRICA
a=2
b=1
def x(t):
    return np.array([a*np.cos(t),a*np.sin(t),b*t],dtype=np.float64)

# Dibuixem-la
t=param_t(0,8*np.pi,100)
dibuixar(x(t))

def dx1(t):
    return np.array([-a*np.sin(t),a*np.cos(t),b])

def dx2(t):
    return np.array([-a*np.cos(t),-a*np.sin(t),0])

def dx3(t):
    return np.array([a*np.sin(t),-a*np.cos(t),0])

#Calculem el triedre de Frenet al valor del paràmetre t 

#Punt del patàmetre t on trobar el triedre
p_t=np.pi

# Vector tangent al punt t
vt(p_t)

# Vector binormal al punt t
vb(p_t)

# Vector normal al punt t
vn(p_t)

# Dibuxem la corba i afegim el vector tangent
xx, yy, zz=x(t)
pos=np.pi/2
xxx,yyy,zzz=x(pos)
vt1,vt2,vt3=vt(pos)
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot(xx, yy, zz, label='parametric curve')
ax.quiver(xxx,yyy,zzz,vt1,vt2,vt3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='g')
plt.show()


# Dibuxem la corba i afegim el triedre
pos=np.pi/2
xx, yy, zz=x(t)
xxx,yyy,zzz=x(pos)
vt1,vt2,vt3=vt(pos)
vn1,vn2,vn3=vn(pos)
vb1,vb2,vb3=vb(pos)
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot(xx, yy, zz, label='parametric curve')
ax.quiver(xxx,yyy,zzz,vt1,vt2,vt3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='g')
ax.quiver(xxx,yyy,zzz,vn1,vn2,vn3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='g')
ax.quiver(xxx,yyy,zzz,vb1,vb2,vb3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='g')
plt.show()


# Fem una funció que ho faci tot
def dibuixarT(mat,triedre,pos):
    xx, yy, zz=x(t)
    xxx,yyy,zzz=x(pos)
    vt1,vt2,vt3=vt(pos)
    vn1,vn2,vn3=vn(pos)
    vb1,vb2,vb3=vb(pos)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.plot(xx, yy, zz, label='parametric curve')
    if (triedre):
        ax.quiver(xxx,yyy,zzz,vt1,vt2,vt3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='g')
        ax.quiver(xxx,yyy,zzz,vn1,vn2,vn3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='r')
        ax.quiver(xxx,yyy,zzz,vb1,vb2,vb3,
            pivot='tail',length=2,arrow_length_ratio=0.5,color='y')
    plt.show()

# provem la funció
dibuixarT(x(t),True,np.pi)

# EXERCICI
# Fer una funció que li passem diversos t's a una llista i dibuixi la corba i el triedre a
# cada punt de la llista
def dibuixarTPos(mat,listpos):
    xx, yy, zz=x(t)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.plot(xx, yy, zz, label='parametric curve')
    for i in listpos:
        xxx,yyy,zzz=x(i)
        vt1,vt2,vt3=vt(i)
        vn1,vn2,vn3=vn(i)
        vb1,vb2,vb3=vb(i)
        ax.quiver(xxx,yyy,zzz,vt1,vt2,vt3,
            pivot='tail',length=1,arrow_length_ratio=0.5,color='g')
        ax.quiver(xxx,yyy,zzz,vn1,vn2,vn3,
            pivot='tail',length=1,arrow_length_ratio=0.5,color='r')
        ax.quiver(xxx,yyy,zzz,vb1,vb2,vb3,
            pivot='tail',length=1,arrow_length_ratio=0.5,color='y')
    plt.show()

#Si la funci està ben feta aquesta linia hauria de funcionar
dibuixarTPos(x(t),[0,np.pi/2,np.pi,3*np.pi/2])


# SEGONA CORBA #HELIX CÒNICA
a=1
b=1
def x(t):
    return np.array([a*np.exp(t)*np.cos(t),a*np.exp(t)*np.sin(t),b*np.exp(t)],dtype=np.float64)

# Dibuixem-la
t=param_t(-2*np.pi,2*np.pi,100)
dibuixar(x(t))

# EXERCICI 2
# DIBUIXAR LA CORBA AMB EL TRIEDRE A DIFERENTS PUNTS DEL PARÀMETRE

# PELS DOS EXERCICIS ENTREGAR UN NOTEBOOK O UN .PY


