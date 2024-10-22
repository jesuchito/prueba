import psycopg2
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

def conexion():
    conn = psycopg2.connect(host='localhost',
                            database='Contenidos',
                            user='postgres',
                            password='12345')
    return conn

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/contenido/<string:idCont>/", methods=['GET'])
def getContenidoById(idCont):
    conn = conexion()
    cur = conn.cursor()
    consulta = "SELECT * FROM contenidos Where idContenido = %s"
    cur.execute(consulta, [idCont])
    contenido = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("cont_view.html", contenido=contenido, idCont=idCont)

# @app.route("/contenido", methods=['POST'])
# def contenido_form():
#     name = request.form['name']
#     tipo = request.form['tipo']
#     sinopsis = request.form['sinopsis']
#     duracion = request.form['duracion']
#     print(name, tipo, sinopsis, duracion)
#     conn = conexion()
#     try:
#         cur = conn.cursor()
#         consulta = "INSERT INTO contenidos (titulo, tipo, sinopsis, duracion) VALUES(%s, %s, %s, %s) RETURNING idContenido"
#         cur.execute(consulta, [name, tipo, sinopsis, duracion])
#         conn.commit()
#         cur.close()
#         conn.close()
#     except psycopg2.DatabaseError as error:
#         print("Error. No se ha podido insertar el Servidor")
#         print(error)
#     return "insertado el id: "

@app.route('/contenido', methods=['GET', 'POST'])
def get_all_contenido():
    if request.method == 'GET':
        conn = conexion()
        cur = conn.cursor()
        cur.execute('SELECT * FROM contenidos;')
        conts = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', contenidos=conts)
    if request.method == 'POST':
        name = request.form['name']
        tipo = request.form['tipo']
        sinopsis = request.form['sinopsis']
        duracion = request.form['duracion']
        print(name, tipo, sinopsis, duracion)
        conn = conexion()
        try:
            cur = conn.cursor()
            consulta = "INSERT INTO contenidos (titulo, tipo, sinopsis, duracion) VALUES(%s, %s, %s, %s) RETURNING idContenido"
            cur.execute(consulta, [name, tipo, sinopsis, duracion])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.DatabaseError as error:
            print("Error. No se ha podido insertar el Servidor")
            print(error)
        return "insertado el id: "
    else: 
        print ("Method not allowed")
        
            
if __name__ == "__main__":
    app.run(debug=True)