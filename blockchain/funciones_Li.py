
#library
import  hashlib  #libreria de hash
import yagmail   #modulo envio de correos
import smtplib   #modulo SMTP para envio de correos
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema
from PIL import Image, ImageDraw, ImageFont # Modulo para el procesamiento de plantillas y generacion de imagenes
from ElemenChain import minar_sesion
import os #  modulo para gestion del sistema.
from re import split
import re
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
    image = Image.open(r'D:\Usb\TESIS\Ts\Lichan\blockchain\clave_dina.jpg') # Plantilla
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
                           database="blockchain")
    cursor = conexion.cursor()
    SQL = "UPDATE usuario SET US_CLAVE_DINA= %s  WHERE CORREO = %s"
    clave=(CD_formato, destinatario) #actualizacion de clave
    cursor.execute(SQL,clave)
    conexion.commit()
    conexion.close()
    #
    os.remove(Name_CD)
    print("%s has been removed successfully" %Name_CD) 
# Funcion de  envio de correos clave dinamicas#
def Clave_out(destinatario):
    #generacion de codigo
    Cd_timepo = datetime.now()
    format = Cd_timepo.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
    concatec_email= destinatario + format
    dinamic_pass= Key_MD5(concatec_email)
    CD_formato= dinamic_pass[0:4]+" "+dinamic_pass[28:32] #  codigo generado   
    
    #Actualizacion de acceso en DB

    # Conectar con base de datos
    conexion = pymysql.connect(host="localhost", 
                           user="root", 
                           passwd="12345", 
                           database="blockchain")
    cursor = conexion.cursor()
    SQL = "UPDATE usuario SET US_CLAVE_DINA= %s  WHERE CORREO = %s"
    clave=(CD_formato, destinatario) #actualizacion de clave
    cursor.execute(SQL,clave)
    conexion.commit()
    conexion.close()
    #
def cad_num (cadena):
    caden=str(cadena)
    cade = caden.strip(" ")
    numero= split('\D+',cade)
    if  numero[1]=='':
         valor = 0
    else:
         valor = int(numero[1])
    return valor
def consulta_one_DB_STR(colum,tabla,condicion,valor):
    Concate_sql = "SELECT `{}` FROM `{}` WHERE `{}` = {}".format(colum,tabla,condicion,valor)
    
    conexion = pymysql.connect(host="localhost", 
                            user="root", 
                            passwd="12345", 
                            database="blockchain")
    cursor = conexion.cursor()
    SQL=Concate_sql
    cursor.execute(SQL)
    return cursor.fetchone() 

    conexion.commit()
    conexion.close()
def consulta_varc_Str(colum,tabla,condicion,valor):

    Concate_sql = "SELECT `{}` FROM `{}` WHERE `{}` = {}".format(colum,tabla,condicion,valor)
    conexion = pymysql.connect(host="localhost", 
                                    user="root", 
                                    passwd="12345", 
                                    database="blockchain")
    cursor = conexion.cursor()
    SQL=Concate_sql
    cursor.execute(SQL)
    result=cursor.fetchone()
    retorno= re.sub(r'[^\w]','', str(result))
    return retorno 
    conexion.commit()
    conexion.close()
def consulta_correo(correo):
    conexion = pymysql.connect(host="localhost", 
                           user="root", 
                           passwd="12345", 
                           database="blockchain")
                           
    cursor = conexion.cursor()
    SQL = "SELECT US_STATUS From usuario WHERE CORREO = %s"
    clave=correo
    cursor.execute(SQL,clave)
    return cad_num (cursor.fetchone())

    conexion.commit()
    conexion.close()    
def consulta_status_usuario(correo):
    autorizacion=0
    # primer nivel validar al usuario
   
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    
    
    estado_us= consulta_correo(correo) #estado del usuario
    #print('us : '+ str(estado_us))
    if estado_us==1:
        #segundo nivel validar la empresa ligada al usuario
        sql_empresa= "SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO = %s"
        cursor.execute(sql_empresa,correo)
        FK_empresa=cad_num(cursor.fetchone())
        #print('empresa fk: '+ str(FK_empresa))
        sql_empresa_Stado= "SELECT  E_STATUS FROM entidad WHERE ID_ENTIDAD =%s"
        cursor.execute(sql_empresa_Stado,FK_empresa)
        estado_empresa=cad_num(cursor.fetchone())
        #print('empresa: '+ str(estado_empresa))
        if estado_empresa==1:
            autorizacion=1
        else:
            autorizacion=0    
    else:
        autorizacion=0
    conexion.close()    
    return autorizacion
def generar_id_hash(CC,marca_tiempo,nombre,adm_cc,Con_bloque):
    cadena= str(CC)+str(marca_tiempo)+str(nombre)+str(adm_cc)+'Generacion de ID para sistem Lichain'
    minar_sesion(1)
    hash_previo =consulta_varc_Str('Hash_previo','cadena','Index',Con_bloque)
    Cad_id_ud = cadena+hash_previo
    hash_id=hashlib.sha256(Cad_id_ud).hexdigest()
    return hash_id

