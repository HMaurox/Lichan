import hashlib
import os
import sys
import bcrypt
import pdfkit
from funciones_Li import*
from datetime import date      #modulo de captura de  fechas del sistema
from datetime import datetime  #modulo de captura de  tiempo del sistema
from flask import Flask, render_template, request, redirect, url_for, session ,flash
from flask_mysqldb import MySQL, MySQLdb
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'blockchain'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route("/")
def index():
    if 'NOMBRE' in session:
        if Rol() == 0:
            return render_template("home.html")
        else:
            return render_template("home_admin.html")
    else:
        return render_template("login_clave.html")


@app.route("/home")
def home():
    if 'NOMBRE' in session:
        if Rol() == 0:
            return render_template("home.html")
        else:
            return render_template("home_admin.html")
    else:
        return render_template("login.html")

@app.route("/validate",methods=['GET','POST'])
def validate():
    if 'NOMBRE' in session:
        if Rol() == 0:
            if request.method == 'GET':
                return render_template("home.html")
        else:
            if request.method == 'GET':
                return render_template("validate.html")

            if request.method == 'POST':
                consulta = request.form['gender']
                print(consulta)

                if consulta == 'user':
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM usuario WHERE US_STATUS=0")
                    data_user = cur.fetchall()
                    cur.close()
                    print(data_user)
                    return render_template("validate.html", usuario=data_user)
                elif consulta == 'ent':

                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM entidad WHERE E_STATUS=0")
                    data_ent = cur.fetchall()
                    cur.close()
                    print(data_ent)
                    return render_template("validate.html", entidad=data_ent)

    else:
        return render_template("login.html")


@app.route("/query", methods=['GET', 'POST'])
def query():
    if 'NOMBRE' in session:
        if Rol() == 0:

            if request.method == 'GET':

                return render_template("query.html")

            else:
                consulta = request.form['gender']
                print(consulta)

                if consulta == 'user':
                    CORREO = session['CORREO']
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM usuario WHERE CORREO=%s", (CORREO,))
                    data_user = cur.fetchall()
                    cur.close()
                    print(data_user)
                    return render_template("query.html",usuario=data_user)
                elif consulta == 'ent':
                    EMPRESA = session['EMPRESA']
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM entidad WHERE N_ENTIDAD=%s", (EMPRESA,))
                    data_ent = cur.fetchall()
                    cur.close()
                    print(data_ent)
                    return render_template("query.html", entidad=data_ent)
                elif consulta == 'lic':
                    ID_USER = info_act_lic(session['CORREO'])
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM licencia WHERE FK_ID_CLINETE=%s", (ID_USER,))
                    data_lic = cur.fetchall()
                    cur.close()
                    print(data_lic)
                    return render_template("query.html", licencia=data_lic)
        else:

            if request.method == 'GET':
                return render_template("query_admin.html")
            else:
                consulta = request.form['gender']
                print(consulta)

                if consulta == 'user':

                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM usuario")
                    data_user = cur.fetchall()
                    cur.close()
                    print(data_user)
                    return render_template("query_admin.html", usuario=data_user)
                elif consulta == 'ent':

                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM entidad ")
                    data_ent = cur.fetchall()
                    cur.close()
                    print(data_ent)
                    return render_template("query_admin.html", entidad=data_ent)
                elif consulta == 'lic':

                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM licencia ")
                    data_lic = cur.fetchall()
                    cur.close()
                    print(data_lic)
                    return render_template("query_admin.html", licencia=data_lic)


    else:

        return render_template("login-html")


@app.route("/buy_lic")
def buy_lic():
    if 'NOMBRE' in session:
        if Rol() == 0:
            return render_template("buy_lic.html")
        else:
            return render_template("buy_lic_admin.html")
    else:
        return render_template("login.html")


