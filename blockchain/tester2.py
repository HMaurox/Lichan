import pymysql
from funciones_Li import*
import json

def json_sesion():
    
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=int(cursor.fetchone()[0])
    SQL="SELECT * FROM cadena"
    cursor.execute(SQL)
    h= cursor.fetchall()
    x=1
    cadena=[]

    for x in range (len_cadena):
        BC_sesion = {
            'index' : h[x][0],                                   
            'timestamp':h[x][3],
            'fK_entidad':h[x][6],                                  
            'tipo_bloque':'1',
            'proof':h[x][2] ,                                           
            'hash_previo':h[x][5]                                 
        }
        cadena.append(BC_sesion)

    with open('cadena_sesion.json', 'w') as jsonFile:
        json.dump(cadena, jsonFile)
        jsonFile.close()    
def json_sesion_us():
    
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM usuario"
    cursor.execute(SQL)
    len_cadena=int(cursor.fetchone()[0])
    SQL="SELECT * FROM usuario"
    cursor.execute(SQL)
    h= cursor.fetchall()
    x=1
    cadena=[]

    for x in range (len_cadena):
        BC_usuario = {
            'index' : h[x][0], 
            'tipo bloque':'2', 
            'Nombre':  h[x][1], 
            'Apellido': h[x][2],
            'ROL': h[x][7], 
            'Id idendificacion':h[x][3],
            'Correo':h[x][4],
            'ID Hash':h[x][5],
            'Id entidad': h[x][6],
            'Ciudad':h[x][10],
            'Provincia':h[x][9],
            'Pais':h[x][8],
            'Status':h[x][11] 
        }
        cadena.append(BC_usuario)

    with open('cadena_us.json', 'w') as jsonFile:
        json.dump(cadena, jsonFile)
        jsonFile.close()    
def json_sesion_en():
    
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM entidad"
    cursor.execute(SQL)
    len_cadena=int(cursor.fetchone()[0])
    SQL="SELECT * FROM entidad"
    cursor.execute(SQL)
    h= cursor.fetchall()
    x=1
    cadena=[]

    for x in range (len_cadena):
        BC_entidad = {  
            'index' : h[x][0], 
            'tipo bloque':'3', 
            'Nombre entidad':h[x][1], 
            'Nic':h[x][2], 
            'Correo entidad':h[x][3], 
            'Direccion':h[x][7], 
            'E Ciudad':h[x][6], 
            'E Provincia':h[x][5], 
            'E Pais':h[x][4], 
            'N licencias':h[x][9], 
            'L activas': h[x][8],
            'Status':h[x][10],
            'ID HASH':h[x][11]  
            }
        cadena.append(BC_entidad)

    with open('cadena_en.json', 'w') as jsonFile:
        json.dump(cadena, jsonFile)
        jsonFile.close()   
def json_sesion_li():
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM licencia"
    cursor.execute(SQL)
    len_cadena=int(cursor.fetchone()[0])
    SQL="SELECT * FROM licencia"
    cursor.execute(SQL)
    h= cursor.fetchall()
    x=1
    cadena=[]

    for x in range (len_cadena):
        BC_licencia = {
            'index' : h[x][0], 
            'tipo_bloque':'4', 
            'Id_cliente': h[x][3],
            'Id_entidad': h[x][4],
            'fecha_activate': h[x][5],
            'status':h[x][6],
            'HASH ID':h[x][1],
            'Codigo L':h[x][2]
         }
        cadena.append(BC_licencia)

    with open('cadena_li.json', 'w') as jsonFile:
        json.dump(cadena, jsonFile)
        jsonFile.close()  
json_sesion_li()