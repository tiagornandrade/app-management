from flask import Flask, render_template, url_for, request, session, redirect
from datetime import date, datetime
from flask.wrappers import Response
import pyodbc
import json


app = Flask(__name__)


server = '192.168.0.2' 
database = 'db_projetos' 
username = 'sa' 
password = 'SenhaDev1234' 

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = conn.cursor() 


def get_cliente():
    cursor.execute("SELECT nome_cliente FROM cliente GROUP BY nome_cliente")
    cliente = cursor.fetchall()
    response_cliente = [x for x in cliente]
    return response_cliente

def get_projeto():
    cursor.execute("SELECT nome_projeto FROM projeto GROUP BY nome_projeto")
    projeto = cursor.fetchall()
    response_projeto = [x for x in projeto]
    return response_projeto

def get_lider():
    cursor.execute("SELECT lider_projeto FROM projeto GROUP BY lider_projeto")
    lider = cursor.fetchall()
    response_lider = [x for x in lider]
    return response_lider

def get_ciclo():
    cursor.execute("SELECT nome_ciclo FROM ciclo WHERE ciclo_completo = 'Não'")
    ciclo = cursor.fetchall()
    response_ciclo = [x for x in ciclo]
    return response_ciclo


@app.route('/')
def index():
    # if 'email' in session:
    #     return 'Você está logado como ' + session['username']

    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # msg = ''
    # if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    #     # Create variables for easy access
    #     email       = request.form['email']
    #     password    = request.form['password']

    #     cursor.execute("SELECT * FROM usuario WHERE email = ? AND password = ?", email,password)
    #     user = cursor.fetchone()

    #     if 'email' in session:
    #         return 'Você está logado como ' + session['email']
    #     else:
    #         msg = 'Email/senha Incorreto!'
    # , msg=msg
    return render_template('index.html')

@app.route('/esqueceu-senha')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/registrar', methods=['POST', 'GET'])
def registrar():
    msg = ''
    if request.method == 'POST':
    #  and 'email' in request.form and 'password' in request.form and 'first_name' in request.form and 'last_name' in request.form:      
        email       = request.form['email']
        password    = request.form['password']
        first_name  = request.form['first_name']
        last_name   = request.form['last_name']
        criacao     = datetime.now().strftime('%Y%m%d')
        alteracao   = None
    
        cursor.execute('INSERT INTO usuario (email, password, first_name, last_name, criacao, alteracao) VALUES (?,?,?,?,?,?)', (email,password,first_name,last_name,criacao,alteracao))
        cursor.commit()
        msg = 'Registro efetuado com sucesso!'
        return redirect(url_for('registrar'))
    else:
        None

    return render_template('registrar.html', msg=msg)

@app.route('/home')
def home():
    cursor.execute("""exec sp_cliente""")
    cliente = cursor.fetchall()

    cursor.execute("""exec sp_tarefa""")
    tarefa = cursor.fetchall()

    cursor.execute("""exec sp_hora""")
    hora = cursor.fetchall()

    cursor.execute("""exec sp_fatura""")
    fatura = cursor.fetchall()

    cursor.execute("""exec sp_projeto""")
    projeto = cursor.fetchall()

    # cursor.execute("""\
    #     SELECT
    #         nome_ciclo AS ciclo
    #     FROM ciclo
    #     WHERE ciclo_completo = 'não'
    # """)
    # ciclo = cursor.fetchall()
    cursor.execute("""exec sp_ciclo""")
    ciclo = cursor.fetchall()

    return render_template('index.html', cliente=cliente, tarefa=tarefa, projeto=projeto, hora=hora, fatura=fatura, ciclo=ciclo)

#___________________#
#                   #
#   CRUD PROJETO    #
#                   #
#___________________#

# INCLUDE
@app.route('/projeto', methods=['POST', 'GET'])
def projeto():
    if request.method == 'POST':
        cursor              = conn.cursor()
        nome_projeto        = request.form['projeto']
        tipo_projeto        = request.form['tipo_projeto']
        nome_cliente        = request.form['cliente']
        lider_projeto       = request.form['lider']
        categoria_projeto   = request.form['categoria']
        valor_hora          = request.form['valor_hora']
        descricao           = request.form['descricao']
        criacao             = datetime.now().strftime('%Y%m%d')
        alteracao           = None

        cursor.execute("INSERT INTO projeto (nome_projeto,tipo_projeto,nome_cliente,lider_projeto,categoria_projeto,valor_hora,descricao,criacao,alteracao) VALUES (?,?,?,?,?,?,?,?)", (nome_projeto,tipo_projeto,nome_cliente,lider_projeto,categoria_projeto,valor_hora,descricao,criacao,alteracao))
        cursor.commit()
        return redirect(url_for('projeto'))
    else:
        None

    cliente = get_cliente()
    return render_template('projeto.html', cliente=cliente)