@app.route("/act_lic",  methods=["GET", "POST"])
def act_lic():
    if 'NOMBRE' in session:
        if Rol() == 0:

            if request.method == 'GET':

                EMPRESA = session['EMPRESA']
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM entidad WHERE N_ENTIDAD=%s", (EMPRESA,))
                data = cur.fetchone()
                ID_EMPRESA = data['ID_ENTIDAD']
                Lic_Activas = Li_Acti(ID_EMPRESA)
                Lic_Inactivas = Li_Dis(ID_EMPRESA)
                Lic_Vencidas = Li_Ven(ID_EMPRESA)
                return render_template("act_lic.html",Lic_Vencidas=Lic_Vencidas,Lic_Activas=Lic_Activas,Lic_Inactivas=Lic_Inactivas)


            if request.method == 'POST':
                response_li = activar_li(session['CORREO'])
                response_cod_li = Obt_cod(session['CORREO'])
                if response_li == "1":
                    res = "Bloque minado con exito"
                elif response_li == "2":
                    res = "No posees licencias disponibles"
                elif response_li == "3":
                    res = "Usuario o empresa sin activación"        
                
                return render_template("act_lic.html",res=res,response_cod_li=response_cod_li)

        else:

            if request.method == 'GET':

                return render_template("act_lic_admin.html")

            if request.method == 'POST':

                ENTIDAD = request.form['N_ENTIDAD']
                cur = mysql.connection.cursor()
                cur.execute("SELECT *  FROM entidad WHERE N_ENTIDAD=%s ", (ENTIDAD,))
                ent = cur.fetchone()
                ID_ENTIDAD = int(ent['ID_ENTIDAD'])
                cur.execute("SELECT *  FROM licencia WHERE FK_ID_ENTIDAD=%s AND STATUS=0 ", (ID_ENTIDAD,))
                data = cur.fetchall()
                return render_template("act_lic_admin.html",licencia=data)

    else:
        return render_template("login.html")



@app.route("/support")
def support():
    if 'NOMBRE' in session:
        if Rol() == 0:
            return render_template("support.html")
        else:
            return render_template("support_admin.html")
    else:
        return render_template("login.html")

@app.route("/register")
def register():
    if 'NOMBRE' in session:
        if Rol() == 0:
            return render_template("register.html")
        else:
            return render_template("register_admin.html")
    else:
        return render_template("login.html")


@app.route("/certificate",methods=['GET'])
def certificate():
   if request.method == 'GET':
        if 'NOMBRE' in session:
            if Rol() == 0:
                ID_USER = info_act_lic(session['CORREO'])
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT * FROM licencia WHERE FK_ID_CLINETE=%s", (ID_USER,))
                data_lic = cur.fetchall()
                cur.close()
                print(data_lic)
                return render_template("certificate.html", licencia=data_lic)
            else:
                return render_template("certificate_admin.html")
        else:
            return render_template("login.html")
   else:
       return render_template("certificate.html")


@app.route("/gen_cert/<string:L_CODIGO>/<string:STATUS>", methods=['GET'])
def gen_cert(L_CODIGO,STATUS):

    if request.method == 'GET':
        if 'NOMBRE' in session:

           env = Environment(loader=FileSystemLoader("templates"))
           template = env.get_template("reporte.html")
           if STATUS == 0:
               STATUS_REF = 'Ináctivo'
           else:
               STATUS_REF = 'Activo'
           usuario = {
               'nombre': session['NOMBRE'],
               'empresa': session['EMPRESA'],
               'licencias': L_CODIGO,
               'status': STATUS_REF,
           }

           html = template.render(usuario)
           options = {
               'page-size': 'A5',
               'margin-top': '0.1in',
               'margin-right': '0.1in',
               'margin-bottom': '0.1in',
               'margin-left': '0.1in',

           }

           pdfkit.from_string(html, 'Certificado.pdf', options=options)
           return render_template("home.html")
        else:
            return render_template("home.html")
    else:
        return render_template("home.html")


@app.route('/register_ent', methods=["GET", "POST"])
def register_ent():
    if request.method == 'GET':
        return render_template("register_ent.html")
    else:
        N_ENTIDAD = request.form['N_ENTIDAD']
        NIC = request.form['NIC']
        E_EMAIL = request.form['E_EMAIL']
        E_PAIS = request.form['E_PAIS']
        E_PROVINCIA = request.form['E_PROVINCIA']
        E_CIUDAD = request.form['E_CIUDAD']
        E_DIRECCION = request.form['E_DIRECCION']
        NUM_LICENCIAS = request.form['NUM_LICENCIAS']

        Cd_timepo = datetime.now() # Captura la marca de tiempo del sistema
        marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')
        ID_EHash=generar_id_hash(NIC,marca_tiempo,N_ENTIDAD,'Lichain','1')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO entidad (N_ENTIDAD,NIC,E_EMAIL,E_PAIS,E_PROVINCIA,E_CIUDAD,E_DIRECCION,NUM_LICENCIAS,ID_EHash) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (N_ENTIDAD, NIC, E_EMAIL, E_PAIS, E_PROVINCIA, E_CIUDAD, E_DIRECCION, NUM_LICENCIAS,ID_EHash))
        mysql.connection.commit()
        minar_sesion(1)
        return redirect(url_for('index'))


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM entidad")
        data = cur.fetchall()
        cur.close()
        return render_template('register_user.html', entidad=data)
    else:

        NOMBRE = request.form['NOMBRE']
        APELLIDO = request.form['APELLIDO']
        ID_IDENTIFICACION = request.form['ID_IDENTIFICACION']
        CORREO = request.form['CORREO']
        FK_ID_ENTIDAD = request.form['FK_ID_ENTIDAD']
        PAIS = request.form['PAIS']
        PROVINCIA = request.form['PROVINCIA']
        CIUDAD = request.form['CIUDAD']

        Cd_timepo = datetime.now()
        marca_tiempo = Cd_timepo.strftime('%Y-%m-%d %H:%M:%S')

        US_HASH = generar_id_hash(ID_IDENTIFICACION,marca_tiempo,NOMBRE,'Lichain',FK_ID_ENTIDAD)

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuario (NOMBRE,APELLIDO,ID_IDENTIFICACION,CORREO,FK_ID_ENTIDAD,PAIS,PROVINCIA,CIUDAD,US_HASH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (NOMBRE, APELLIDO, ID_IDENTIFICACION, CORREO, FK_ID_ENTIDAD, PAIS, PROVINCIA, CIUDAD,US_HASH))
        mysql.connection.commit()
        minar_sesion(1)
        return redirect(url_for('index'))


