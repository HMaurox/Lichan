import hashlib
import os
import sys
import bcrypt
import pdfkit
from funciones_Li import claves_dinamicas
from funciones_Li import Clave_out
from funciones_Li import cad_num
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


@app.route("/query", methods=['GET', 'POST'])
def query():
    if request.method == 'GET':
        if 'NOMBRE' in session:
            if Rol() == 0:
                return render_template("query.html")
            else:
                return render_template("query_admin.html")
        else:
            return render_template("login.html")
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

    if request.method == 'GET':
        ID_CLIENTE = info_act_lic(session['CORREO'])
        cur = mysql.connection.cursor()
        cur.execute("SELECT *  FROM licencia WHERE FK_ID_CLINETE=%s AND STATUS=0", (ID_CLIENTE,))
        data = cur.fetchall()

        if 'NOMBRE' in session:
            if Rol() == 0:
                return render_template("act_lic.html",licencia=data)
            else:
                return render_template("act_lic_admin.html",licencia=data)
        else:
            return render_template("login.html")

    if request.method == 'POST':

        return render_template("act_lic.html")




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

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO entidad (N_ENTIDAD,NIC,E_EMAIL,E_PAIS,E_PROVINCIA,E_CIUDAD,E_DIRECCION,NUM_LICENCIAS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (N_ENTIDAD, NIC, E_EMAIL, E_PAIS, E_PROVINCIA, E_CIUDAD, E_DIRECCION, NUM_LICENCIAS))
        mysql.connection.commit()
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

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuario (NOMBRE,APELLIDO,ID_IDENTIFICACION,CORREO,FK_ID_ENTIDAD,PAIS,PROVINCIA,CIUDAD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (NOMBRE, APELLIDO, ID_IDENTIFICACION, CORREO, FK_ID_ENTIDAD, PAIS, PROVINCIA, CIUDAD))
        mysql.connection.commit()
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

        ID_CLIENTE = info_act_lic(CORREO)
        cur = mysql.connection.cursor()
        cur.execute("SELECT count(*)  FROM licencia WHERE FK_ID_CLINETE=%s AND STATUS=1", (ID_CLIENTE,))
        lic_act = cur.fetchall()[0]
        cur.execute("SELECT count(*)  FROM licencia WHERE FK_ID_CLINETE=%s AND STATUS=0", (ID_CLIENTE,))
        lic_inact = cur.fetchall()[0]
        cur.close()

        session['LIC_ACT'] = cad_num(lic_act)
        session['LIC_INACT'] = cad_num(lic_inact)

        if (estado_us == 1):
            STATUS = "activo"
        else:
            STATUS = "ináctivo"

        if (len(user) > 0):
            if (US_CLAVE_DINA, user['US_CLAVE_DINA'] == user['US_CLAVE_DINA']):
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

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM usuario WHERE CORREO=%s", (CORREO,))
        user = cur.fetchone()
        cur.close()

        if (len(user) > 0):
            claves_dinamicas(CORREO)
            return render_template("login.html")
            print("Se encuentra usuario , se envia correo")
        else:
            return "Error password o user not match"


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
