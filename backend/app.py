# Bibliotecas 
import os, datetime, sys, json
from flask import Flask, jsonify, request, render_template, redirect, session, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, delete
from flask_marshmallow import Marshmallow
from flask_session import Session
from flask_mqtt import Mqtt
from twilio.rest import Client

# Endereços de arquivos e pastas
backdir = os.path.dirname(__file__)   #Backend
rootdir = os.path.dirname(backdir)    #Diretório raiz
frontdir = os.path.join(rootdir, "frontend") #Frontend
staticdir = os.path.join(frontdir, 'styles') #Diretório de templates, imagens, scripts

##########################################################################################################
# APLICATIVO FLASK
app = Flask(__name__, template_folder=frontdir, static_folder=staticdir)
app.secret_key = b'\x05\xf1\xac\xde\x92\xba\xd2\xf6\x19\xd5\xf1\xd4'

# CONFIGURAÇÃO DE SESSÃO
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# CONFIGURAÇÃO DO BANCO DE DADOS SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(backdir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CONFIGURAÇÃO MQTT
# Tópico geral para receber dados da ESP
topic_up = '/microgreens/usp/mqtt/up' 
# Tópico geral para enviar dados para ESP
topic_down = '/microgreens/usp/mqtt/down' 
# Tópico específico para receber dados dos sensores da ESP
topic_data = '/microgreens/usp/mqtt/data' 

# Configuração do Broker
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'  
app.config['MQTT_BROKER_PORT'] = 1883 
app.config['MQTT_USERNAME'] = ''  
app.config['MQTT_PASSWORD'] = ''  
app.config['MQTT_KEEPALIVE'] = 5 
app.config['MQTT_TLS_ENABLED'] = False  

db = SQLAlchemy(app)
ma = Marshmallow(app)
mqtt = Mqtt(app)

##########################################################################################################
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
    name_esp = db.Column(db.String)
    cod_user = db.Column(db.Integer) 

    def __init__(self, cod_esp, name_esp, cod_user):
        self.cod_esp = cod_esp
        self.name_esp = name_esp
        self.cod_user = cod_user

# Tabela 4 (Dados de cada ESP)
class Dados_ESP32(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cod_esp = db.Column(db.Integer)
    hora_coleta = db.Column(db.DateTime, default=datetime.datetime.now)
    temperatura = db.Column(db.Integer)
    altura = db.Column(db.Integer)
    umidade = db.Column(db.Integer)                

    def __init__(self, cod_esp, temperatura, altura, umidade):
        self.cod_esp = cod_esp
        self.temperatura = temperatura
        self.altura = altura
        self.umidade = umidade

# Tabela 5 (Cultivo atual de cada ESP)
class CultivoESP32(db.Model):
    cod_esp = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.String)
    start_date = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    status_irrigar = db.Column(db.Boolean)
    status_iluminar = db.Column(db.Boolean)
    status_ventilar = db.Column(db.Boolean)
    status_soaking = db.Column(db.Boolean)
    status_plantar = db.Column(db.Boolean)
    status_colheita = db.Column(db.Boolean)
    min_days_harvest = db.Column(db.Integer)          

    def __init__(self, cod_esp, seed, min_days_harvest):
        self.cod_esp = cod_esp
        self.seed = seed
        self.status_irrigar = False
        self.status_iluminar = False
        self.status_ventilar = False
        self.status_soaking = False
        self.status_plantar = False
        self.status_colheita = False
        self.min_days_harvest = min_days_harvest

# Tabela 6 (Dados de tipos de semente)
class Datasheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seed_type = db.Column(db.String)
    soaking_time = db.Column(db.String)
    avg_temperature = db.Column(db.Integer)
    seed_quantity = db.Column(db.String)
    watering = db.Column(db.String)
    avg_harvest_height = db.Column(db.Float)
    min_days_harvest = db.Column(db.Integer)    
    max_days_harvest = db.Column(db.Integer)    

    def __init__(self, seed_type, soaking_time, avg_temperature, seed_quantity, watering, avg_harvest_height, min_days_harvest, max_days_harvest):
        self.seed_type = seed_type
        self.soaking_time = soaking_time
        self.avg_temperature = avg_temperature
        self.seed_quantity = seed_quantity
        self.watering = watering
        self.avg_harvest_height = avg_harvest_height
        self.min_days_harvest = min_days_harvest
        self.max_days_harvest = max_days_harvest

# SERIALIZAÇÃO DOS DADOS
class DatasheetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Datasheet
    
    seed_type = ma.auto_field()
    soaking_time = ma.auto_field()
    avg_temperature = ma.auto_field()
    seed_quantity = ma.auto_field()
    watering = ma.auto_field()
    avg_harvest_height = ma.auto_field()
    min_days_harvest = ma.auto_field()
    max_days_harvest = ma.auto_field()

