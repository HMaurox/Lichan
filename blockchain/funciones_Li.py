
#library
import  hashlib  #libreria de hash
import yagmail   #modulo envio de correos
import smtplib   #modulo SMTP para envio de correos
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema
from PIL import Image, ImageDraw, ImageFont # Modulo para el procesamiento de plantillas y generacion de imagenes
import os #  modulo para gestion del sistema.
from re import split
import re
import pymysql #modulo de  conecion con DB
import json 
import qrcode
import os


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
    hash_id=hashlib.sha256(Cad_id_ud.encode('utf-8')).hexdigest()
    return hash_id

##elemt
def bloque_sesion(proof,hash_previo,entidad,index):
    Cd_timepo = datetime.now()
    #estructura de datos del bloque
    BC_sesion = {
        'index' : int(index)+1,                                   #se aumenta el indice de la cadena
        'timestamp': Cd_timepo.strftime('%Y-%m-%d %H:%M:%S'),     # toma el  fecha (dia/mes) y hora del sistema (HH:MM:SS)
        'fK_entidad':   entidad,                                  # id nombre del usuario que inicio sesion 
        'tipo_bloque':'1',
        'proof':proof ,                                           # resultado de la PoW
        'hash_previo': hash_previo                                # hash previo al bloque
        }
    return BC_sesion                                              # se retorna  el bloque parametrizado.
   
    # Definicion del Pow         
def proof_of_work(proof_previo):
    nuevo_proof = 1   #creamos prueba de trabajo
    valida_proof = False # asumimos que  la interacion es falasa para  frozar la validacion
    while valida_proof is False:
        hash_operation = hashlib.sha256(str(nuevo_proof**2 - proof_previo**2).encode()).hexdigest() #minado de respuesta
        #print(hash_operation)
        if hash_operation[:6] == '000001': #  citerio de busqueda
            valida_proof = True
            
        else:
            nuevo_proof += 1
    return nuevo_proof

def cadena_valida():
    index_bloque= 2         #indexamos el bloque
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0]) #consulta del numero de registros
    conexion.commit()
    
    while   index_bloque< len_cadena:

        SQL="SELECT `proof` FROM `cadena` WHERE `Id_Cadena` = %s"
        cursor.execute(SQL,index_bloque)
        proof_previo= int(cursor.fetchone()[0])
        #print(str(proof_previo))
        
        SQL="SELECT `proof` FROM `cadena` WHERE `Id_Cadena` = %s"
        cursor.execute(SQL,(index_bloque+1))
        proof_nuevo= int(cursor.fetchone()[0])
        #print(str(proof_nuevo))

        hash_operation = hashlib.sha256(str(proof_nuevo**2 - proof_previo**2).encode()).hexdigest()
        if hash_operation[:6] != '000001':
            return False
        index_bloque+= 1

    return True

    #hasH de sesion         
def hash(BC_sesion):
    codificacion_bloque = json.dumps(BC_sesion, sort_keys = True).encode()
    #print(codificacion_bloque)
    #print(hashlib.sha3_256(codificacion_bloque).hexdigest())
    return hashlib.sha3_256(codificacion_bloque).hexdigest()
    #return hashlib.sha256(codificacion_bloque).hexdigest()

    #hasH de sesion  
def minar_sesion(FK_empresa):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0]) #consulta del numero de registros
    conexion.commit()
    Con_bloque= str(len_cadena-1)
    Index=cad_num(consulta_one_DB_STR('Index','cadena','Index',Con_bloque))
    Index_nuevo=int(Con_bloque)+2
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    proof_previo= cad_num(consulta_one_DB_STR('proof','cadena','Index',len_cadena))
    proof =proof_of_work(proof_previo)
    hash_previo =consulta_varc_Str('Hash_previo','cadena','Index',Con_bloque) 
    BC_sesion= bloque_sesion(proof,hash_previo,FK_empresa,Index)
    #hash_bloque=hash(hash_previo)
    hash_bloque=hash(BC_sesion)
    Sql_up="INSERT INTO cadena (`Index`,`proof`,`time`,`Tipo_bloque`,`Hash_previo`,`ID_FK_entidad`) VALUES (%s,%s,%s,%s,%s,%s)"
    complemento=(Index_nuevo,proof,marca_tiempo,1,hash_bloque,FK_empresa)
    cursor.execute(Sql_up,complemento)
    conexion.commit()
    validar=cadena_valida()
    if validar== True:
        print('bloque validado y  adicionado a la cadena')
    else:
        print('Bloque  corrupto')        
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
        #print (Con_empresa)
        minar_sesion(Con_empresa)
        claves_dinamicas(correo)
        autorizacion=1
    else:
        autorizacion=0
    return autorizacion    
