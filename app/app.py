from flask import Flask, render_template, request, jsonify, redirect, session, url_for, make_response
from redis import Redis
from datetime import datetime, timedelta
#from mysql.connector import *
from pymysql import *
from flask_cors import CORS
from flask_session import Session
import bcrypt
import logging
import pymysql
import uuid
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from dbutils.pooled_db import PooledDB


######## Acessos da base #########
config = {
    "host": "localhost",
    "user": "root",
    "password": "27769304Jm@",
    "database": "sissal",
}

connection = connect(**config)
cursor = connection.cursor()

db_lock = Lock()

def get_connection():
    connection = pymysql.connect(**config)
    return connection

###############################################

######### Funções Auxiliares ##################

def get_connection():
    connection = pymysql.connect(**config)
    return connection

def calcular_semana(data):
    # Calcular a data da segunda-feira desta semana
    dias_desde_segunda_feira = data.weekday()
    print(dias_desde_segunda_feira)  # 0 para segunda-feira, 1 para terça-feira, etc.
    segunda_feira = data - timedelta(days=dias_desde_segunda_feira)

    # Calcular a data da sexta-feira desta semana
    dias_ate_sexta_feira = 4 - dias_desde_segunda_feira  # Sexta-feira é o quinto dia da semana
    sexta_feira = data + timedelta(days=dias_ate_sexta_feira)

    return segunda_feira, sexta_feira

# Obter a data de hoje
data_de_hoje = datetime.today().date()

# Calcular a semana
segunda_feira, sexta_feira = calcular_semana(data_de_hoje)

# Imprimir os resultados
print(f"A data da segunda-feira desta semana é: {segunda_feira.strftime('%Y-%m-%d')}")
print(f"A data da sexta-feira desta semana é: {sexta_feira.strftime('%Y-%m-%d')}")

def timedelta_to_string(td):
    # Converter o timedelta para um objeto datetime
    dt = datetime(1, 1, 1) + td
    # Formatar o objeto datetime como uma string no formato HH:MM:SS
    return dt.strftime('%H:%M:%S')

def cria_senha(senha,name):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    hashed = hashed.decode('utf-8')

    cursor.execute(f"INSERT INTO sissal.users (userName, userPassword) VALUES ('{name}','{hashed}') ON DUPLICATE KEY UPDATE userPassword = '{hashed}'")
    connection.commit()
    return True

def reset_senha(senha,name):
    cursor.execute(f"SELECT userId from sissal.users where userName = '{name}'")
    result = cursor.fetchall()
    ID, = result[0]

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    hashed = hashed.decode('utf-8')

    cursor.execute(f"UPDATE sissal.users SET userPassword = '{hashed}' WHERE userId = '{ID}'")
    connection.commit()
    return True

def verificar_senha(senha_inserida, name):
    cursor.execute(f"SELECT userId from sissal.users where UserName = '{name}'")
    result = cursor.fetchall()
    ID, = result[0]

    cursor.execute(f"SELECT userPassword FROM sissal.users WHERE userId = '{ID}'")
    result = cursor.fetchall()
    hashed, = result[0]
    if bcrypt.checkpw(senha_inserida.encode('utf-8'), hashed.encode('utf-8')): #aqui o hashed vai ser a partir de uma consulta na base e puxando o valor que tá na tabela pra comparar
        return True
    else:
        return False

######################################################

############## Api ############################

##app = Flask(__name__)
####CORS(app, origins='http://localhost:PORTA_DO_SEU_FRONTEND', supports_credentials=True)
##CORS(app, origins='*', supports_credentials=True, methods=['POST','GET'], allow_headers=['Content-Type'])
##Session(app)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "123456"
sess = Session()
sess.init_app(app)
sess._get_interface
CORS(app)

executor = ThreadPoolExecutor()
leituraCard = None

@app.route('/leitura_card', methods=['POST', 'OPTIONS'])
def leitura_card():
    global leituraCard
    leituraCard = True
    print(leituraCard)
    return jsonify(200)

