import hashlib
import pymysql
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema
from ElemenChain import activar_user
from funciones_Li import generar_id_hash

#valor= autorizacion_usuario('proing.mauro@gmail.com')
#minar_sesion(1)
#activar_user('Mauro','Avila',1144160700,'proing.mauro@gmail.com',1,'Colombia','Valle del Cauca','Cali',0,'LIchain')

valor=generar_id_hash(1144160700,'1-11-2020 7:24','Maurox','Lichain',3)
print(valor)