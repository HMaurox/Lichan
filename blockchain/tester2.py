import pymysql
from funciones_Li import*
import json



def activar_li_adm(id_enti):
   #se valida que el usuario  y la empresa  esten habilitados para activar licencias
   status_li=0
  
   conexion = pymysql.connect(host="localhost",user="root",passwd="12345",database="blockchain")
   cursor = conexion.cursor()
   valor = 1 # se salta  la seguridad de validacion por ser adm
   SQL="SELECT CORREO FROM usuario WHERE FK_ID_ENTIDAD =%s"
   cursor.execute(SQL,id_enti)
   CORREO=cursor.fetchone()[0] 


   if valor==1:
       #se  carga el numero de licencias

       #conexio a DB
        
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
            Index=cad_num(consulta_one_DB_STR('Index','cadena','Index',len_cadena))
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


valor= activar_li_adm(1)
print(valor)