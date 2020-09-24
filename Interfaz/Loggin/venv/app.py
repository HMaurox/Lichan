from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blockchain'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM entidad")
        data = cur.fetchall()
        cur.close()
        return render_template('register.html', entidad=data)
    else:
        NOMBRE              =  request.form['NOMBRE']
        APELLIDO            =  request.form['APELLIDO']
        CORREO              =  request.form['CORREO']
        HUELLA              =  request.form['HUELLA'].encode('utf-8')
        ID_IDENTIFICACION   =  request.form['ID_IDENTIFICACION']
        FK_ID_ENTIDAD       =  request.form['FK_ID_ENTIDAD']
        PAIS                =  request.form['PAIS']
        PROVICIA            =  request.form['PROVINCIA']
        CIUDAD              =  request.form['CIUDAD']

        HASH_HUELLA = bcrypt.hashpw(HUELLA, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (NOMBRE,APELLIDO, CORREO, HUELLA,ID_IDENTIFICACION,FK_ID_ENTIDAD,PAIS,PROVICIA,CIUDAD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(NOMBRE,APELLIDO,CORREO,HASH_HUELLA,ID_IDENTIFICACION,FK_ID_ENTIDAD,PAIS,PROVICIA,CIUDAD))
        mysql.connection.commit()
        session['NOMBRE'] = request.form['NOMBRE']
        session['CORREO'] = request.form['CORREO']
        return redirect(url_for('index'))



@app.route('/register_ent', methods=["GET", "POST"])
def register_ent():

    if request.method == 'GET':
        return render_template("register_ent.html")
    else:

        N_ENTIDAD           =  request.form['N_ENTIDAD']
        NIC                 =  request.form['NIC']
        E_EMAIL             =  request.form['E_EMAIL']
        E_PAIS              =  request.form['E_PAIS']
        E_PROVINCIA         =  request.form['E_PROVINCIA']
        E_CIUDAD            =  request.form['E_CIUDAD']
        E_DIRECCION         =  request.form['E_DIRECCION']
        F_INICIO            =  request.form['F_INICIO']
        NUM_LICENCIAS       =  request.form['NUM_LICENCIAS']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO entidad (N_ENTIDAD,NIC,E_EMAIL,E_PAIS,E_PROVINCIA,E_CIUDAD,E_DIRECCION,F_INICIO,NUM_LICENCIAS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(N_ENTIDAD,NIC,E_EMAIL,E_PAIS,E_PROVINCIA,E_CIUDAD,E_DIRECCION,F_INICIO,NUM_LICENCIAS))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/login',methods=["GET","POST"])
def login():
    if (request.method == "POST"):

        CORREO = request.form['CORREO']
        HUELLA = request.form['HUELLA'].encode('utf-8')
        HUELLA2 = request.form['HUELLA']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM usuario WHERE CORREO=%s",(CORREO,))
        user = cur.fetchone()
        cur.close()

        if user is None:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM us_adm WHERE CORREO=%s", (CORREO,))
            adm = cur.fetchone()
            cur.close()
            if adm is None:
                return "Error de todo"

            if (len(adm) > 0):
                if (HUELLA2, adm['HUELLA'] == adm['HUELLA']):
                    session['NOMBRE'] = adm['NOMBRE']
                    session['CORREO'] = adm['CORREO']

                    return render_template("home.html")
                else:
                    return "Error password o user not match"
            else:
                return "Error password o user not match"

        if (len(user) > 0):
            if (bcrypt.hashpw(HUELLA, user['HUELLA'].encode('utf-8')) == user['HUELLA'].encode('utf-8')):
                session['NOMBRE'] = user['NOMBRE']
                session['CORREO'] = user['CORREO']
                return render_template("home.html")
            else:
                return "Error de contraseña"
        else:
                return "Error password o user not match"
    else:
        return render_template("login.html")


@app.route('/login_adm',methods=["GET","POST"])
def login_adm():
    if (request.method == "POST"):
        CORREO = request.form['CORREO']
        HUELLA = request.form['HUELLA']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM us_adm WHERE CORREO=%s",(CORREO,))
        user = cur.fetchone()
        cur.close()
        if user is None:
            return "Error de todo"

        if (len(user) > 0):
            if (HUELLA, user['HUELLA'] == user['HUELLA']):
                session['NOMBRE'] = user['NOMBRE']
                session['CORREO'] = user['CORREO']

                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM usuario")
                data = cur.fetchall()
                cur.close()
                return render_template('admin_page.html', usuario=data)
            else:
                return "Error password o user not match"
        else:
            return "Error password o user not match"
    else:
        return render_template("login.html")

@app.route("/update",methods=['POST'])
def update():
    USUARIO = request.form['USUARIO']
    NOMBRE = request.form['NOMBRE']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuario SET data=%s WHERE id=%s", (NOMBRE,ID_Usuario))
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")



if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)