##usuario
def bloque_usuario(proof,hash_previo,nombre,apellido,rol,identidicacion,correo,us_hash,id_entidad,ciudad,provincia,pais,u_status,index):
    #estructura de datos del bloque
    Cd_timepo = datetime.now()
    BC_usuario = {
        'index' : index, 
        'timestamp': Cd_timepo.strftime('%Y-%m-%d %H:%M:%S'),
        'tipo_bloque':'2', 
        'Nombre':  nombre, 
        'Apellido':  apellido,
        'ROL': rol, 
        'Id_idendificacion' : identidicacion,
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
    return BC_usuario
# Se mina el usuario para Activacion  del user 
def activar_user(nombre, apellido,cc,correo,fk_entidad,pais,provincia,ciudad,rol,Adm):
    #conexio a DB
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    #obtencion de data de db
    len_cadena=cad_num(cursor.fetchall()[0])
    Con_bloque= str(len_cadena-1)
    Index=cad_num(consulta_one_DB_STR('Index','cadena','Index',Con_bloque))
    Index_nuevo=int(Con_bloque)+2
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    proof_previo= cad_num(consulta_one_DB_STR('proof','cadena','Index',Index))
    proof =proof_of_work(proof_previo)
    hash_previo =consulta_varc_Str('Hash_previo','cadena','Index',Con_bloque) 
    #Generacion de identidad unica de usuario 
    us_hash=generar_id_hash(cc,marca_tiempo,nombre,Adm,Con_bloque)
    #creasion de vloque y  validacion
    BC_sesion= bloque_usuario(proof,hash_previo,nombre,apellido,rol,cc,correo,us_hash,fk_entidad,ciudad,provincia,pais,1,Index_nuevo)
    hash_bloque=hash(BC_sesion)
    Sql_up=("UPDATE `usuario` SET `US_HASH`= %s ,`US_STATUS`= %s  WHERE `CORREO`=%s")
    complemento=(us_hash,1,correo)
    cursor.execute(Sql_up,complemento)
    Sql_up="INSERT INTO cadena (`Index`,`proof`,`time`,`Tipo_bloque`,`Hash_previo`,`ID_FK_entidad`) VALUES (%s,%s,%s,%s,%s,%s)"
    complemento=(Index_nuevo,proof,marca_tiempo,2,hash_bloque,1)
    cursor.execute(Sql_up,complemento)
    conexion.commit()
    conexion.close()
#Entidad#
#se define el bloque  que contiene la estructura de datos de entidad
def bloque_entidad(proof,hash_previo,n_entidad,nic,n_correo,direccion,e_ciudad,e_provincia,e_pais,n_licencias,l_activas,e_status,Index):
    Cd_timepo = datetime.now()

    BC_entidad = {  
        'index' : Index, 
        'timestamp': Cd_timepo.strftime('%Y-%m-%d %H:%M:%S'),
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
    return BC_entidad 
def activar_enti(n_entidad,nic,n_correo,direccion,e_ciudad,e_provincia,e_pais,n_licencias,l_activas):
    #conexio a DB
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    #obtencion de data de db
    len_cadena=cad_num(cursor.fetchall()[0])
    Con_bloque= str(len_cadena-1)
    Index=cad_num(consulta_one_DB_STR('Index','cadena','Index',Con_bloque))
    Index_nuevo=int(Con_bloque)+2
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    proof_previo= cad_num(consulta_one_DB_STR('proof','cadena','Index',Index))
    print(proof_previo)
    print(Index)
    proof =proof_of_work(proof_previo)
    hash_previo =consulta_varc_Str('Hash_previo','cadena','Index',Con_bloque) 
    #Generacion de identidad unica de entidad 
    IDE_hash=generar_id_hash(nic,marca_tiempo,n_entidad,'Lichain',Con_bloque)
    #creasion de vloque y  validacion
    BC_sesion = bloque_entidad(proof,hash_previo,n_entidad,nic,n_correo,direccion,e_ciudad,e_provincia,e_pais,n_licencias,l_activas,1,Index_nuevo)
    hash_bloque=hash(BC_sesion)
    Sql_up=("UPDATE `entidad` SET `ID_EHash`= %s ,`E_STATUS`= %s  WHERE `E_EMAIL`=%s")
    complemento=(IDE_hash,1,n_correo)
    cursor.execute(Sql_up,complemento)
    Sql_up="INSERT INTO cadena (`Index`,`proof`,`time`,`Tipo_bloque`,`Hash_previo`,`ID_FK_entidad`) VALUES (%s,%s,%s,%s,%s,%s)"
    complemento=(Index_nuevo,proof,marca_tiempo,3,hash_bloque,1)
    cursor.execute(Sql_up,complemento)
    conexion.commit()
    conexion.close()
### Licencias
def  Li_total(ID_empresa):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()    
    SQL="SELECT NUM_LICENCIAS FROM entidad WHERE ID_ENTIDAD=%s"
    cursor.execute(SQL,ID_empresa)
    N_total= str(cad_num(cursor.fetchall()[0]))
    return N_total
    conexion.commit()
    conexion.close()
def Li_Acti(ID_empresa):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()    
    #se obtiene el numero de licencias activas
    SQL="SELECT COUNT(*) FROM licencia WHERE FK_ID_ENTIDAD=%s AND STATUS=1"
    cursor.execute(SQL,ID_empresa)
    N_Act= str(cad_num(cursor.fetchall()[0]))
    return N_Act
    conexion.commit()
    conexion.close()
def Li_Ven(ID_empresa):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()    
    #se obtiene el numero de licencias activas
    SQL="SELECT COUNT(*) FROM licencia WHERE FK_ID_ENTIDAD=%s AND STATUS=2"
    cursor.execute(SQL,ID_empresa)
    N_Ven= str(cad_num(cursor.fetchall()[0]))
    return N_Ven
    conexion.commit()
    conexion.close()    
def Li_Dis(ID_empresa):
     
    Li_t= int(Li_total(ID_empresa))
    Li_activ= int(Li_Acti(ID_empresa))
    Li_venc=int(Li_Ven(ID_empresa))
    
    Li_dipo= str(Li_t-(Li_activ+Li_venc))
    return Li_dipo
    
def bloque_Licencia(proof,hash_previo,L_t,L_a,L_v,L_d,id_cliente,id_entidad,fecha_activate,l_status,Index):
    Cd_timepo = datetime.now()
        #estructura de datos del bloque
    BC_licencia = {
        'index' : Index, 
        'timestamp': Cd_timepo.strftime('%Y-%m-%d %H:%M:%S'),
        'tipo_bloque':'4', 
        'Li_T':  L_t,
        'Li_A':  L_a,
        'Li_v':  L_v,
        'Li_d':  L_d, 
        'Id_cliente': id_cliente,
        'Id_entidad': id_entidad,
        'fecha_activate': fecha_activate,
        'status':l_status,
        'proof': proof ,
        'hash_previo': hash_previo
        }
    return(BC_licencia)

def activar_li(CORREO):
   #se valida que el usuario  y la empresa  esten habilitados para activar licencias
   status_li=0
   valor = consulta_status_usuario(CORREO)
   if valor==1:
       #se  carga el numero de licencias

       #conexio a DB
        conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
        cursor = conexion.cursor()
        #obtemos  el ID de la entidad a la que pertenece  el usuario
        SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO=%s"
        cursor.execute(SQL,CORREO)
        Con_empresa=cad_num(cursor.fetchone())
        #obtenemos el numero  de licencias que posee el usuario
        L_total= int(Li_total(Con_empresa)) #licencias totales de la entidad
        L_Acti=  int(Li_Acti(Con_empresa))  #licencias activas de la entidad
        L_Ven=   int(Li_Ven(Con_empresa))   #licencias vencidas de la  entidad
        L_di=    int(Li_Dis(Con_empresa))   #licencias disponibles de la entidad

        if(L_di>0):
            ##validaciones
            status_li='1'
            
            #se inicia proceso de activacion 
            conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
            cursor = conexion.cursor()
            SQL="SELECT COUNT(*) FROM cadena"
            cursor.execute(SQL)
            #obtencion de data de db
            len_cadena=cad_num(cursor.fetchall()[0])
            Con_bloque= str(len_cadena-1)
            Index=cad_num(consulta_one_DB_STR('Index','cadena','Index',Con_bloque))
            Index_nuevo=int(Con_bloque)+2
            Cd_timepo = datetime.now()
            marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
            proof_previo= cad_num(consulta_one_DB_STR('proof','cadena','Index',Index))
           
          
            proof =proof_of_work(proof_previo)
            hash_previo =consulta_varc_Str('Hash_previo','cadena','Index',Con_bloque)
            #Obtener el ID del usuario#
            SQL="SELECT ID_Usuario FROM usuario WHERE CORREO=%s"
            cursor.execute(SQL,CORREO)
            ID_us_L= cad_num(cursor.fetchone()) 
            BC_sesion = bloque_Licencia(proof,hash_previo,L_total,L_Acti,L_Ven,L_di,ID_us_L,Con_empresa,marca_tiempo,1,Index_nuevo)
            hash_bloque=hash(BC_sesion)
            #Generacion del codigo de licencia
            Codigo_li = licenciar(hash_bloque)
            #Actuaizacion de licencia
            Sql_li="INSERT INTO licencia (`COD_SHA`,`L_CODIGO`,`FK_ID_CLIENTE`,`FK_ID_ENTIDAD`,`TIME_ACT_L`,`STATUS`) VALUES(%s,%s,%s,%s,%s,%s)"
            compl_li=(hash_bloque,Codigo_li,ID_us_L,Con_empresa,marca_tiempo,1)
            cursor.execute(Sql_li,compl_li)
            conexion.commit()
            Sql_up="INSERT INTO cadena (`Index`,`proof`,`time`,`Tipo_bloque`,`Hash_previo`,`ID_FK_entidad`) VALUES (%s,%s,%s,%s,%s,%s)"
            complemento=(Index_nuevo,proof,marca_tiempo,4,hash_bloque,Con_empresa)
            cursor.execute(Sql_up,complemento)
            conexion.commit()
            conexion.close()
            return status_li
        elif(L_di==0):
            ## Mensaje de error  
            status_li = '2'
            return status_li
                
   else:
       status_li= '3'
       return status_li  
def Obt_cod(CORREO):
    #conexio a DB
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    #obtemos  el ID de la entidad a la que pertenece  el usuario
    SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO=%s"
    cursor.execute(SQL,CORREO)
    Con_empresa=cad_num(cursor.fetchone())
    SQL="SELECT ID_Usuario FROM usuario WHERE CORREO=%s"
    cursor.execute(SQL,CORREO)
    ID_us_L= cad_num(cursor.fetchone()) 
    SQL="SELECT MAX(ID_LICENCIA) FROM licencia WHERE FK_ID_CLIENTE=%s AND FK_ID_ENTIDAD=%s"
    comple=(ID_us_L,Con_empresa)
    cursor.execute(SQL,comple)
    id_cod = cad_num(cursor.fetchone())
    SQL="SELECT L_CODIGO FROM licencia WHERE ID_LICENCIA=%s"
    cursor.execute(SQL,id_cod)
    tempo_cod=str(cursor.fetchone())
    CODIGO_act= Format_L(re.sub(r'[^\w]','', str(tempo_cod)))
    conexion.commit()
    conexion.close()
    return CODIGO_act 

def comprar_li (numer_L,correo):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    #obtemos  el ID de la entidad a la que pertenece  el usuario
    SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO=%s"
    cursor.execute(SQL,correo)
    id_enti=cad_num(cursor.fetchone())
    num_lic= int(Li_total(id_enti))   
    add_num= int(numer_L)
    ## en este segmento se ingresaria  validacion de pago si se desea agregar 
    ## algun agente bancario
    store_L=  num_lic + add_num
    #validamos la transaccion
    minar_sesion(id_enti)
    SQL="UPDATE `entidad` SET `NUM_LICENCIAS`=%s WHERE `ID_ENTIDAD`=%s"
    comple=(store_L,id_enti)
    cursor.execute(SQL,comple)
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    #obtencion de data de db
    len_cadena=cad_num(cursor.fetchall()[0])
    conexion.commit()
    SQL="SELECT Hash_previo FROM cadena WHERE Id_Cadena=%s"
    cursor.execute(SQL,(len_cadena+1))
    hash_transa= cursor.fetchone()
    hashin=re.sub(r'[^\w]','',str(hash_transa))
    conexion.commit()
    conexion.close()
    return hashin

def certi_us(CORREO):      
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    #consultas#
    SQL="SELECT NOMBRE FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_nombre = cursor.fetchone()[0]
    SQL="SELECT APELLIDO FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_apellido=cursor.fetchone()[0]
    SQL="SELECT ID_IDENTIFICACION FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    CC_us=str(cursor.fetchone()[0])
    SQL="SELECT PAIS FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_pa=cursor.fetchone()[0]
    SQL="SELECT PROVINCIA FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_pr=cursor.fetchone()[0]
    SQL="SELECT CIUDAD FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_ci=cursor.fetchone()[0]
    ubicacion = temp_ci+'-'+temp_pr+'-'+temp_pa
    SQL="SELECT US_HASH FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    hash_us=cursor.fetchone()[0]
    SQL="SELECT US_STATUS FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    estatus=cursor.fetchone()[0]
    print(estatus)
    if(estatus==1):
        esta_u='Activo'
    else:
        esta_u='Inactivo'        
    nombre = temp_nombre+' '+temp_apellido
    SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    id_enti=cursor.fetchone()[0]
    SQL="SELECT N_ENTIDAD FROM entidad WHERE ID_ENTIDAD = %s"
    cursor.execute(SQL,id_enti)
    enti_us=cursor.fetchone()[0]
    minar_sesion(id_enti)
    conexion.commit()

    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0])
    SQL="SELECT Hash_previo FROM cadena WHERE Id_Cadena=%s"
    cursor.execute(SQL,len_cadena)
    hash_t=cursor.fetchone()[0]
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    Cer_dia = Cd_timepo.strftime('%d')
    Cer_mes = Cd_timepo.strftime('%m')
    Cer_ano = Cd_timepo.strftime('%Y')
    Cer_hora = Cd_timepo.strftime('%H:%M:%S')

    hash_QR = hash_us + ' - ' + hash_t + '- Firma Digital -' + marca_tiempo + '- Sistema de licensamiento - LICHAIN - '
    conexion.commit()
    conexion.close()
    
    #Generacion de QR#
    qr = qrcode.QRCode(
    version=12,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=5.9,
    border=4
    )
    qr.add_data(hash_QR)
    qr.make()
    im2 = qr.make_image(fill_color="black", back_color="#ffffff")    
    im1=Image.open("blockchain/plan_us.jpg")
    back_im = im1.copy()
    back_im.paste(im2,(1390,504))
    #texto#
    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",55 )
    #textos#

    text = nombre  
    draw.text((510,534), text , font=font, fill="Black",align="center")
    
    text = 'Con C.c ' + CC_us
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Italic.otf",30)  
    draw.text((570,590), text , font=font, fill="Black",align="center")

    text = esta_u
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",35)  
    draw.text((465,690), text , font=font, fill="Black",align="center")
   
    text = "Se encuentra " +"                    "+ " en la plataforma de licenciamiento \n como gestor de las licencias de la entidad "
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Regular.otf",35)  
    draw.text((235,690), text , font=font, fill="Black",align="center")

    text = enti_us
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",55)  
    draw.text((255,790), text , font=font, fill="Black",align="center")

    text = 'Certificado emitido a los '+ Cer_dia + ' del ' + Cer_mes + ' del ' + Cer_ano  
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Italic.otf",35)  
    draw.text((380,890), text , font=font, fill="Black",align="center")


    back_im.save('blockchain/temporal.pdf')
    #envio al correo#
      #Envio de codigo a correo 
    temporal = "blockchain/temporal"+".pdf"
    correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura") # Datos de acceso al correo del proyecto
    correo.send(
        to= CORREO,
        subject= "Certificado Usuario- LICHAIN",
        contents=["Lichain, hace entrega de la solicitud de cerificado de Usuario: ",temporal]
        )
    os.remove(temporal)    
    print("su correo fue enviado correctamente")

