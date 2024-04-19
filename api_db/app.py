from flask import Flask, session
from flask import request
from flask_restful import Api
from flask_restful import Resource
from models import Pessoas
from models import Atividades
from models import Usuarios
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import joinedload

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first() 
    
class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        atividades = Atividades.query.join(Pessoas).filter(Pessoas.nome == nome).all()
        nome_atividades = [atividade.nome for atividade in atividades]
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id,
                'atividades':nome_atividades
            }
            
        except AttributeError:
            response = {'status': 'erro', 'mensagem':f'O nome {nome} não consta em nossa base de dados!'}
            
        return response
    
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response
    
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        return {'status':'Sucesso', 'messagem':f'Registro {nome} deletado com sucesso!'}


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response


class InserirPessoas(Resource):
    def post(self):
        dados = request.json
        pessoa = Pessoas(
            nome=dados['nome'],
            idade=dados['idade']
        )
        pessoa.save()
        return {'status': 'Sucesso', 'mensagem': f'Registro com o ID {pessoa.id} inserido com sucesso!'}
    

class ListaGeralAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response


class ListaAtividadesPessoa(Resource):
    def get(self, id_pessoa):
        atividade = Atividades.query.filter_by(id_pessoa=id_pessoa).first()
        try:
            response = {
                'id':atividade.id,
                'nome':atividade.nome,
                'pessoa':atividade.pessoa.nome,
                'id_pessoa':atividade.id_pessoa
            }
        
        except AttributeError:
            response = {'status':'Erro', 'menssagem':f'Não foi possivel encontrar uma tarefa com o id de responsável {id_pessoa}'}
        
        return response

class InserirAtividades(Resource):
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        return {'status': 'Sucesso', 'mensagem': f'Registro com o ID {atividade.id} inserido com sucesso!'}
    

class ListaPorAtividades(Resource):
    def get(self, atividade):
        pessoas = Pessoas.query.join(Atividades).filter(Atividades.nome == atividade).all()
        nomes_pessoas = [pessoa.nome for pessoa in pessoas]
        try:
            response = {
                'nome':atividade,
                'pessoa':nomes_pessoas
            }
             
        except AttributeError:
            response = {'status':'Erro', 'menssagem':f'Não foi possivel encontrar uma tarefa com esse nome'}
        
        return response
        
        
    
api.add_resource(Pessoa, '/pessoa/<string:nome>')   
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(InserirPessoas, '/pessoa/')
api.add_resource(InserirAtividades, '/atividade/')
api.add_resource(ListaGeralAtividades, '/atividade/')
api.add_resource(ListaAtividadesPessoa, '/atividade/<int:id_pessoa>')
api.add_resource(ListaPorAtividades, '/atividade/<string:atividade>')
    
if __name__ == '__main__':
    app.run(debug=True)