datasheet_schema = DatasheetSchema()
datasheets_schema = DatasheetSchema(many=True)

##########################################################################################################
## ROTAS FLASK HTTP 
@app.route('/', methods = ['GET'])
def index():    
    if request.method == 'GET':        
        return render_template('index.html')

# Página de login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':    
        # Entradas no formulário  
        username = request.form.get("user")
        user = Users.query.filter_by(username=username).first()

        # Se usuário já adicionado na BD:
        if user:                
            # Se senha correta:
            if user.password == request.form.get("password"):
                # Variáveis de sessão utilizadas
                session["username"] = username
                session["firstname"] = user.first_name
                session["cod_user"] = user.cod_user                  
            
                return render_template('home.html')            
            else:
                error = "Senha incorreta!"
                return render_template('login.html', error=error)      
        else:
            error = "Usuário não encontrado!"
            return render_template('login.html', error=error)

# Página de cadastro
@app.route('/cadastro', methods=['GET','POST'])
def register_new_user():
    if request.method == 'GET':
        return render_template('cadastro.html')
    if request.method == 'POST':           
        # Entradas no formulário  
        first_name = request.form.get('firstname')        
        last_name = request.form.get('lastname')
        user_email = request.form.get('email')
        user_phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        validate_password = request.form.get('validate_password')
        
        # Notificações de erro
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
            # Adiciona novo usuário a BD
            new_user = Users(first_name, last_name, user_email, user_phone, username, password)

            db.session.add(new_user)
            db.session.commit()
        
            return redirect('/login')

# Rota auxiliar: adicionar uma nova ESP32 fabricada à base de dados de produtos à venda
@app.route('/add/esp/<int:cod_esp>', methods = ['GET'])
def add_new_esp32(cod_esp):      
    if not ESP32.query.filter_by(cod_esp=cod_esp).first():      
        new_esp32 = ESP32(cod_esp, status_esp=True)

        db.session.add(new_esp32)
        db.session.commit()

        return "ESP32 adicionada com sucesso!"
    else:
        return Response(status=204)

# Parear modelo de ESP32 adquirido pelo usuário
@app.route('/pair', methods = ['GET','POST'])
def pair_esp32_to_user():
    if request.method == 'GET':
        return render_template("pareamento.html")
    if request.method == 'POST':
        cod_esp = request.form.get('code_esp')        
        esp32 = ESP32.query.filter_by(cod_esp=cod_esp).first()
        
        if PairedESP32.query.filter_by(cod_esp=cod_esp).first():
            error = 'Código já cadastrado.'
            return render_template("pareamento.html", error=error)
        elif esp32 and esp32.status_esp:
            name_esp = request.form.get('name_esp')
            paired_esp = PairedESP32(esp32.cod_esp, name_esp, session["cod_user"])

            db.session.add(paired_esp)
            db.session.commit()          
            
            db.create_all() 
   
            error = 'Sistema pareado com sucesso!'
            return render_template("pareamento.html", error=error)        
        else:
            error = 'Código incorreto ou não existente!'
            return render_template("pareamento.html", error=error)

# Lista de microcontroladores do usuário (Painel de controle)
@app.route('/list', methods=['GET'])
def choose_micro():
    if request.method == 'GET':        
        micros = PairedESP32.query.filter_by(cod_user=session["cod_user"]).all()
        
        aux = []
        for micro in micros:
            info_cultivo = CultivoESP32.query.filter_by(cod_esp=micro.cod_esp).first()
            aux.append([micro, info_cultivo])
  
        return render_template('dashboardList.html', micros=aux)

# Painel de controle (Requisição HTTP para cada cód. ESP)
@app.route('/dashboard')
def dashboard():
    cod_esp = request.args.get('cod')
    if cod_esp:               
        info_cultivo = CultivoESP32.query.filter_by(cod_esp=cod_esp).first()
       
        # Adicionar novo cultivo 
        if info_cultivo == None:                        
            return render_template("dashboardAdd.html", datasheet=Datasheet.query.all(), cod_esp=cod_esp)
        # Se esperando tempo de embebição:
        elif not info_cultivo.status_soaking:
            return render_template("dashboardWaiting.html")
        # Painel de controle integral
        else:
            esp = PairedESP32.query.filter_by(cod_esp=cod_esp).first()
            esp_cultivo = CultivoESP32.query.filter_by(cod_esp=cod_esp).first()

            start_date = esp_cultivo.start_date.strftime("%d/%m/%Y %H:%M:%S")
             
            return render_template("dashboard.html", esp=esp, esp_cultivo=esp_cultivo, start_date=start_date)
            
    return Response(status=401)  

