import hashlib
import pymysql
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema
from ElemenChain import autorizacion_usuario
from funciones_Li import consulta_status_usuario
from funciones_Li import consulta_one_DB_STR
from funciones_Li import consulta_varc_Str
from funciones_Li import cad_num
from funciones_Li import consulta_correo
from ElemenChain import minar_sesion
from ElemenChain import proof_of_work


valor= autorizacion_usuario('proing.mauro@gmail.com')
print(valor)