from app import app
from flask import render_template
from flask import request
import requests
import json
link = "https://flaskisabella-default-rtdb.firebaseio.com/"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titulo="Página Inicial")

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo="Contato")

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo="Cadastro")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    try:
        cpf        = request.form.get("cpf")
        nome       = request.form.get("nome")
        telefone   = request.form.get("telefone")
        endereco   = request.form.get("endereco")
        dados      = {"cpf":cpf, "nome":nome, "telefone":telefone, "endereco":endereco}
        requisicao = requests.post(f'{link}/cadastro/.json', data = json.dumps(dados))
        return 'Cadastrado com sucesso!'
    except Exception as e:
        return f'Ocorreu um erro\n +{e}'

@app.route('/listar')
def listarTudo():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        return dicionario
    except Exception as e:
        return f'Algo deu errado\n +{e}'


@app.route('/listarIndividual', methods=['POST'])
def listarIndividual(cpf):
    try:
        requesicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requesicao.json()
        for codigo in dicionario:
            chave = dicionario[codigo]['cpf']
            if chave == cpf:
                idCadastro = codigo
                return idCadastro
    except Exception as e:
        return f'Algo deu errado\n {e}'


@app.route('/individual', methods=['GET', 'POST'])
def individual():
    idCadastro = None
    try:
        if request.method == 'POST':
            cpf = request.form.get("cpfConsulta")
            dados = {"cpf": cpf}
            idCadastro = listarIndividual(cpf)
            requisicao = requests.get(f'{link}/cadastro/{idCadastro}/.json', data=json.dumps(dados))

        return render_template('individual.html', titulo="Consultar Individual", idCadastro=idCadastro)
    except Exception as e:
        return f'Ocorreu um erro\n {e}'


@app.route('/atualizar')
def atualizar():
    return render_template('/cadastroAtualizar.html', titulo="Atualizar")

@app.route('/cadastroAtualizar', methods=['POST'])
def atualizarCadastro():
    try:
        cpf = request.form.get("cpfAtualizar")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")

        dados = {"nome": nome, "telefone": telefone, "endereco": endereco}
        idCadastro = listarIndividual(cpf)
        requisicao = requests.patch(f'{link}/cadastro/{idCadastro}/.json', data = json.dumps(dados))
        return render_template('cadastroAtualizar.html', titulo="Atualizar cadastro")
    except Exception as e:
        return f'Ocorreu um erro\n {e}'


@app.route('/excluir', methods=['GET', 'POST'])
def excluir():
    if request.method == 'POST':
        try:
            cpf = request.form.get("cpfExcluir")
            dados = {"cpf": cpf}
            idCadastro = listarIndividual(cpf)
            requisicao = requests.delete(f'{link}/cadastro/{idCadastro}/.json', data=json.dumps(dados))

            return render_template('excluir.html', titulo="Excluir", sucesso=True)
        except Exception as e:
            return f'Ocorreu um erro\n {e}'

    return render_template('excluir.html', titulo="Excluir")