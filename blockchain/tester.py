from funciones_Li import*
import pymysql


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

    print("numero de resgistros "+ str(N_trans))
    print("numero de usuarios "+ str(N_usuario))
    print("numero de usuarios activos " + str(N_bloque_us))
    print("numero de usuarios incativos " + str(N_user_inac))
    print("numero de entidades" + str(N_entidades))
    print("numero de entidades activos " + str(N_bloque_en))
    print("numero de entidades incativos " + str(N_entid_inac))
    print("numero de licencias" + str(N_licencia))
    print("numero de licencias activas " + str(N_licencia_ac))
    print("numero de licencias venciadas " + str(N_licencia_ve))
    print("numero de licencias disponibles "+ str(num_lic_dis))


reporte()


    





