import os, datetime
from flask import Flask, jsonify, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_session import Session

backdir = os.path.dirname(__file__)
rootdir = os.path.dirname(backdir)
frontdir = os.path.join(rootdir, os.listdir(rootdir)[0])
staticdir = os.path.join(frontdir, 'styles')

app = Flask(__name__, template_folder=frontdir, static_folder=staticdir)
app.secret_key = b'\x05\xf1\xac\xde\x92\xba\xd2\xf6\x19\xd5\xf1\xd4'

# CONFIGURAÇÃO DE SESSÃO
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# CONFIGURAÇÃO DO BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(backdir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Tabela 1 (Usuários)
class Users(db.Model):
    cod_user = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_phone = db.Column(db.String(13), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, first_name, last_name, user_email, user_phone, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_email = user_email
        self.user_phone = user_phone
        self.username = username
        self.password = password

# Tabela 2 (Microcontroladores)
class ESP32(db.Model):
    cod_esp = db.Column(db.Integer, primary_key=True)
    status_esp = db.Column(db.Boolean)
    production_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, cod_esp, status_esp):
        self.cod_esp = cod_esp
        self.status_esp = status_esp
  
# Tabela 3 (Usuários e produtos adquiridos)
class PairedESP32(db.Model):
    cod_esp = db.Column(db.Integer, primary_key=True)
    cod_user = db.Column(db.Integer)

    def __init__(self, cod_esp, cod_user):
        self.cod_esp = cod_esp
        self.cod_user = cod_user

# Para criar a base de dados, ir no terminal e fazer:
# export FLASK_APP=app
# flask shell
# from app import db
# db.create_all()
# exit()    

# Se quiser deletar tudo: db.drop_all()

# SERIALIZAÇÃO DOS DADOS
""" ma = Marshmallow(app)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users

    cod_user = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ESP32Schema(ma.SQLAlchemySchema):
    class Meta:
        model = ESP32

    cod_esp = ma.auto_field()
    status_esp  = ma.auto_field()
    production_date = ma.auto_field()

ESP32_schema = ESP32Schema()
ESP32s_schema = ESP32Schema(many=True) """

@app.route('/', methods = ['GET'])
def index():    
    if request.method == 'GET':        
        return render_template('index.html')

# Página de cadastro
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':      

        username = request.form.get("user")
        user = Users.query.filter_by(username=username).first()

        if user:                
            if user.password == request.form.get("password"):
                session["name"] = username
                return render_template('dashboard.html', )
            else:
                error = "Senha incorreta."
                return render_template('login.html', error=error)
        else:
            error = "Usuário não encontrado."
            return render_template('login.html', error=error)

@app.route('/cadastro', methods=['GET','POST'])
def register_new_user():
    if request.method == 'GET':
        return render_template('cadastro.html')
    if request.method == 'POST':           
        first_name = request.form.get('firstname')        
        last_name = request.form.get('lastname')
        user_email = request.form.get('email')
        user_phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        validate_password = request.form.get('validate_password')
        
        if Users.query.filter_by(user_email=user_email).first():            
            error = "Email já cadastrado."
            return render_template('cadastro.html', error=error)
        elif Users.query.filter_by(user_phone=user_phone).first():
            error = "Telefone já cadastrado."
            return render_template('cadastro.html', error=error)
        elif Users.query.filter_by(username=username).first():
            error = "usuário já cadastrado."
            return render_template('cadastro.html', error=error)
        elif validate_password != password:
            error = "Senhas distintas foram digitadas."
            return render_template('cadastro.html', error=error)
        else:        
            new_user = Users(first_name, last_name, user_email, user_phone, username, password)

            db.session.add(new_user)
            db.session.commit()
        
            return redirect('/login')
# Adicionar uma nova ESP32 fabricada à base de dados de produtos à venda
@app.route('/add/esp', methods = ['POST'])
def add_new_esp32():  
    cod_esp = request.json['cod_esp']
    status_esp = request.json['status_esp']
    
    if ESP32.query.filter_by(cod_esp=cod_esp).first():
        return jsonify({"Erro": "Código de ESP32 já cadastrado na base de dados."})
    else:
        new_esp32 = ESP32(cod_esp, status_esp)

        db.session.add(new_esp32)
        db.session.commit()
    
        return ESP32_schema.jsonify(new_esp32)

# Parear modelo de ESP32 adquirido pelo usuário
@app.route('/user?=<cod_user>/pair', methods = ['POST'])
# Considera a sessão do usuário (Talvez tenha que mudar quando for ver essa parte)
def pair_esp32_to_user(cod_user):
    cod_esp = request.json['cod_esp']
  
    esp32 = ESP32.query.filter_by(cod_esp=cod_esp).first()

    if esp32 and esp32.status_esp:

        user = ESP32.query.filter_by(cod_user=cod_user).first()
        
        pair_esp32 = PairedESP32(esp32.cod_esp, cod_user)





        return jsonify({"Sucesso":"ESP32 pareada"})
    else:
        return jsonify({"Erro":"ESP32 não cadastrada ou desativada"})

    

    

if __name__ ==  '__main__':
    app.run(debug=True)