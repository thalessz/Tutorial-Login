from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector as mysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging
from user import User

# Inicializa o aplicativo e define a chave secreta (Serve para fins de debug)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chavesecreta'

# Instancia o LoginManager
loginManager = LoginManager()
# Define a rota inicial da aplicação para o LoginManager
loginManager.init_app(app)

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'login'
}

# Função com decorator para carregar o usuário
@loginManager.user_loader 
def load_user(user_id):
    # Configura a conexão
    connection = mysql.connect(**db_config)
    # Configura o "cursor". Ele que movimenta os dados e faz as operações
    cursor = connection.cursor()
    consulta = "SELECT * FROM USUARIO WHERE ID = %s"
    parametros = (user_id,)  # O tipo dos parâmetros é um tuple - tupla
    cursor.execute(consulta, parametros)  # Executa o sql, enviando a consulta e os parâmetros.
    user = cursor.fetchone()  # Pega o primeiro resultado que a consulta devolveu
    connection.close()  # Fecha a conexão após uso
    if user:  # Confere se usuário não é vazio.
        return User(user[0], user[1], user[2])  # Constroi o objeto utilizando a variável user do resultado
        # user[0] nesse caso é o id (primeira coluna), user[1] é o username (segunda coluna) e user[2] é a senha (terceira coluna)
    else:
        return None  # Não retorna nada, não há usuário.

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')  # Carrega a rota de login em /login

@app.route('/login_action', methods=['POST', 'GET'])
# Principais Métodos HTTP:
# GET: Recupera dados do servidor.
# Ex: GET /api/users

# POST: Envia dados ao servidor para criar um novo recurso.
# Ex: POST /api/users { "name": "Thales" }

# PUT: Atualiza um recurso existente ou cria um novo se não existir.
# Ex: PUT /api/users/1 { "name": "Thales Updated" }

# DELETE: Remove um recurso do servidor.
# Exemplo: DELETE /api/users/1

def login_action():
    username = request.form['username']
    password = request.form['password']
    remember = 'remember' in request.form
    
    connection = mysql.connect(**db_config)
    cursor = connection.cursor()
    consulta = "SELECT * FROM USUARIO WHERE username = %s"
    parametros = (username,)  # Corrigido para ser uma tupla
    cursor.execute(consulta, parametros)
    user = cursor.fetchone()
    
    # Se o usuário existir E user[2] (campo da senha) for igual à senha provida por ele, faz o login
    # Obs.: método porco, pesquise por hash nas senhas se quiser fazer melhor -.-
    
    if user and user[2] == password:
        usuario = User(user[0], user[1], user[2])  # Cria um objeto de usuário
        login_user(usuario, remember=remember)  # Faz o login do usuário, passando o obj de usuário como parâmetro, e o remember para manter a sessão
        return redirect(url_for('home'))
    else:
        flash('Login inválido.')
        return redirect(url_for('login'))

@app.route('/home')
@login_required  # O nome disso é decorador. Resumindo, é uma função embrulhando outra. A função user sobreescreve o código de Login_required, garantindo que o login esteja feito.
def home():
    return render_template('home.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)