
#library
import  hashlib 

#def

def Key_MD5(clave):

    Key_co = clave.encode('utf-8')
    Key_L = hashlib.md5(Key_co)    
    Key_F = Key_L.hexdigest()
    Key_F= Key_F.upper()
    return Key_F

def Format_L(formatos):
    lisen = formatos[0:4]+"-"+formatos[4:8]+"-"+formatos[8:12]+"-"+formatos[12:16]+"-"+formatos[16:20]+"-"+formatos[20:24]+"-"+formatos[24:28]+"-"+formatos[28:32]
    return lisen

def  licenciar(codigo_licencia):    
    Key_str= str(codigo_licencia)
    Temp_lice = Key_MD5(Key_str)
    licencia=Format_L(Temp_lice)
    return licencia
# parametros#
    