# Novo cultivo
@app.route('/start')
def start():
    values = request.args.get('cod').split('?')
    cod_esp = values[0]
    seed_id = values[1].split("=")[1]
    
    if cod_esp and seed_id:                     
        microgreen = Datasheet.query.filter_by(id=seed_id).first()
        esp_cultivo = CultivoESP32(cod_esp, microgreen.seed_type, microgreen.min_days_harvest)

        # INFORMAR A ESP QUE FOI DADO O START NO CULTIVO
        # CRONOMETRAR TEMPO DE EMBEBIÇÃO        
        tempo = ''.join(filter(str.isdigit, microgreen.soaking_time))

        if tempo != "":
            unidade = microgreen.soaking_time.split(tempo)[1]
            tempo = 3600*int(tempo) if unidade == " horas." else 60*int(tempo)            
        else:
            tempo = 0

        publish_message(str(cod_esp) + '/' + str(tempo))

        db.session.add(esp_cultivo)
        db.session.commit()

        return redirect('/list')
    return Response(status=401)

# Desconexão da conta
@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop('username')
        return redirect('/')

# HTTP auxiliar: adicionar dados a BD (datasheet de cultivos)
@app.route('/datasheet')
def fill_datasheet():
    if Datasheet.query.first() == None:
        soaking_time1 = "lave as sementes e, em seguida, as embeba em água por "
        soaking_time2 = "não embeba as sementes."
        watering = "manter sempre úmido."

        agriao = Datasheet("Agrião", soaking_time1+"1 minuto.",21,"4-6 colheres de sopa.", watering, 7.5, 2, 4)
        cevada = Datasheet("Cevada", soaking_time1+"10 horas.",21,"1½ - 2 xícaras.", watering, 12.5, 6, 9)
        aveia = Datasheet("Aveia", soaking_time1+"3 horas.",21,"1½  - 2 xícaras.", watering, 12.5, 6, 9)
        trigo = Datasheet("Trigo", soaking_time1+"3 horas.",23,"1½ - 2 xícaras.", watering, 12.5, 6, 9)
        linhaca = Datasheet("Linhaça", soaking_time2,21,"¼ - ½ de xícara.", watering, 5, 5, 6)
        girassol = Datasheet("Girassol", soaking_time1+"25 minutos.",23,"1 - 1½ xícaras.", watering, 8.5, 8, 12)
        beterraba = Datasheet("Beterraba", soaking_time1+"6 horas.",21,"2 colheres de sopa.", watering, 7.5, 11, 21)

        db.session.add(agriao)
        db.session.add(cevada)
        db.session.add(aveia)
        db.session.add(trigo)
        db.session.add(linhaca)
        db.session.add(girassol)
        db.session.add(beterraba)
        db.session.commit()

    return Response(status=204)

# Finalizar um cultivo 
@app.route('/encerrar/<int:cod_esp>', methods=['GET'])
def encerrar(cod_esp):    
    cultivo = CultivoESP32.query.filter_by(cod_esp=cod_esp).first()
    db.session.delete(cultivo)
    
    for esp in Dados_ESP32.query.filter_by(cod_esp=cod_esp).all():           
        db.session.delete(esp)
    
    db.session.commit()
    return Response(status=204)

# HTTP auxiliar (Requisição JS): checar fim do tempo de embebição para atualizar o status do painel de controle automaticamente
@app.route('/checkfinish/<int:cod_user>', methods=['GET'])
def check(cod_user): 
    res = []

    for esp in PairedESP32.query.filter_by(cod_user=cod_user).all():
        try:
            cultivo = CultivoESP32.query.filter_by(cod_esp=esp.cod_esp).first() 
            res.append(cultivo.status_soaking)
        except AttributeError:
            res.append(False)

    response = make_response(json.dumps(res))
    response.content_type = 'application/json'

    return response

# HTTP auxiliar (Requisição JS): reenviar dados de cultivo para o frontend
@app.route('/info/<int:id>', methods=['GET'])
def get_seed_info(id):  
    if request.method == 'GET':
        microverde = Datasheet.query.filter_by(id=id).first()        
        return datasheet_schema.jsonify(microverde)

# HTTP auxiliar (Requisição JS): reenvio de dados de sensores para o painel de controle
@app.route('/data/<int:cod_esp>', methods=["GET", "POST"])
def data(cod_esp):  
    dados_esp = Dados_ESP32.query.filter_by(cod_esp=cod_esp).order_by(desc(Dados_ESP32.hora_coleta)).limit(20).all()
    
    Temperatura, Umidade, Altura, time = [], [], [], []
 
    for dataset in dados_esp:
        Temperatura.append(dataset.temperatura)
        Umidade.append(dataset.umidade)
        Altura.append(dataset.altura)
        time.append(dataset.hora_coleta.strftime("%H:%M:%S"))

    data = [time, Temperatura, Altura, Umidade]    

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'

    return response

