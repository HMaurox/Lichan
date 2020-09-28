# Bloque encargado de registrar en cadena de bloques los inicios de sesion de usuarios del aplicatico Lichain
# Se registra   fechas de ingreso , fincalizacion de sesion , nombre de usuario
# Universidad de San  Buenaventura de Cali - Proyecto de grado - Lichain 
#programado por : Herney Mauricio Avila - Felipe Idrobo Avirama 

################################################################################################################
################################# BLOCKCHAIN DE  REGISTRO DE SESION ############################################
################################################################################################################

# Modulos 

import hashlib 
import sys
import os 
import bcrypt
import math
import datetime
import json 
from flask import Flask, jsonify

# Creacion del Bloque

class BLOCKCHAIN_sesion:

    #definicion del bloque inicial 

    def __init__(self):
        self.chain = []
        self.crea_BC_sesion(proof = 1, hash_previo = '0',usuario="Lichain",tipo_us="1",accion_us="0")
    
    #definicion de los datos a contener en el bloque

    def crea_BC_sesion(self,proof,hash_previo,usuario,tipo_us,accion_us):
        #estructura de datos del bloque
        BC_sesion = {
            'index' : len(self.chain) +1, #se aumenta el indice de la cadena
            'timestamp': str(datetime.datetime.now()), # toma el  fecha (dia/mes) y hora del sistema (HH:MM:SS)
            'Usuario':  usuario, #nombre del usuario que inicio sesion 
            'Tipo_us':  tipo_us, # tipo de usuario (Adm (1) o usuario normal (2))
            'Accion' :  accion_us, # logueo (1) o deslogueo (2) , es cero solo cuando se inicia la cadena por primera vez
            'proof':proof , # resultado de la PoW
            'hash_previo': hash_previo # hash previo al bloque
            }
        self.chain.append(BC_sesion)
        return BC_sesion  # se retorna  el bloque parametrizado.

    # obtener hash previo
    
    def get_bloque_previo(self):
        return self.chain[-1]

   # Definicion del Pow      
    def proof_of_work(self, proof_previo):
        nuevo_proof = 1   #creamos prueba de trabajo
        valida_proof = False # asumimos que  la interacion es falasa para  frozar la validacion
        while valida_proof is False:
            hash_operation = hashlib.sha256(str(nuevo_proof**2 - proof_previo**2).encode()).hexdigest() #minado de respuesta
            if hash_operation[:6] == '000001': #  citerio de busqueda
                valida_proof = True
            else:
                nuevo_proof += 1
        return nuevo_proof

    # creacion de archivos Json y  generacion de hash 
    def hash(self, BC_sesion):
        codificacion_bloque = json.dumps(BC_sesion, sort_keys = True).encode()
        return hashlib.sha256(codificacion_bloque).hexdigest()
    
    # Validacion de bloques
    
    def cadena_valida(self, chain):
        bloque_previo = chain[0] #obtiene bloque previo
        index_bloque= 1          #indexamos el bloque
        #inicio de validacion del bloque
        while   index_bloque< len(chain):
            BC_sesion = chain[index_bloque]
            if BC_sesion['hash_previo'] != self.hash(bloque_previo):
                return False
            proof_previo = bloque_previo['proof']
            proof = BC_sesion['proof']
            hash_operation = hashlib.sha256(str(nuevo_proof**2 - proof_previo**2).encode()).hexdigest()
            if hash_operation[:6] != '000001':
                return False
            bloque_previo = BC_sesion
            index_bloque+= 1
        return True

##########################################################################################################################
######################                                   Minar Bloque                      ###############################
##########################################################################################################################

# colocamos el elace a  app Flask

app = Flask(__name__)
blockchain_sesion = BLOCKCHAIN_sesion()  ## llamamos nuestro  clase 
## ordenes para  frozar minado
# Minando un Nuevo Bloque
@app.route('/mine_block', methods=['GET'])

## mina solo un bloque 

def minar_block():
    bloque_previo = blockchain_sesion.get_bloque_previo()
    proof_previo  = bloque_previo['proof']
    proof = blockchain_sesion.proof_of_work(proof_previo)
    hash_previo= blockchain_sesion.hash(bloque_previo)
    BC_sesion = blockchain_sesion.crea_BC_sesion (proof,hash_previo,'Mauricio','1','1')
    response = {'message':'Felicidades, haz minado un bloque!',
                'index':BC_sesion['index'],
                'timestamp':BC_sesion['timestamp'],
                'Usuario': BC_sesion['Usuario'], 
                'Tipo_us': BC_sesion['Tipo_us'], 
                'Accion' : BC_sesion['Accion'],  
                'proof':BC_sesion['proof'],
                'hash_previo':BC_sesion['hash_previo']}
    return jsonify(response), 200

##  Cadena 

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = { 'chain': blockchain_sesion.chain,
                 'length': len(blockchain_sesion.chain)
                 }
    return jsonify(response), 200

app.run(host='0.0.0.0', port='5000') # configuracion 

   
    





     
    
