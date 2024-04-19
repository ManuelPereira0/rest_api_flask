from models import Pessoas
from models import Usuarios
from sqlalchemy import *    

def insere_pessoas():
    pessoa = Pessoas(nome='André', idade=40)
    pessoa.save()
    
def consulta_pessoas():
    pessoa = Pessoas.query.filter_by(nome='Felipe')
    for p in pessoa:
        print(p)
        
def alterar_pessoas():
    pessoa = Pessoas.query.filter_by(nome='André').first()
    pessoa.nome = 'Manuel'
    pessoa.save()

def excluir_pessoas():
    pessoa = Pessoas.query.filter_by(nome='Manuel').first()
    pessoa.delete()
    
def insere_usuarios(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()
    
def consulta_usuarios() :
    usuarios = Usuarios.query.all()
    print (usuarios)
    
if __name__ == '__main__':
    # insere_usuarios('Manuel','1234')
    # insere_usuarios('Rafel', '5678')
    consulta_usuarios()
    # alterar_pessoas()
    # excluir_pessoas()
    # consulta_pessoas()