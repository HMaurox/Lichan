# Definicion estructura de los posibles bloques que pueden pertener  a la cadena de datos
# se definde 
# bloques de sesion : que registrara la actividad de lso usuarios
# bloque  de usurio : contiene la informacion de un usuario y su nivel de acceso
#  

import hashlib 
import sys
import os 
import bcrypt
import math
import datetime
import json 
from flask import Flask, jsonify

def bloque_sesion(self,proof,hash_previo,usuario):

        #estructura de datos del bloque
        BC_sesion = {
            'index' : len(self.chain) +1, #se aumenta el indice de la cadena
            'timestamp': str(datetime.datetime.now()), # toma el  fecha (dia/mes) y hora del sistema (HH:MM:SS)
            'Usuario':  usuario, # id nombre del usuario que inicio sesion 
            'tipo_bloque':'1',
            'proof':proof , # resultado de la PoW
            'hash_previo': hash_previo # hash previo al bloque
            }
        self.chain.append(BC_sesion)
        return BC_sesion  # se retorna  el bloque parametrizado.

def bloque_usuario(self,proof,hash_previo,nombre,apellido,rol,identidicacion,correo,us_hash,id_entidad,ciudad,provincia,pais,u_status):
    
        #estructura de datos del bloque
        BC_usuario = {
            'index' : len(self.chain) +1, 
            'timestamp': str(datetime.datetime.now()),
            'tipo_bloque':'2', 
            'Nombre':  nombre, 
            'Apellido':  apellido,
            'ROL': rol, 
            'Id_idendificacion' :  identidicacion,
            'Correo': correo,
            'Us_Hash': us_hash,
            'Id_entidad': id_entidad,
            'Ciudad': ciudad,
            'Provincia': provincia,
            'Pais': pais,
            'Status':u_status, 
            'proof':proof ,
            'hash_previo': hash_previo
            }
        self.chain.append(BC_usuario)
        return BC_usuario  # se retorna  el bloque parametrizado.

def bloque_entidad(self,proof,hash_previo,n_entidad,nic,n_correo,direccion,e_ciudad,e_provincia,e_pais,n_licencias,l_activas,e_status):

        #estructura de datos del bloque
        BC_entidad = {
            'index' : len(self.chain) +1, 
            'timestamp': str(datetime.datetime.now()),
            'tipo_bloque':'3', 
            'Nombre_entidad': n_entidad, 
            'Nic':  nic, 
            'Correo_entidad': n_correo,
            'Direccion': direccion,
            'E_Ciudad': e_ciudad,
            'E_Provincia': e_provincia,
            'E_Pais': e_pais,
            'N_licencias': n_licencias,
            'L_activas': l_activas, 
            'Status':e_status,
            'proof':proof ,
            'hash_previo': hash_previo
            }
        self.chain.append(BC_entidad)
        return BC_entidad 

def bloque_Licencia(self,proof,hash_previo,id_licencia,codigo,id_cliente,id_entidad,fecha_activate,l_status):
    
        #estructura de datos del bloque
        BC_licencia = {
            'index' : len(self.chain) +1, 
            'timestamp': str(datetime.datetime.now()),
            'tipo_bloque':'4', 
            'Id_licencia':  id_licencia, 
            'Codigo': codigo, 
            'Id_cliente': id_cliente,
            'Id_entidad': id_entidad,
            'fecha_activate': fecha_activate,
            'status':l_status,
            'proof': proof ,
            'hash_previo': hash_previo
            }
        self.chain.append(BC_licencia)