from flask import Flask
from flask import render_template, request, redirect  #Permite el renderizado de templates (vistas),recibir formularios y redireccionar
from flask import send_from_directory  #Permite el acceso a las carpetas de inmagenes
from flaskext.mysql import MySQL  #Importar parte del módulo de mysql
from datetime import datetime  #Se incorpora el tiempo para las fotos fechas
import os


app = Flask(__name__)
#Conexión a la base de datos le decimos que para conectarse a mysql será por medio de localhost
mysql = MySQL()  #Instancia de MYSQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  #Host
app.config['MYSQL_DATABASE_USER'] = 'root'  #Usuario
app.config['MYSQL_DATABASE_PASSWORD'] = ''  #Contraseña
app.config['MYSQL_DATABASE_DB'] = 'python'  #Nombre de Base de datos
mysql.init_app(app)  #Inicializa la conexión

#se crea una referencia a la carpeta uploadas para poder eliminar
CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA

#Metodo para habilitar el acceso a las fotos
@app.route('/uploads/<nombre_foto>')
def uploads(nombre_foto):
   return send_from_directory(app.config['CARPETA'], nombre_foto)


@app.route('/')  #app.route significa lo que el usuario digita en la url para ser mostrado el metodo posterior
def index():
    sql = "SELECT *FROM empleados"
    conn = mysql.connect()  #conecta a la BD
    cursor = conn.cursor()  #almacena la infromación
    cursor.execute(sql)  #ejecuta la sentencia
    _empleados = cursor.fetchall()  #recupera la información
    print(_empleados)
    conn.commit()  #da por terminado la ejecución

    return render_template('empleados/index.html', registros=_empleados) #se envía empleados con la variable regi 

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])  #el solo hecho de escribir la palbra route, aparece las opciones
def registrarEmpleado():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['foto']  #Para recepción de archivos se usa el método files

    _tiempoActual = datetime.now()
    _tiempo = _tiempoActual.strftime("%Y%H%M%S")  #AÑO/HORA/MINUTO/SEGUNDO

    if _foto.filename != '':  #Si la foto no está vacía
        _nuevoNombreFoto = _tiempo + _foto.filename  #se concatena la fecha al nombre del archivo
        _foto.save("uploads/"+_nuevoNombreFoto)  #se guarda en la carpeta uploads

    sql = "INSERT INTO `empleados` (`id_empleado`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre,_correo,_nuevoNombreFoto)
    conn = mysql.connect() 
    cursor = conn.cursor()
    cursor.execute(sql, datos)   #Se le asignan los argumentos de la tupla de datos
    conn.commit()

    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminarEmpleado(id):
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute('SELECT foto FROM empleados WHERE id_empleado =  %s', (id))
   _foto = cursor.fetchall()
   os.remove(os.path.join(app.config['CARPETA'], _foto[0][0]))
   cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (id))
   conn.commit()
   return redirect("/")  #se incorpora redirect para redireccionar a la página anterior

@app.route('/edit/<int:id>')
def moduloActualizar(id):
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("SELECT *FROM empleados WHERE id_empleado = %s", (id))
   _empleado = cursor.fetchall()
   print(_empleado)
   conn.commit()
   return render_template('empleados/edit.html', registro=_empleado)

@app.route('/update', methods=["POST"])
def actualizarEmpleado():
    _nombre = request.form['txtNombre'];
    _correo = request.form['txtCorreo']
    _foto = request.files['foto']
    _mismaFoto = request.form['antigua']
    _id = request.form['id']

    _tiempoActual = datetime.now()
    _tiempo = _tiempoActual.strftime("%Y%H%M%S")
   


    if _foto.filename != '':
         _nuevoNombreFoto = _tiempo + _foto.filename
         _foto.save("uploads/"+_nuevoNombreFoto)
         os.remove(os.path.join(app.config['CARPETA'], _mismaFoto))
    else:
        _nuevoNombreFoto = _mismaFoto

    _datos = (_nombre,_correo,_nuevoNombreFoto,_id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE empleados set nombre = %s, correo = %s, foto = %s WHERE id_empleado =  %s", _datos)
    conn.commit()
    return redirect('/')


#Es una forma de ejecutar como modo de debug
if __name__ == '__main__':
    app.run(debug=True)