from flask import Flask
from flaskext.mysql import MySQL  #Importar parte del módulo de mysql

class Conexion:
    #como la conexión está en otra ruta, se debe especificar en donde se encuentra el template
    app = Flask(__name__,template_folder='../templates') 
    #Conexión a la base de datos - Instancia
    mysql = MySQL()  #Instancia de MYSQL
    
    def iniciar(self):
        #le decimos que para conectarse a mysql será por medio de localhost
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'  #Host
        self.app.config['MYSQL_DATABASE_USER'] = 'root'  #Usuario
        self.app.config['MYSQL_DATABASE_PASSWORD'] = ''  #Contraseña
        self.app.config['MYSQL_DATABASE_DB'] = 'python'  #Nombre de Base de datos
        self.mysql.init_app(self.app)  #Inicializa la conexión
       
        print("Conectado a BD")

