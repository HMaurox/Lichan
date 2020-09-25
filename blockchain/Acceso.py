
import hashlib
import sys 
import bcrypt
from funciones_Li import claves_dinamicas
import smtplib

#conect  db 
import pymysql

# Conectar con base de datos
conexion = pymysql.connect(host="localhost", 
                           user="root", 
                           passwd="12345", 
                           database="tester")
cursor = conexion.cursor()

   #consulta  de correo en base de datos 

email = input("correo de acceso :" )
codiguito = claves_dinamicas(email)
# Recuperar registros de la tabla 'Usuarios'
registros = "SELECT * FROM usuario;"

# Mostrar registros 
cursor.execute(registros)
filas = cursor.fetchall()
for fila in filas:
   print(fila)

# Finalizar 
conexion.commit()
conexion.close()