def certi_en(CORREO):
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    #consultas#
    #id_entidad
    SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    id_enti=cursor.fetchone()[0]
    #nic
    SQL="SELECT NIC FROM entidad WHERE ID_ENTIDAD = %s"
    cursor.execute(SQL,id_enti)
    CC_en=str(cursor.fetchone()[0])
    #hash
    SQL="SELECT ID_EHASH FROM entidad WHERE ID_ENTIDAD = %s"
    cursor.execute(SQL,id_enti)
    hash_en=cursor.fetchone()[0]
    #status
    SQL="SELECT E_STATUS FROM entidad WHERE ID_ENTIDAD = %s"
    cursor.execute(SQL,id_enti)
    estatus=cursor.fetchone()[0]
    
    print(estatus)
    if(estatus==1):
        esta_en='Activo'
    else:
        esta_en='Inactivo'        
    
    #nombre

    SQL="SELECT N_ENTIDAD FROM entidad WHERE ID_ENTIDAD = %s"
    cursor.execute(SQL,id_enti)
    enti_en=cursor.fetchone()[0]
    minar_sesion(id_enti)
    conexion.commit()

    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0])
    SQL="SELECT Hash_previo FROM cadena WHERE Id_Cadena=%s"
    cursor.execute(SQL,len_cadena)
    hash_t=cursor.fetchone()[0]
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    Cer_dia = Cd_timepo.strftime('%d')
    Cer_mes = Cd_timepo.strftime('%m')
    Cer_ano = Cd_timepo.strftime('%Y')
    Cer_hora = Cd_timepo.strftime('%H:%M:%S')

    hash_QR = hash_en + ' - ' + hash_t + '- Firma Digital -' + marca_tiempo + '- Sistema de licensamiento - LICHAIN - '
    conexion.commit()
    conexion.close()
    
    #Generacion de QR#
    qr = qrcode.QRCode(
    version=12,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=5.9,
    border=4
    )
    qr.add_data(hash_QR)
    qr.make()
    im2 = qr.make_image(fill_color="black", back_color="#ffffff")    
    im1=Image.open("blockchain/plan_en.jpg")
    back_im = im1.copy()
    back_im.paste(im2,(1390,504))
    #texto#
    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",55 )
    #textos#

    text = enti_en  
    draw.text((255,534), text , font=font, fill="Black",align="center")
    
    text = 'Con NIT ' + CC_en 
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Italic.otf",30)  
    draw.text((570,590), text , font=font, fill="Black",align="center")

    text = esta_en
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",35)  
    draw.text((465,690), text , font=font, fill="Black",align="center")
   
    text = "Se encuentra " +"                    "+ " en la plataforma de licenciamiento \n como una entidad  verificada."
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Regular.otf",35)  
    draw.text((235,690), text , font=font, fill="Black",align="center")

    
    text = 'Certificado emitido a los '+ Cer_dia + ' del ' + Cer_mes + ' del ' + Cer_ano  
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Italic.otf",35)  
    draw.text((380,890), text , font=font, fill="Black",align="center")


    back_im.save('blockchain/temporal_en.pdf')
    temporal = "blockchain/temporal_en"+".pdf"
    correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura") # Datos de acceso al correo del proyecto
    correo.send(
        to= CORREO,
        subject= "Certificado Entidad - LICHAIN",
        contents=["Lichain, hace entrega de la solicitud de cerificado de Entidad: ",temporal]
        )
    os.remove(temporal)    
    print("su correo fue enviado correctamente")