# UPDATE >> LIST
@app.route('/alterar_projeto', methods=['POST', 'GET'])
def alterar_projeto():
    cursor.execute('SELECT * FROM projeto')
    projeto = cursor.fetchall()
    return render_template('alterar_projeto.html', projeto=projeto)

# UPDATE >> ALTER
@app.route('/editar_projeto', methods=['POST', 'GET'])
def editar_projeto():
    if request.method == 'POST':
        id                  = request.form['id']
        nome_projeto        = request.form['nome_projeto']
        tipo_projeto        = request.form['tipo_projeto']
        nome_cliente        = request.form['nome_cliente']
        lider_projeto       = request.form['lider_projeto']
        categoria_projeto   = request.form['categoria_projeto']
        valor_hora          = request.form['valor_hora']
        descricao           = request.form['descricao']
        alteracao           = datetime.now().strftime('%Y%m%d')
        
        cursor.execute('UPDATE projeto SET nome_projeto = ?, tipo_projeto = ?, nome_cliente = ?, lider_projeto= ?, categoria_projeto = ?, valor_hora = ?, descricao = ?, alteracao = ? WHERE id_projeto = ?', nome_projeto,tipo_projeto,nome_cliente,lider_projeto,categoria_projeto,valor_hora,descricao,alteracao,id)
        cursor.commit()
        return redirect(url_for('alterar_projeto'))
    else:
        projeto_id = request.args.get('id')
        projeto    = cursor.execute('SELECT * FROM projeto WHERE id_projeto=?', projeto_id)
    return render_template('editar_projeto.html', projeto=projeto)

#___________________#
#                   #
#   CRUD CLIENTE    #
#                   #
#___________________#

# INCLUDE
@app.route('/cliente', methods=['POST', 'GET'])
def cliente():
    if request.method == 'POST':
        cursor              = conn.cursor()
        nome_cliente        = request.form['cliente']
        situacao_comercial  = request.form['situacao']
        servico_portfolio   = request.form['servico']
        descricao           = request.form['descricao']
        criacao             = datetime.now().strftime('%Y%m%d')
        alteracao           = None

        cursor.execute("INSERT INTO cliente (nome_cliente,situacao_comercial,servico_portfolio,descricao,criacao,alteracao) VALUES (?,?,?,?,?,?)", (nome_cliente,situacao_comercial,servico_portfolio,descricao,criacao,alteracao))
        cursor.commit()
        return redirect(url_for('cliente'))
    return render_template('cliente.html')

# UPDATE >> LIST
@app.route('/alterar_cliente', methods=['POST', 'GET'])
def alterar_cliente():
    cursor.execute('SELECT * FROM cliente')
    cliente = cursor.fetchall()
    return render_template('alterar_cliente.html', cliente=cliente)

# UPDATE >> ALTER
@app.route('/editar_cliente', methods=['POST', 'GET'])
def editar_cliente():
    if request.method == 'POST':
        id                  = request.form['id']
        nome_cliente        = request.form['nome_cliente']
        situacao_comercial  = request.form['situacao_comercial']
        servico_portfolio   = request.form['servico_portfolio']
        descricao           = request.form['descricao']
        alteracao           = datetime.now().strftime('%Y%m%d')
        
        cursor.execute('UPDATE cliente SET nome_cliente = ?, situacao_comercial= ?, servico_portfolio = ?, descricao = ?, alteracao = ? WHERE id_cliente = ?', nome_cliente,situacao_comercial,servico_portfolio,descricao,alteracao,id)
        cursor.commit()
        return redirect(url_for('alterar_cliente'))
    else:
        cliente_id = request.args.get('id')
        cliente    = cursor.execute('SELECT * FROM cliente WHERE id_cliente=?', cliente_id)
    return render_template('editar_cliente.html', cliente=cliente)

#___________________#
#                   #
#    CRUD CICLO     #
#                   #
#___________________#

# INCLUDE
@app.route('/ciclo', methods=['POST', 'GET'])
def ciclo():
    if request.method == 'POST':
        cursor          = conn.cursor()
        nome_ciclo      = request.form['nome_ciclo']
        data_inicio     = request.form['data_inicio']
        data_fim        = request.form['data_fim']
        descricao       = request.form['descricao']
        ciclo_completo  = 'Não'
        criacao         = datetime.now().strftime('%Y%m%d')
        alteracao       = None

        cursor.execute("INSERT INTO ciclo (nome_ciclo,data_inicio,data_fim,descricao,ciclo_completo,criacao,alteracao) VALUES (?,?,?,?,?,?,?)", (nome_ciclo,data_inicio,data_fim,descricao,ciclo_completo,criacao,alteracao))
        cursor.commit()
        return redirect(url_for('ciclo'))
    return render_template('ciclo.html')

# UPDATE >> LIST
@app.route('/alterar_ciclo', methods=['POST', 'GET'])
def alterar_ciclo():
    cursor.execute('SELECT * FROM ciclo')
    ciclo = cursor.fetchall()
    return render_template('alterar_ciclo.html', ciclo=ciclo)

