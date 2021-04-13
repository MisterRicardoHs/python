from flask import render_template, request, redirect  #Permite el renderizado de templates (vistas),recibir formularios y redireccionar
from flask import send_from_directory  #Permite el acceso a las carpetas de imagenes
from datetime import datetime  #Se incorpora el tiempo para las fotos fechas
import os
from src.Conexion import Conexion  #Se importa la clase Conexion

class Principal:
    #Instancia de la clase Conexion
    objeto = Conexion()
    objeto.iniciar()
    conn = objeto.mysql.connect()  #conecta a la BD
    cursor = conn.cursor()  #almacena la información
    
    #se crea una referencia a la carpeta uploads para poder eliminar o consultar imagen
    objeto.app.config['CARPETA']= os.path.join('../uploads')

    #Metodo para habilitar el acceso a las fotos
    @objeto.app.route('/uploads/<nombre_foto>')
    def uploads(nombre_foto, objeto=objeto):
        return send_from_directory(objeto.app.config['CARPETA'], nombre_foto)


    @objeto.app.route('/')  #app.route significa lo que el usuario digita en la url para ser mostrado el metodo posterior
    def index(cursor=cursor, conn=conn):
        cursor.execute("SELECT *FROM empleados")  #ejecuta la sentencia
        _empleados = cursor.fetchall()  #recupera la información
        conn.commit()  #da por terminado la ejecución
        return render_template('empleados/index.html', registros=_empleados) #se envía empleados con la variable 

    @objeto.app.route('/create')
    def create():
        return render_template('empleados/create.html')

    @objeto.app.route('/store', methods=['POST'])  #el solo hecho de escribir la palbra route, aparece las opciones
    def registrarEmpleado(cursor=cursor,conn=conn):
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
        cursor.execute(sql, datos)   #Se le asignan los argumentos de la tupla de datos
        conn.commit()

        return redirect('/')

    @objeto.app.route('/eliminar/<int:id>')
    def eliminarEmpleado(id, cursor=cursor,conn=conn):
        cursor.execute('SELECT foto FROM empleados WHERE id_empleado =  %s', (id))
        _foto = cursor.fetchall()
        os.remove(os.path.join("uploads/", _foto[0][0]))
        cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (id))
        conn.commit()
        return redirect("/")  #se incorpora redirect para redireccionar a la página anterior

    @objeto.app.route('/edit/<int:id>')
    def moduloActualizar(id, cursor=cursor, conn=conn):
        cursor.execute("SELECT *FROM empleados WHERE id_empleado = %s", (id))
        _empleado = cursor.fetchall()
        conn.commit()
        return render_template('empleados/edit.html', registro=_empleado)

    @objeto.app.route('/update', methods=["POST"])
    def actualizarEmpleado(cursor=cursor,conn=conn):
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
            os.remove(os.path.join("uploads/", _mismaFoto))
        else:
            _nuevoNombreFoto = _mismaFoto

        _datos = (_nombre,_correo,_nuevoNombreFoto,_id)

        cursor.execute("UPDATE empleados set nombre = %s, correo = %s, foto = %s WHERE id_empleado =  %s", _datos)
        conn.commit()
        return redirect('/')
    #Es una forma de ejecutar como modo de debug
    if __name__ == '__main__':
        objeto.app.run(debug=True)