def certi_li(CORREO,id_licencia):      
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    #consultas#

    #Usuario
    SQL="SELECT NOMBRE FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_nombre = cursor.fetchone()[0]

    SQL="SELECT APELLIDO FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    temp_apellido=cursor.fetchone()[0]

    nombre = temp_nombre+' '+temp_apellido
    
    # Empresa

    #id_entidad
    SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    id_enti=cursor.fetchone()[0]

    SQL="SELECT N_ENTIDAD FROM entidad WHERE ID_ENTIDAD = %s"
    cursor.execute(SQL,id_enti)
    enti_li=cursor.fetchone()[0]

    #Licencia
    
    SQL="SELECT L_CODIGO FROM licencia WHERE ID_LICENCIA = %s"
    cursor.execute(SQL,id_licencia)
    codigo=cursor.fetchone()[0]

        
    SQL="SELECT COD_SHA FROM licencia WHERE ID_LICENCIA = %s"
    cursor.execute(SQL,id_licencia)
    Hash_li=cursor.fetchone()[0]


     #vigencia

    SQL="SELECT STATUS FROM licencia WHERE ID_LICENCIA= %s"
    cursor.execute(SQL,id_licencia)
    estatus=cursor.fetchone()[0]
    
    if(estatus==1):
        esta_li='Activo'
    elif(estatus==0):
        esta_li='No registra'
    else:
        esta_li='Vencida'

    #Marca de tiempo
    SQL="SELECT TIME_ACT_L FROM licencia WHERE ID_LICENCIA= %s"
    cursor.execute(SQL,id_licencia)
    time_li =cursor.fetchone()[0]  
     
    Cd_timepo = datetime.now()
    marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
    Cer_dia = Cd_timepo.strftime('%d')
    Cer_mes = Cd_timepo.strftime('%m')
    Cer_ano = Cd_timepo.strftime('%Y')
    Cer_hora = Cd_timepo.strftime('%H:%M:%S')

    
    
    #temp_li_1 = int( re.sub(r'[^\w]','', time_li))
    #temp_li_2 = int( re.sub(r'[^\w]','', marca_tiempo))

    #vigen_li= temp_li_1 - temp_li_2
    #vigen_li =vigen_li*-1
    temp_li_1_str =  re.sub(r'[^\w]','', time_li)
    año_new = str(int( temp_li_1_str[0:4]) + 1)
  


    formato_time_li_1 =  temp_li_1_str[0:4] +'/'+temp_li_1_str[4:6]+'/'+temp_li_1_str[6:8]
    formato_time_li_2 =  año_new +'/'+temp_li_1_str[4:6]+'/'+temp_li_1_str[6:8]
    vigen_li= formato_time_li_1+ ' - ' + formato_time_li_2      
    
    #minar la sesion 
    minar_sesion(id_enti)
    conexion.commit()

    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0])
    SQL="SELECT Hash_previo FROM cadena WHERE Id_Cadena=%s"
    cursor.execute(SQL,len_cadena)
    hash_t=cursor.fetchone()[0]
    



    hash_QR = Hash_li + ' - ' + hash_t + '- Firma Digital -' + marca_tiempo + '- Sistema de licensamiento - LICHAIN - '
    conexion.commit()
    conexion.close()
    
    #Generacion de QR#
    qr = qrcode.QRCode(
    version=12,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=5.9,
    border=4
    )
    qr.add_data(hash_QR)
    qr.make()
    im2 = qr.make_image(fill_color="black", back_color="#ffffff")    
    im1=Image.open("blockchain/plan_li.jpg") 
    back_im = im1.copy()
    back_im.paste(im2,(1390,504))
    #texto#
    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",55 )
    #textos#

    text = codigo  
    draw.text((155,534), text , font=font, fill="Black",align="center")
    
    text = 'Vigencia :' + vigen_li
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Italic.otf",20)  
    draw.text((550,600), text , font=font, fill="Black",align="center")


    text = esta_li
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",35)  
    draw.text((480,690), text , font=font, fill="Black",align="center")
   
    text = "Se encuentra " +"                    "+ " en la plataforma de licenciamiento \n y esta asigando a la  "
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Regular.otf",35)  
    draw.text((235,690), text , font=font, fill="Black",align="center")

    text = enti_li
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Bold.otf",45)  
    draw.text((350,790), text , font=font, fill="Black",align="center")

    text = 'Certificado emitido a los '+ Cer_dia + ' del ' + Cer_mes + ' del ' + Cer_ano  
    font = ImageFont.truetype("C:/Users/homer/Downloads/aleo/Aleo-Italic.otf",35)  
    draw.text((380,890), text , font=font, fill="Black",align="center")


    back_im.save('blockchain/temporal_li.pdf') 
    temporal = "blockchain/temporal_li"+".pdf"
    correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura") # Datos de acceso al correo del proyecto
    correo.send(
        to= CORREO,
        subject= "Certificado Licencia - LICHAIN",
        contents=["Lichain, hace entrega de la solicitud de cerificado de Codifo de licencia: ",temporal]
        )
    os.remove(temporal)    
    print("su correo fue enviado correctamente")