@app.route('/Verifica_senha', methods=['POST', 'OPTIONS'])
def verifica_senha():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    name = data.get('username')
    senha_inserida = data.get('senha')

    cursor.execute(f"SELECT userId from sissal.users where UserName = '{name}'")
    result = cursor.fetchall()
    ID, = result[0]

    cursor.execute(f"SELECT userPassword FROM sissal.users WHERE userId = '{ID}'")
    result = cursor.fetchall()
    hashed, = result[0]
    if bcrypt.checkpw(senha_inserida.encode('utf-8'), hashed.encode('utf-8')): #aqui o hashed vai ser a partir de uma consulta na base e puxando o valor que tá na tabela pra comparar
        resposta = {'mensagem': 'True'}
        return jsonify(resposta)
    else:
        resposta = {'mensagem': 'False'}
        return jsonify(resposta)

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    name = data.get('username')
    password = data.get('password')
    print("ESTOU AQUI", name, password)

    def process_login(name, password):
        with db_lock:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT userName from sissal.users where userName = %s", (name,))
            result = cursor.fetchone()
            print("RESULTADO:",result)
        if result == None:
            resposta = {'Login Inexistente'}
            return resposta
        else:
            if verificar_senha(password, name):
                resposta = "Sucesso"
                return resposta
                # Configurar a sessão do usuário
                # session['user'] = nome  # Novo: Armazena o nome do usuário na sessão
                # session['session_id'] = str(uuid.uuid4())  # Novo: Adiciona um identificador de sessão único
                # session['logged_in'] = True  # Novo: Marca que o usuário está logado
                # session.modified = True
                # resp = make_response(jsonify(resposta))
                # print(resp)
                # resp.set_cookie('session_id', "oi", max_age=10)  # Define o cookie com o ID do usuário
                # return resp
            else:
                resposta = {'Login Failed'}
                return resposta

    future = executor.submit(process_login, name, password)
    resp = future.result()
    print(resp)
    if resp == 'Sucesso':
        print("mandei sucesso")
        return jsonify({'mensagem': 'Login bem-sucedido!'})
    else: 
        return jsonify({'mensagem': 'Login Falhou!'})
   

@app.route('/Cadastro', methods=['POST', 'OPTIONS'])
def Cadastro():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    name = data.get('idcadastroUser')
    password = data.get('idcadastroPass')
    print("ESTOU AQUI", name, password)

    try:
        cursor.execute(f"SELECT userName from sissal.users where userName = '{name}'")
        result = cursor.fetchall()
        print("CHEGUEI AQUI: ",result)
        if not result:
            print("Usuário não existe no sistema")
            cria_senha(password,name)
            resposta = {'mensagem': 'Cadastro bem-sucedido!'}
            return jsonify(resposta)
        else:
            print("Usuário já existe no sistema")
            resposta = {'mensagem': 'Login Falhou!'}
            return jsonify(resposta)
    except Exception as e:
        print("Não foi possível localizar o usuário. Erro: {e}", e)
        resposta = {'mensagem': 'Login Falhou!'}
        return jsonify(resposta)


@app.route('/exclusaoCadastro', methods=['POST', 'OPTIONS'])
def exclusaoCadastro():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    name = data.get('idexclusaoUser')
    print("ESTOU AQUI", name)

    try:
        cursor.execute(f"SELECT userId from sissal.users where userName = '{name}'")
        result = cursor.fetchall()
        print("Id do user: ",result)
        if not result:
            print("Usuário não existe no sistema")
            resposta = {'mensagem': 'User não existe!'}
            return jsonify(resposta)
        else:
            print("Usuário encontrado")
            ID, = result[0]
            cursor.execute(f"DELETE FROM sissal.users WHERE userId = '{ID}'")
            connection.commit()
            resposta = {'mensagem': 'Cadastro excluído com sucesso!'}
            return jsonify(resposta)
    except Exception as e:
        print("Não foi possível localizar o usuário. Erro: {e}", e)
        resposta = {'mensagem': 'Login Falhou!'}
        return jsonify(resposta)
    

@app.route('/resetCadastro', methods=['POST', 'OPTIONS'])
def resetCadastro():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    name = data.get('idresetUser')
    password = data.get('idresetPass')
    print("ESTOU AQUI", name)

    try:
        cursor.execute(f"SELECT userId from sissal.users where userName = '{name}'")
        result = cursor.fetchall()
        print("Id do user: ",result)
        if not result:
            print("Usuário não existe no sistema")
            resposta = {'mensagem': 'User não existe!'}
            return jsonify(resposta)
        else:
            print("Usuário encontrado")
            reset_senha(password,name)
            resposta = {'mensagem': 'Troca de senha bem-sucedida!'}
            return jsonify(resposta)
    except Exception as e:
        print("Não foi possível localizar o usuário. Erro: {e}", e)
        resposta = {'mensagem': 'Login Falhou!'}
        return jsonify(resposta)


