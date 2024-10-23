import psycopg2
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#formato: postgresql://<usuario>:<password>@<host>:<puerto>/<nombre_db>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/Contenidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("home.html")



@app.route("/contenido/<string:idCont>/", methods=['GET'])
def getContenidoById(idCont):
    contenido = Contenidos.query.get_or_404(idCont)
    return render_template("cont_view.html", contenido=contenido, idCont=idCont)


@app.route('/contenido', methods=['GET'])
def get_all_contenido():
    if request.method == 'GET':
        contenidos = Contenidos.query.all()  # Fetch all contents
    return render_template('index.html', contenidos=contenidos)

class Contenidos(db.Model):
    tablename = 'contenidos'
    idcontenido = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    sinopsis = db.Column(db.Text, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)

    def repr(self):
        return f'<Contenido {self.titulo}>'

# def conexion():
#     conn = psycopg2.connect(host='localhost',
#                             database='Contenidos',
#                             user='postgres',
#                             password='12345')
#     return conn

# @app.route("/")
# def index():
#     return render_template("home.html")

# @app.route("/contenido/<string:idCont>", methods=['GET', 'PUT', 'DELETE'])
# def getContenidoById(idCont):
#     if request.method == 'GET':
#         conn = conexion()
#         cur = conn.cursor()
#         consulta = "SELECT * FROM contenidos Where idContenido = %s"
#         cur.execute(consulta, [idCont])
#         contenido = cur.fetchone()
#         cur.close()
#         conn.close()
#         return render_template("cont_view.html", contenido=contenido, idCont=idCont)
#     if request.method == 'PUT':
#         print ("a")
#     if request.method == 'DELETE':
#         print("a")
#     else: 
#         print ("Method not allowed")

# @app.route('/contenido', methods=['GET', 'POST']) # /contenido
# def get_all_contenido():
#     if request.method == 'GET':
#         conn = conexion()
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM contenidos;')
#         conts = cur.fetchall()
#         cur.close()
#         conn.close()
#         return render_template('index.html', contenidos=conts)
#     if request.method == 'POST':
#         name = request.form['name']
#         tipo = request.form['tipo']
#         sinopsis = request.form['sinopsis']
#         duracion = request.form['duracion']
#         print(name, tipo, sinopsis, duracion)
#         conn = conexion()
#         try:
#             cur = conn.cursor()
#             consulta = "INSERT INTO contenidos (titulo, tipo, sinopsis, duracion) VALUES(%s, %s, %s, %s) RETURNING idContenido"
#             cur.execute(consulta, [name, tipo, sinopsis, duracion])
#             conn.commit()
#             cont_id = cur.fetchone()[0]
#             cur.close()
#             conn.close()
#         except psycopg2.DatabaseError as error:
#             print("Error. No se ha podido insertar el Servidor")
#             print(error)
#         return ("insertado el id: "+str(cont_id))
#     else: 
#         print ("Method not allowed")
        
            
if __name__ == "__main__":
    app.run(debug=True)