def soporte (CORREO,come):
    #conexion
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()

    SQL="SELECT FK_ID_ENTIDAD FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    id_enti=cursor.fetchone()[0]

    SQL="SELECT ID_Usuario FROM usuario WHERE CORREO = %s"
    cursor.execute(SQL,CORREO)
    id_user=cursor.fetchone()[0]

    Sql_li="INSERT INTO soporte (`FK_ID_USUARIO`,`FK_ID_ENTIDAD`,`COMENT`,`STATUS`) VALUES(%s,%s,%s,%s)"
    complemen=(id_user,id_enti,come,0)
    cursor.execute(Sql_li,complemen)
    conexion.commit()
    conexion.close()

def validacion():
    index_bloque= 1         #indexamos el bloque
    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    len_cadena=cad_num(cursor.fetchall()[0]) #consulta del numero de registros
    conexion.commit()


    while   index_bloque< len_cadena:


        SQL="SELECT `proof` FROM `cadena` WHERE `Id_Cadena` = %s"
        cursor.execute(SQL,index_bloque)
        proof_previo= int(cursor.fetchone()[0])
        #print(str(proof_previo))
            
        SQL="SELECT `proof` FROM `cadena` WHERE `Id_Cadena` = %s"
        cursor.execute(SQL,(index_bloque+1))
        proof_nuevo= int(cursor.fetchone()[0])
      
        print(str(proof_nuevo))

        hash_operation = hashlib.sha256(str(proof_nuevo**2 - proof_previo**2).encode()).hexdigest()
        
        print(hash_operation)
        
        if hash_operation[:6] != '000001':
            return False
       
        index_bloque+= 1

    return True

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
def reporte():

    conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
    cursor = conexion.cursor()
    SQL="SELECT COUNT(*) FROM cadena"
    cursor.execute(SQL)
    N_trans=cad_num(cursor.fetchall()[0]) #consulta del numero de transacciones
    SQL="SELECT COUNT(*) FROM cadena WHERE Tipo_bloque=%s"
    cursor.execute(SQL,1)
    #indica el numero de solicitudes
    N_bloque_s=cad_num(cursor.fetchall()[0]) #consulta del numero de bloques  tipo 1
   
    
   

    ################## USUARIOS  ################
    
    SQL="SELECT COUNT(*) FROM usuario"
    cursor.execute(SQL)
    N_usuario=cad_num(cursor.fetchall()[0]) 
    # usuario activos
    SQL="SELECT COUNT(*) FROM usuario WHERE US_STATUS=%s"
    cursor.execute(SQL,1)
    N_bloque_us=cad_num(cursor.fetchall()[0]) #consulta del numero de bloques  tipo 2
    #solicitud de usuarios
    N_user_inac = N_usuario-N_bloque_us

    ###############  ENTIDADES ####################
    
    SQL="SELECT COUNT(*) FROM entidad"
    cursor.execute(SQL)
    N_entidades=cad_num(cursor.fetchall()[0]) 
    # entidades activas
    SQL="SELECT COUNT(*) FROM entidad WHERE E_STATUS=%s"
    cursor.execute(SQL,3)
    #indica el numero de entidades activas
    N_bloque_en=cad_num(cursor.fetchall()[0]) #consulta del numero de bloques  tipo 3
    #solicitud de entides
    N_entid_inac= N_entidades-N_bloque_en

    ################## Licencias #####################

    SQL="SELECT COUNT(*) FROM licencia"
    cursor.execute(SQL)
    N_licencia=cad_num(cursor.fetchall()[0]) 
    #licencias  activas
    SQL="SELECT COUNT(*) FROM licencia WHERE STATUS=%s"
    cursor.execute(SQL,1)
    N_licencia_ac=cad_num(cursor.fetchall()[0])
    #licencias vencidas
    SQL="SELECT COUNT(*) FROM licencia WHERE STATUS=%s"
    cursor.execute(SQL,2)
    N_licencia_ve=cad_num(cursor.fetchall()[0])
    #licencias Disponibles
    x=1
    num_lic_dis=0
    while x!=(N_entidades+1):
        SQL="SELECT `NUM_LICENCIAS` from `entidad` WHERE `ID_ENTIDAD`=%s"
        cursor.execute(SQL,x)
        temp=cursor.fetchone()[0]
        num_lic_dis=num_lic_dis+temp
        temp=0
        x=x+1
    #######################################################
    Cd_timepo = datetime.now()
   
    Cer_dia = Cd_timepo.strftime('%d')
    Cer_mes = Cd_timepo.strftime('%m')
    Cer_ano = Cd_timepo.strftime('%Y')
    
    

    cadena = "EL sistema reporta un total de " + str(N_trans) + " transacciones validas. \n \n"+ "      Informe detallado: \n \n" + "Número de Usuario: " +  str(N_usuario) + "\n"+"Número de Usuario Activos: " +  str(N_bloque_us) + "\n"+"Solicitud de resgistro: " +  str(N_user_inac) + "\n \n"+"Número de Entidas: " +  str(N_entidades) + "\n"+" Número de Entidades Activas: " +  str(N_bloque_en) + "\n"+" Solicitud de resgistro: " +  str(N_entid_inac) + "\n \n"+" Número de Licencias generadas: " +  str(N_licencia) + "\n"+" Número de Licencias Activas: " +  str(N_licencia_ac) + "\n"+" Número de Licencias Vencidas: " + str(N_licencia_ve) + "\n"+" Total de licencias disponibles para activar: " +  str(num_lic_dis) + "\n \n"+ "Informe generado por  Lichain a  los "+ Cer_dia +" del "+ Cer_mes + " del " + Cer_ano
    return cadena
                       
    
