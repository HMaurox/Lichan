#library
import  hashlib  #libreria de hash
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema

from PIL import Image, ImageDraw, ImageFont # Modulo para el procesamiento de plantillas y generacion de imagenes
import os #  modulo para gestion del sistema.
import pymysql #modulo de  conecion con DB
import re
import json 
from funciones_Li import cad_num
from funciones_Li import consulta_one_DB_STR
from funciones_Li import consulta_varc_Str
from funciones_Li import consulta_status_usuario
from funciones_Li import claves_dinamicas
#se importan los bloques que contienen  la estructura del bloque a minar


def bloque_sesion(proof,hash_previo,entidad,index):

    #estructura de datos del bloque
    BC_sesion = {
        'index' : int(index)+1, #se aumenta el indice de la cadena
        'timestamp': str(datetime.datetime.now()), # toma el  fecha (dia/mes) y hora del sistema (HH:MM:SS)
        'fK_entidad':   entidad, # id nombre del usuario que inicio sesion 
        'tipo_bloque':'1',
        'proof':proof , # resultado de la PoW
        'hash_previo': hash_previo # hash previo al bloque
        }
    return BC_sesion  # se retorna  el bloque parametrizado.

    # Definicion del Pow         
def proof_of_work(proof_previo):
    nuevo_proof = 1   #creamos prueba de trabajo
    valida_proof = False # asumimos que  la interacion es falasa para  frozar la validacion
    while valida_proof is False:
        hash_operation = hashlib.sha256(str(nuevo_proof**2 - proof_previo**2).encode()).hexdigest() #minado de respuesta
        if hash_operation[:6] == '000001': #  citerio de busqueda
            valida_proof = True
        else:
            nuevo_proof += 1
    return nuevo_proof
    #hasH de sesion         
def hash(BC_sesion):
    codificacion_bloque = json.dumps(BC_sesion, sort_keys = True).encode()
    print(codificacion_bloque)
    return hashlib.sha256(codificacion_bloque).hexdigest()

    #hasH de sesion  
def minar_sesion(FK_empresa):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0]) #consulta del numero de registros
    Con_bloque= str(len_cadena-1)
    Index=cad_num(consulta_one_DB_STR('Index','cadena','Index',Con_bloque))
    Index_nuevo=Index+1
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    proof_previo= cad_num(consulta_one_DB_STR('proof','cadena','Index',Con_bloque))
    proof =proof_of_work(proof_previo)
    hash_previo =consulta_varc_Str('Hash_previo','cadena','Index',Con_bloque) 
    hash_bloque=hash(hash_previo)
    print(hash_bloque)
    #BC_sesion= bloque_sesion(proof,hash_previo,FK_empresa,Index)
    Sql_up="INSERT INTO cadena (`Index`,`proof`,`time`,`Tipo_bloque`,`Hash_previo`,`ID_FK_entidad`) VALUES (%s,%s,%s,%s,%s,%s)"
    complemento=(Index_nuevo,proof,marca_tiempo,1,hash_bloque,FK_empresa)
    cursor.execute(Sql_up,complemento)
    conexion.commit()
    conexion.close()
#se minara el bloque si el usuarios es valido y se autorizara el ingreso
def autorizacion_usuario(correo):
    valor= consulta_status_usuario(correo)
    if valor==1:
        conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
        cursor = conexion.cursor()
        SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO=%s"
        cursor.execute(SQL,correo)
        Con_empresa=cad_num(cursor.fetchone())
        print (Con_empresa)
        minar_sesion(Con_empresa)
        claves_dinamicas(correo)
        autorizacion=1
    else:
        autorizacion=0
    return autorizacion    




            











#def elemens():











