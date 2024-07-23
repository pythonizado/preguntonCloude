from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import random
import string
import init_db

app = Flask(__name__)
app.secret_key = '1234'  # Necesario para usar sesiones

def get_db_connection():
    conn = sqlite3.connect('cuestionarioBD.db')
    conn.row_factory = sqlite3.Row
    return conn

def codigo_generar():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pregunta', methods=['GET', 'POST'])
def pregunta():
    if request.method == 'POST':
        guardar_respuesta()
        
    conn = get_db_connection()
    pregunta = conn.execute('SELECT * FROM Pregunta ORDER BY IDPREGUNTA ASC LIMIT 1 OFFSET ?', 
                            (session.get('pregunta_actual', 0),)).fetchone()
    conn.close()

    if pregunta:
        session['pregunta_actual'] = session.get('pregunta_actual', 0) + 1
        return render_template('pregunta.html', pregunta=pregunta)
    else:
        return render_template('pregunta.html', codigo=session.get('codigo_generado'))

def guardar_respuesta():
    respuesta = request.form['respuesta']
    id_pregunta = request.form['id_pregunta']
    codigo = session.get('codigo_generado')
    
    conn = get_db_connection()     
    conn.execute('INSERT INTO Respuesta (RESPUESTA, IDPREGUNTA, CODIGO_GENERADO) VALUES (?, ?, ?)',
                 (respuesta, id_pregunta, codigo))
    conn.commit()
    conn.close()

@app.route('/iniciar_cuestionario')
def iniciar_cuestionario():
    session['codigo_generado'] = codigo_generar()
    session['pregunta_actual'] = 0
    return redirect(url_for('pregunta'))

@app.route('/resultado')
def resultado():
    return render_template('resultado.html')

@app.route('/probabilidad', methods=['POST'])
def probabilidad():
    codigo1 = request.form['codigo1']
    codigo2 = request.form['codigo2']
    # Aquí iría la lógica del método comparar
    probabilidad = "Método comparar aún no implementado"
    return render_template('probabilidad.html', probabilidad=probabilidad)

if __name__ == '__main__':
    app.run(debug=True)