@app.route('/get_reservas', methods=['GET'])
def get_reservas():

    teste = request.cookies.get('oi')
    print(teste)
    def process_reservas():
        with db_lock:
            connection = get_connection()
            cursor = connection.cursor()
            data_hoje = str(datetime.today().date())
            cursor.execute(f"SELECT * from sissal.bookingrooms where sissal.bookingrooms.bookingDate = '{data_hoje}' order by sissal.bookingrooms.startHour")
            result = cursor.fetchall()
        if not result:
            resposta = {'msg': 'Error'}
            return jsonify(resposta)
        else:
            dados_reservas = []

            for row in result:
                reserva = {
                    "numero_sala": row[3],  # Substitua com o nome correto da coluna
                    "reserva": row[5],          # Substitua com o nome correto da coluna
                    "horaInicio": timedelta_to_string(row[6]),
                    "horaFinal": timedelta_to_string(row[7])                  # Substitua com o nome correto da coluna
                }
                dados_reservas.append(reserva)

            print(dados_reservas)
            return dados_reservas

    future = executor.submit(process_reservas)
    lista = future.result()
    return jsonify(lista)


@app.route('/get_reserva_user', methods=['POST', 'OPTIONS'])
def get_reserva_user():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    data = request.json  # Recebe os dados do frontend
    user = data.get('username')
    print(user)

    def get_reserva_user_func():
        with app.app_context():
            with db_lock:
                try:
                    connection = get_connection()
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * from sissal.bookingrooms where userName = '{user}'")
                    result = cursor.fetchall()
                    print("hello", result)
                    if not result:
                        resposta = {'mensagem': 'Error'}
                        print(resposta)
                        return jsonify(resposta)
                    else:
                        dados_reserva_user = []

                        for row in result:
                            reserva = {
                                "numero_sala": row[3],  # Substitua com o nome correto da coluna
                                "data": row[8].strftime('%Y-%m-%d'),     # Substitua com o nome correto da coluna
                                "horaInicio": timedelta_to_string(row[6]),
                                "horaFinal": timedelta_to_string(row[7])       # Substitua com o nome correto da coluna
                            }
                            dados_reserva_user.append(reserva)
                        print(dados_reserva_user)
                        return dados_reserva_user

                except Exception as e:
                    print("Não foi possível localizar o usuário. Erro:", e)
                    resposta = {'mensagem': 'Error 2'}
                    return jsonify(resposta)
    
    future = executor.submit(get_reserva_user_func)
    retorno = future.result()
    return jsonify(retorno)
    
@app.route('/get_reserva_user_week', methods=['POST', 'OPTIONS'])
def get_reserva_user_week():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    data = request.json  # Recebe os dados do frontend
    user = data.get('username')
    print(user)
    data_de_hoje = datetime.today().date()
    segunda_feira, sexta_feira = calcular_semana(data_de_hoje)
    segunda = segunda_feira.strftime('%Y-%m-%d')
    print("oi oi ", segunda)
    sexta = sexta_feira.strftime('%Y-%m-%d')
    
    def get_reserva_user_week_func():
        with app.app_context():
            with db_lock:
                try:
                    connection = get_connection()
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * from sissal.bookingrooms where userName = '{user}' AND bookingrooms.bookingDate <= '{sexta}' AND bookingrooms.bookingDate >= '{segunda}'")
                    result = cursor.fetchall()
                    print("hello", result)
                    if not result:
                        resposta = {'mensagem': 'Error ou não há reservas'}
                        print(resposta)
                        return resposta
                    else:
                        dados_reserva_user = []

                        for row in result:
                            print(row[8].weekday())
                            reserva = {
                                "numero_sala": row[3],  # Substitua com o nome correto da coluna
                                "dia": row[8].weekday(),   # Substitua com o nome correto da coluna
                                "horaInicio": timedelta_to_string(row[6])      # Substitua com o nome correto da coluna
                            }
                            dados_reserva_user.append(reserva)

                        print(dados_reserva_user)

                        return dados_reserva_user
                except Exception as e:
                    print("Não foi possível localizar o usuário. Erro: {e}", e)
                    resposta = {'mensagem': 'Error 2'}
                    return resposta

    future = executor.submit(get_reserva_user_week_func)
    resposta = future.result()
    return jsonify(resposta)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/PagInicial")
