from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2

app = Flask(__name)
app.secret_key = 'tu_clave_secreta'

# Configura la conexión a la base de datos
conn = psycopg2.connect(
    dbname="proyectodb",  # Nombre de tu base de datos
    user="postgres",      # Tu nombre de usuario de PostgreSQL
    password="_password123",  # Tu contraseña de PostgreSQL
    host="10.0.0.4",      # Dirección IP de tu servidor de base de datos
    port="5432"           # Puerto predeterminado de PostgreSQL
)
cursor = conn.cursor()

# Rutas
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    if user:
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return "¡Inicio de sesión exitoso!"
    else:
        return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form['username']
    password = request.form['password']
    
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    
    flash('Cuenta creada exitosamente. Por favor inicia sesión.')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
