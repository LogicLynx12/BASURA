from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'mysecretkey'

# Inicializamos SQLAlchemy
db = SQLAlchemy(app)

# Modelo de la base de datos para los usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250), nullable=True)
    pickup_days = db.Column(db.String(50), nullable=True)

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):  # Verificar la contraseña
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

# Ruta para el registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Hashear la contraseña
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Ruta para el panel de usuario después de iniciar sesión
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        address = request.form['address']
        pickup_days = ', '.join(request.form.getlist('pickup_days'))
        
        # Guardar los datos en la base de datos
        user = User.query.filter_by(username='user1').first()  # Esto es solo un ejemplo, deberías implementar la autenticación
        user.address = address
        user.pickup_days = pickup_days
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('dashboard.html')

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