def paginicial():
    return render_template('PagInicial.html')

@app.route("/Hist")
def hist():
    return render_template('Hist.html')

@app.route("/Salas")
def salas():
    return render_template('Salas.html')

@app.route("/Schedule")
def schedule():
    return render_template('Schedule.html')

@app.route("/Admin")
def admin():
    username = request.args.get('username')
    print(username)

    def verifica_admin():
        with app.app_context():
            with db_lock:
                try:
                    cursor.execute(f"SELECT userId from sissal.users where userName = '{username}'")
                    result = cursor.fetchall()
                    ID, = result[0]

                    cursor.execute(f"SELECT userRole FROM sissal.users WHERE userId = '{ID}'")
                    result = cursor.fetchall()
                    result, = result[0]
                    return result

                except Exception as e:
                    print("Não foi possível localizar o usuário. Erro: {e}")
                    resposta = {'Error'}
                    return resposta
                
    future = executor.submit(verifica_admin)
    resposta = future.result()
    if resposta == 'Admin':
        return render_template('Admin.html')
    else:
        return render_template('PagInicial.html') 

@app.route('/get_salas', methods=['POST','OPTIONS'])
def get_salas():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    andarSala = data.get('andarSala')
    hourConsulta = data.get('hourConsulta')
    dataConsulta = data.get('dataConsulta')
    print("sou data:", dataConsulta)
    print("sou hora:", hourConsulta)

    def get_salas_func():
        with app.app_context():
            with db_lock:
                try:
                    cursor.execute(f"SELECT rooms.roomId, rooms.roomFloor, rooms.roomNumber, rooms.roomCapacity, rooms.roomCooling FROM sissal.rooms as rooms WHERE rooms.roomFloor = '{andarSala}'")
                    result = cursor.fetchall()
                    print(dataConsulta)
                    cursor.execute(f"SELECT rooms.roomNumber, bookingrooms.startHour, bookingrooms.endHour, bookingrooms.bookingDate FROM sissal.rooms as rooms JOIN sissal.bookingrooms as bookingrooms ON rooms.roomNumber = bookingrooms.roomNumber WHERE bookingrooms.bookingDate = '{dataConsulta}' AND bookingrooms.startHour <= '{hourConsulta}' AND bookingrooms.endHour > '{hourConsulta}'")
                    result2 = cursor.fetchall()
                    print("resulta2:",result2)
                    if not result:
                        resposta = {'msg': 'Error'}
                        return jsonify(resposta)
                    else:
                        salas = []
                        reservas = []
            
                        for row in result:
                            salas_info = {
                                "numeroSala": row[2],
                                "capacidadeSala": row[3], 
                                "refrigeracaoSala": row[4],
                                "reservado": 'Nao'
                            }
                            salas.append(salas_info)
                        
                        for row in result2:
                            reservas_salas = {
                                "numeroSala": row[0],
                                "reservado": 'Sim'
                            }
                            reservas.append(reservas_salas)
                        
                        sala_dict = {sala["numeroSala"]: sala for sala in salas}
            
                        # Atualizando os valores de reservado conforme a lista de reservas
                        for reserva in reservas:
                            numero_sala = reserva["numeroSala"]
                            if numero_sala in sala_dict:
                                sala_dict[numero_sala]["reservado"] = reserva["reservado"]
            
                        # Convertendo o dicionário de volta para uma lista
                        salas_total = list(sala_dict.values())
                        
                        print(salas_total)
                        print(reservas)
            
                        return salas_total
                except Exception as e:
                    print("Não foi possível localizar as salas. Erro: {e}", e)
                    resposta = {e}
                    return resposta
    
    future = executor.submit(get_salas_func)
    resposta = future.result()
    return jsonify(resposta)
    