# UPDATE >> ALTER
@app.route('/editar_ciclo', methods=['POST', 'GET'])
def editar_ciclo():
    if request.method == 'POST':
        id                  = request.form['id']
        nome_ciclo          = request.form['nome_ciclo']
        data_inicio         = request.form['data_inicio']
        data_fim            = request.form['data_fim']
        descricao           = request.form['descricao']
        ciclo_completo      = request.form['ciclo_completo']
        alteracao           = datetime.now().strftime('%Y%m%d')
        
        cursor.execute('UPDATE ciclo SET nome_ciclo = ?, data_inicio= ?, data_fim = ?, descricao = ?, ciclo_completo= ?, alteracao = ? WHERE id_ciclo = ?', nome_ciclo,data_inicio,data_fim,descricao,ciclo_completo,alteracao,id)
        cursor.commit()
        return redirect(url_for('alterar_ciclo'))
    else:
        ciclo_id = request.args.get('id')
        ciclo    = cursor.execute('SELECT * FROM ciclo WHERE id_ciclo=?', ciclo_id)
    return render_template('editar_ciclo.html', ciclo=ciclo)

@app.route('/excluir_ciclo', methods=['POST', 'GET'])
def excluir_ciclo():
    ciclo_id = request.args.get('id')
    cursor.execute('DELETE FROM ciclo WHERE id_ciclo=?', ciclo_id)
    cursor.commit()
    return render_template('alterar_ciclo.html')

#_______________#
#               #
#  CRUD TAREFA  #
#               #
#_______________#

# INCLUDE
@app.route('/tarefa', methods=['POST', 'GET'])
def tarefa():
    if request.method == 'POST':
        cursor              = conn.cursor()
        data                = request.form['data']
        time                = request.form['time']
        nome_tarefa         = request.form['nome_tarefa']
        nome_cliente        = request.form['nome_cliente']
        nome_projeto        = request.form['nome_projeto']
        lider_projeto       = request.form['lider_projeto']
        ciclo               = request.form['ciclo']
        descricao           = request.form['descricao']
        criacao             = datetime.now().strftime('%Y%m%d')
        alteracao           = None

        cursor.execute("INSERT INTO tarefa (data,time,nome_tarefa,nome_cliente,nome_projeto,nome_lider,ciclo,descricao,criacao,alteracao) VALUES (?,?,?,?,?,?,?,?,?,?)", (data,time,nome_tarefa,nome_cliente,nome_projeto,lider_projeto,ciclo,descricao,criacao,alteracao))
        cursor.commit()
        return redirect(url_for('tarefa'))
    else:
        None

    cliente = get_cliente()
    projeto = get_projeto()
    lider   = get_lider()
    ciclo   = get_ciclo()
    return render_template('tarefa.html', cliente=cliente, projeto=projeto, lider=lider, ciclo=ciclo)

# UPDATE >> LIST
@app.route('/alterar_tarefa', methods=['POST', 'GET'])
def alterar_tarefa():
    cursor.execute('SELECT * FROM tarefa')
    tarefa = cursor.fetchall()
    return render_template('alterar_tarefa.html', tarefa=tarefa)

# UPDATE >> ALTER
@app.route('/editar_tarefa', methods=['POST', 'GET'])
def editar_tarefa():
    if request.method == 'POST':
        id              = request.form['id']
        data            = request.form['data']
        time            = request.form['time']
        nome_tarefa     = request.form['nome_tarefa']
        nome_cliente    = request.form['nome_cliente']
        nome_projeto    = request.form['nome_projeto']
        nome_lider      = request.form['nome_lider']
        ciclo           = request.form['ciclo']
        descricao       = request.form['descricao']
        alteracao       = datetime.now().strftime('%Y%m%d')
        
        cursor.execute('UPDATE tarefa SET data = ?, time = ?, nome_tarefa = ?, nome_cliente = ?, nome_projeto = ?, nome_lider = ?, ciclo = ?, descricao = ?, alteracao = ?  WHERE id_tarefa = ?', data,time,nome_tarefa,nome_cliente,nome_projeto,nome_lider,ciclo,descricao,alteracao,id)
        cursor.commit()
        return redirect(url_for('alterar_tarefa'))
    else:
        tarefa_id = request.args.get('id')
        tarefa    = cursor.execute('SELECT * FROM tarefa WHERE id_tarefa=?', tarefa_id)
        return render_template('editar_tarefa.html', tarefa=tarefa)

@app.route('/dash_vendas')
def dash_vendas():
    return render_template('dash_vendas.html')

@app.route('/dash_rh')
def dash_desafio():
    return render_template('dash_rh.html')

@app.route('/dash_projetos')
def dash_projetos():
    return render_template('dash_projetos.html')

@app.route('/dash_suprimentos')
def suprimentos():
    return render_template('dash_suprimentos.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')


if __name__ == "__main__":
    app.secret_key = "app-management-2"
    app.run(use_reloader=True, debug=True)