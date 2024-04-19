from sqlalchemy import *
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///atividades.db")
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Pessoas(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), index=True)
    idade = Column(Integer)
    
    def __repr__(self):
        return f'<Pessoa {self.nome}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Atividades(Base):
    __tablename__ = 'atividade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
    id_pessoa = Column(Integer, ForeignKey('pessoas.id'))
    pessoa = relationship('Pessoas')
    
    def __repr__(self):
        return f'<Atividade {self.nome}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()
    

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    senha = Column(String(255))
    
    def __repr__(self):
        return f'<Usuario {self.login}'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()
        
    
def init_db():
    Base.metadata.create_all(bind=engine)
    
if __name__ == '__main__':
    init_db()