@app.route('/get_salas_inicial', methods=['POST','OPTIONS'])
def get_salas_inicial():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    andarSala = data.get('andarSala') 

    def get_salas_inicial_func():
        with app.app_context():
            with db_lock:
                try:
                    cursor.execute(f"SELECT rooms.roomFloor, rooms.roomNumber from sissal.rooms as rooms WHERE rooms.roomFloor = '{andarSala}'")
                    result = cursor.fetchall()
                    if not result:
                        resposta = {'msg': 'Error'}
                        return jsonify(resposta)
                    else:
                        salas = []

                        for row in result:
                            salas_nmb = {
                                "numeroSala": row[1]
                            }
                            salas.append(salas_nmb)

                        print(salas)

                        return salas
                except Exception as e:
                    print("Não foi possível localizar as salas. Erro: {e}")
                    resposta = {e}
                    return resposta
    future = executor.submit(get_salas_inicial_func)
    resposta = future.result()
    return jsonify(resposta)

@app.route('/get_sala_info', methods=['POST','OPTIONS'])
def get_sala_info():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    logging.info(f"Valor A")
    data = request.json  # Recebe os dados do frontend
    Sala = data.get('Sala') 

    def get_sala_info_func():
        with app.app_context():
            with db_lock:
                try:
                    cursor.execute(f"SELECT rooms.roomCapacity, rooms.roomCooling, rooms.roomNumber from sissal.rooms as rooms WHERE rooms.roomNumber = '{Sala}'")
                    result = cursor.fetchall()
                    if not result:
                        resposta = {'msg': 'Error'}
                        return jsonify(resposta)
                    else:
                        sala = []

                        for row in result:
                            sala_info = {
                                "numeroSala": row[2],
                                "capacidadeSala": row[0],
                                "refrigeracaoSala": row[1]
                            }
                            sala.append(sala_info)

                        print(sala)

                        return sala
                except Exception as e:
                    print("Não foi possível localizar as salas. Erro: {e}")
                    resposta = {e}
                    return resposta
    future = executor.submit(get_sala_info_func)
    resposta = future.result()
    return jsonify(resposta)

@app.route('/reserva_Sala', methods=['POST', 'OPTIONS'])
def reserva_Sala():

    if request.method == 'OPTIONS':
        # Responda às requisições OPTIONS
        headers = {
            'Access-Control-Allow-Origin': '*',  # Substitua pelo seu domínio ou '*' para permitir de qualquer lugar
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    data = request.json  # Recebe os dados do frontend
    dataConsulta = data.get('dataConsulta') 
    horaConsulta = data.get('horaConsulta')
    sala = data.get('sala')
    username = data.get('username')

    def reserva_Sala_func():
        with app.app_context():
            with db_lock:
                try:
                    cursor.execute(f"SELECT * from sissal.bookingrooms as bookingrooms where bookingrooms.startHour = '{horaConsulta}' AND bookingrooms.bookingDate = '{dataConsulta}' AND bookingrooms.roomNumber = {sala}")
                    result = cursor.fetchall()
                    cursor.execute(f"SELECT userId, userCard from sissal.users where UserName = '{username}'")
                    result2 = cursor.fetchall()
                    result2 = result2[0]
                    ID_user, Card = (result2[0],result2[1])
                    print("oi",ID_user, Card)
                    cursor.execute(f"SELECT roomId from sissal.rooms where roomNumber = '{sala}'")
                    result3 = cursor.fetchall()
                    ID_room, = result3[0]
                    print(ID_room)
                    if len(result) == 0:
                        cursor.execute(f"INSERT INTO sissal.bookingrooms (userId, roomId, roomNumber, userCard, userName, startHour, endHour, bookingDate) VALUES ({ID_user}, {ID_room}, {sala}, {Card}, '{username}', '{horaConsulta}' , ADDTIME('{horaConsulta}', '02:00:00'), '{dataConsulta}')")
                        resposta = {'mensagem': 'True'}
                        connection.commit()
                        print(cursor.fetchall())
                        return resposta
                    else:
                        resposta = {'mensagem': 'Sala Preenchida'}
                        return resposta

                except Exception as e:
                    print("Não foi possível localizar o usuário. Erro:", e)
                    resposta = {'Error'}
                    return resposta
    future = executor.submit(reserva_Sala_func)
    resposta = future.result()
    print(resposta)
    return jsonify(resposta)


if __name__ == '__main__':
    app.run(debug=True) 
