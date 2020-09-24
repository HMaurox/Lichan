
import hashlib
import sys 
import bcrypt
from funciones_Li import Key_MD5
from datetime import date
from datetime import datetime
import smtplib

#conect  db 
import pymysql

tiempo = datetime.now()
format = tiempo.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
# Conectar con base de datos
conexion = pymysql.connect(host="localhost", 
                           user="root", 
                           passwd="12345", 
                           database="tester")
cursor = conexion.cursor()

   #consulta  de correo en base de datos 

email = input("correo de acceso :" )
concatec_email= email + format
dinamic_pass= Key_MD5(concatec_email)


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