@app.route("/sol_clave")
def sol_clave():
    if (request.method == "GET"):
        if 'NOMBRE' in session:
            if Rol() == 0:
                return render_template("home.html")
            else:
                return render_template("home_admin.html")
        else:
            return render_template("login_clave.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'NOMBRE' in session:
            if Rol() == 0:
                return render_template("home.html")
            else:
                return render_template("home_admin.html")
        else:
            return render_template("login_clave.html")
    else:

        CORREO = request.form['CORREO']
        US_CLAVE_DINA = request.form['US_CLAVE_DINA']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM usuario WHERE CORREO=%s", (CORREO,))
        user = cur.fetchone()
        cur.close()

        EMPRESA = info(int(user['FK_ID_ENTIDAD']), 1)
        LIC_ACTIVAS = info(int(user['FK_ID_ENTIDAD']), 0)
        estado_us = int(user['US_STATUS'])

        if (len(user) > 0):
            if (US_CLAVE_DINA == user['US_CLAVE_DINA']):
                session['NOMBRE'] = user['NOMBRE']
                session['CORREO'] = user['CORREO']
                session['EMPRESA'] = EMPRESA
                session['LIC_ACTIVAS'] = LIC_ACTIVAS
                session['STATUS'] = STATUS

                print("Ingresó!")
                if (int(user['ROL']) == 0):
                    return render_template("home.html")
                else:
                    return render_template("home_admin.html")
            else:
                error = "Clave incorrecta"
                return render_template("login_clave.html",error=error)
        else:
            flash('Usuario no econtrado')
            return redirect(url_for('index'))


@app.route('/login_clave', methods=["GET", "POST"])
def login_clave():
    if (request.method == "GET"):
        if 'NOMBRE' in session:
            if Rol() == 0:
                return render_template("home.html")
            else:
                return render_template("home_admin.html")
        else:
            return render_template("login_clave.html")
    else:
        CORREO = request.form['CORREO']

        #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cur.execute("SELECT * FROM usuario WHERE CORREO=%s", (CORREO,))
        #user = cur.fetchone()
        #cur.close()
        response_user= autorizacion_usuario(CORREO)
        print(response_user)

        if (response_user == 1):
            #claves_dinamicas(CORREO)
            ingreso = "Revisa tu bandeja de correo"
            return render_template("login.html",ingreso=ingreso)
            print("Se encuentra usuario , se envia correo")
        else:
            error = "Usuario no coincide"
            return render_template("login_clave.html", error=error)


@app.route('/logout')
def logout():
    if 'NOMBRE' in session:
        Clave_out(session['CORREO'])
        session.clear()
        return render_template("login_clave.html")
    else:
        return render_template("login_clave.html")


def Rol():
    CORREO = session['CORREO']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM usuario WHERE CORREO=%s", (CORREO,))
    user = cur.fetchone()
    cur.close()
    if int(user['ROL']) == 0:
        return 0
    else:
        return 1


def info(fk_entidad, opc):
    ID_ENTIDAD = fk_entidad
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM entidad WHERE ID_ENTIDAD=%s", (ID_ENTIDAD,))
    enti = cur.fetchone()
    cur.close()
    if opc == 1:
        return str(enti['N_ENTIDAD'])
    else:
        return int(enti['NUM_LICENCIAS'])

def info_act_lic(us_correo):
    CORREO = us_correo
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM usuario WHERE CORREO=%s", (CORREO,))
    data_us = cur.fetchone()
    cur.close()
    return data_us['ID_Usuario']






if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)
