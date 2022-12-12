from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)

# Coneccion Mysql
mysql = MySQL(app)
app.config['MYSQL_DATRABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flaskclientes'
mysql.init_app(app)

# settings
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/carga')
def carga():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    datos_clientes = cursor.fetchall()
    return render_template('carga.html', clientes=datos_clientes)


@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tel = request.form['telefono']
        email = request.form['correo']
        dni = request.form['dni']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT dni FROM clientes')
        resultados = cursor.fetchone()
        if dni not in resultados:
            cursor.execute('INSERT INTO clientes (nombre, apellido, telefono, email, dni) VALUES (%s, %s, %s, %s, %s)',
                           (nombre, apellido, tel, email, dni))

            flash('Cliente agregado con éxito')
        else:
            flash('El DNI ya existe')
    conn.commit()
    return redirect(url_for('carga'))


@app.route('/editar/<id>')
def get_cliente(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = %s', (id))
    datos_clientes = cursor.fetchall()
    return render_template('editar.html', cliente=datos_clientes[0])


@app.route('/update/<id>', methods=['POST'])
def update_cliente(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tel = request.form['telefono']
        email = request.form['correo']
        dni = request.form['dni']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE `flaskclientes`.`clientes` SET `nombre`=%s, `apellido`=%s, `telefono`=%s, `email`=%s, `dni`=%s WHERE id=%s',
                   (nombre, apellido, tel, email, dni, id))
    conn.commit()
    flash('Cliente actualizado con éxito')
    return redirect(url_for('carga'))


@app.route('/eliminar/<string:id>')
def eliminar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = {0}'.format(id))
    conn.commit()
    flash('Cliente eliminado con éxito')
    return redirect(url_for('carga'))


if __name__ == '__main__':
    app.run(debug=True)
