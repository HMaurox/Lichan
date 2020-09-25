
#library
import  hashlib  #libreria de hash
import yagmail   #modulo envio de correos
import smtplib   #modulo SMTP para envio de correos
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema
from PIL import Image, ImageDraw, ImageFont # Modulo para el procesamiento de plantillas y generacion de imagenes
import os #  modulo para gestion del sistema.
import pymysql #modulo de  conecion con DB

#def

#Obtiene la codificacion en MD5
def Key_MD5(clave):
    Key_co = clave.encode('utf-8')
    Key_L = hashlib.md5(Key_co)    
    Key_F = Key_L.hexdigest()
    Key_F= Key_F.upper()
    return Key_F
#genera el formato de la licencia
def Format_L(formatos):
    lisen = formatos[0:4]+"-"+formatos[4:8]+"-"+formatos[8:12]+"-"+formatos[12:16]+"-"+formatos[16:20]+"-"+formatos[20:24]+"-"+formatos[24:28]+"-"+formatos[28:32]
    return lisen
#de SHA256  a clave de licencia
def  licenciar(codigo_licencia):    
    Key_str= str(codigo_licencia)
    Temp_lice = Key_MD5(Key_str)
    licencia=Format_L(Temp_lice)
    return licencia
# parametros#

# Funcion de  envio de correos clave dinamicas#
def claves_dinamicas(destinatario):
    #generacion de codigo
    Cd_timepo = datetime.now()
    format = Cd_timepo.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
    concatec_email= destinatario + format
    dinamic_pass= Key_MD5(concatec_email)
    CD_formato= dinamic_pass[0:4]+" "+dinamic_pass[28:32] #  codigo generado   
    
    #generacion de imagen
    image = Image.open("clave_dina.jpg") # Plantilla
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 44)
    draw.text((660,380), CD_formato, font=font, fill="Black")
    Name_CD= dinamic_pass+".jpg"
    image.save(Name_CD)

    #Envio de codigo a correo 
    correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura") # Datos de acceso al correo del proyecto
    correo.send(
    to= destinatario,
    subject= "CLAVE DINAMICA - Acceso a LICHAIN",
    contents=[ "Bienvenido a LiChain,  su codigo de acceso temporal es : ",Name_CD]
    )
    print("su correo fue enviado correctamente")
    
    #Actualizacion de acceso en DB
    
    # Conectar con base de datos
    conexion = pymysql.connect(host="localhost", 
                           user="root", 
                           passwd="12345", 
                           database="tester")
    cursor = conexion.cursor()
    SQL = "UPDATE usuario set Clave_dina= %s  Where Correo = %s"
    clave=(CD_formato, destinatario) #actualizacion de clave
    cursor.execute(SQL,clave)
    conexion.commit()
    conexion.close()
    #
    os.remove(Name_CD)
    print("%s has been removed successfully" %Name_CD) 
    
    
    
    
    





#     

