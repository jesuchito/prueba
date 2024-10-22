import psycopg2
from flask import Flask, render_template, jsonify, request

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

@app.route("/contenido",methods=['POST'])
@app.route("/contenido/<int:cont_id>/", methods=['PUT'])
def contenido_form(cont_id=None):
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
        cont_id = cur.fetchone()[0]
        cur.close()
        conn.close()
    except psycopg2.DatabaseError as error:
        print("Error. No se ha podido insertar el Servidor")
        print(error)
    return "ndkcsdkvn"

@app.route('/contenido', methods=['GET'])
def get_all_contenido():
    conn = conexion()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contenidos;')
    conts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', contenidos=conts)

if __name__ == "__main__":
    app.run(debug=True)