# HTTP auxiliar (Requisição JS): reenvio de horário atual para o painel de controle
@app.route('/time', methods=["GET", "POST"])
def time():    
    time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    response = make_response(json.dumps(time))
    response.content_type = 'application/json'

    return response

##########################################################################################################
## DIRETIVAS MQTT 
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:  
       print('\nMQTT: Conectado ao broker com sucesso.')    
       mqtt.subscribe(topic=topic_up, qos=1) 
       mqtt.subscribe(topic=topic_down, qos=1) 
       mqtt.subscribe(topic=topic_data, qos=1) 
       print('MQTT: Subscrito nos tópicos com sucesso.')    
   else:
       print('\nMQTT: Erro na conexão. Código:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )   
    # print("Recebido do tópico {topic} a mensagem {payload}".format(**data))

    [cod_esp, dados] = data["payload"].split("/")    

    # HANDLE: RECEBER DADOS DOS SENSORES
    if data["topic"] == topic_data:
        with app.app_context():                  
            dados = dados.split("&")

            new_data = Dados_ESP32(cod_esp, dados[0], dados[1], dados[2])
        
            db.session.add(new_data)
            db.session.commit()

    # HANDLE: RECEBER DADOS GERAIS
    elif data["topic"] == topic_up:
        # Quando a ESP é ligada:
        if dados == "esp-on":                   
            with app.app_context():        
                try:
                    esp_cultivo = CultivoESP32.query.filter_by(cod_esp=cod_esp).first()                  
                    esp_cultivo.status_irrigar = False
                    esp_cultivo.status_iluminar = False 
                    esp_cultivo.status_ventilar = False 
                    db.session.commit()
                except AttributeError:
                    pass 
        # Quando o tempo de embebição termina
        elif dados == "finish":
            with app.app_context(): 
                esp_cultivo = CultivoESP32.query.filter_by(cod_esp=cod_esp).first() 
                esp_cultivo.status_soaking = True                
                for dados in Dados_ESP32.query.filter_by(cod_esp=cod_esp).all():
                    db.session.delete(dados)
                db.session.commit()
        # Quando o tempo de colheita termina
        elif dados == "colheita":
            with app.app_context(): 
                esp_cultivo = CultivoESP32.query.filter_by(cod_esp=cod_esp).first() 
                esp_cultivo.status_colheita = True
                db.session.commit()

                # Notificação SMS
                esp = PairedESP32.query.filter_by(cod_esp=cod_esp).first()
                user = Users.query.filter_by(cod_user=esp.cod_user).first()
                
                account_sid = 'AC9ca8004589b7fb5d596b1a41742a7248'
                auth_token = 'b8c3774b822bc6e4293a0f07d5c653b7'
                client = Client(account_sid, auth_token)
                
                sms = "Esta mensagem está sendo enviada de um de seus Babygreens "
                sms += "por um motivo! Parabéns, " + str(user.first_name) + "! " 
                sms += str(esp.name_esp) + " informa que você já pode colher seus novos microverdes de " + str(esp_cultivo.seed) + "!" 
                sms += " Aproveite essa experiência 🌱"

                message = client.messages.create(
                                from_='+15734923846',
                                body =sms,
                                to =str(user.user_phone)
                            )
  
                print(message.sid)

@app.route('/publish/<path:msg>', methods=['GET','POST'])
def publish_message(msg):
  request_data = {'topic':topic_down, 'msg':msg}  
  publish_result = mqtt.publish(request_data['topic'], request_data['msg'], 1)
  print("MQTT: Publicação realizada. Código: " + str(publish_result[0]))

  # MODIFICAR STATUS DOS BOTÕES DE COMANDO
  dados = msg.split("/")

  esp_cultivo = CultivoESP32.query.filter_by(cod_esp=dados[0]).first()

  if dados[1] == "irrigar":
    esp_cultivo.status_irrigar = False if esp_cultivo.status_irrigar else True
  elif dados[1] == "iluminar":
    esp_cultivo.status_iluminar = False if esp_cultivo.status_iluminar else True
  elif dados[1] == "ventilar":
    esp_cultivo.status_ventilar = False if esp_cultivo.status_ventilar else True
  elif dados[1].isdigit() and int(dados[1]) < 60:
    esp_cultivo.status_plantar = True
  db.session.commit()
       
  return Response(status=204)
##########################################################################################################
   
if __name__ ==  '__main__':    
    app.run(debug=False, port=6001)