from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from BisApp import db

# N : N
AutorExemplar = db.Table(
    'autorExemplar',
    #id = db.Column(db.Integer, primary_key = True),
    db.Column('id_autor', db.Integer, db.ForeignKey('autor.id')),
    db.Column('id_exemplar', db.Integer, db.ForeignKey('exemplar.id'))
)



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40))
    senha = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    cpf = db.Column(db.String(14))
    #data_nasc = db.Column(db.DateTime)
    sexo = db.Column(db.String(10))

    emprestimos = db.relationship(              # Para os relacionamento de 1 : N
        'Emprestimo',
        backref='usuario',
        lazy='dynamic')

    def __init__(self, nome, senha, endereco, cpf, sexo):
        self.nome = nome
        self.senha = senha
        self.endereco = endereco
        self.cpf = cpf
        #self.data_nasc = data_nasc
        self.sexo = sexo



class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #data_emprestimo = db.Column(db.DateTime)
    #data_devolucao = db.Column(db.DateTime)
    #id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    #id_exemplar = db.Column(db.Integer, db.ForeignKey('exemplar.id'))
    status = db.Column(db.String(10)) #devolvido / pendente

    id_usuario = db.Column(                    # Para os relacionamento de 1 : N
        db.Integer,
        db.ForeignKey('usuario.id'))

    def __init__(self, id_usuario, status):
        #self.data_emprestimo = data_emprestimo
        #self.data_devolucao = data_devolucao
        self.id_usuario = id_usuario
        #self.id_exemplar = id_exemplar
        self.status = status


'''    # 1 : N
    usuario = db.relationship(              
        'Usuario',
        backref='emprestimo',
        lazy='dynamic')
'''
    

'''    # 1 : 1
    exemplar = db.relationship(        
        'Exemplar',
        backref='emprestimo',
        uselist=False)
'''


class Exemplar(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(40))
    editora = db.Column(db.String(20))
    edicao = db.Column(db.String(10))
    ano_edicao = db.Column(db.Integer)
    #data_cadastro = db.Column(db.DateTime)
    observacao = db.Column(db.Text)
    quantidade = db.Column(db.Integer)

    id_emprestimo = db.Column(
        db.Integer,
        db.ForeignKey('emprestimo.id'))


    emprestimo = db.relationship(             # Para os relacionamento de 1 : 1
            'Emprestimo',
            backref='exemplar',
            uselist=False)

    autores = db.relationship(                 # Para os relacionamento de N : N
    
        'Autor',
    
        secondary=AutorExemplar,
    
        backref=db.backref(
            'exemplar',
            lazy='dynamic'))

    def __init__(self, titulo, editora, edicao, ano_edicao, observacao, quantidade, id_emprestimo):
        self.titulo = titulo  
        self.editora = editora
        self.edicao = edicao
        self.ano_edicao = ano_edicao
        #self.data_cadastro = data_cadastro
        self.observacao = observacao
        self.quantidade = quantidade
        self.id_emprestimo = id_emprestimo


class Autor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40))
    biografia = db.Column(db.Text)

    exemplares = db.relationship(          # Para os relacionamento de N : N
        'Exemplar',
        secondary=AutorExemplar,
        backref=db.backref(
        'autor',
        lazy='dynamic'))

    def __init__(self, nome, biografia, exemplar):
        self.nome = nome
        self.biografia = biografia
        self.exemplares.append(exemplar)


def alterar_usuario(id, nome):
    usuario = Usuario.query.get(id)

    if usuario is not None:
        usuario.nome = nome
        db.session.commit()
    else:
        raise Exception('Usuario não existe!')

def remover_usuario(id):
    usuario = Usuario.query.get(id)

    if usuario is not None:
        db.session.delete(usuario)
        db.session.commit()
    else:
        raise Exception('Usuario não existe!')

def alterar_emprestimo(id, status):
    emprestimo = Emprestimo.query.get(id)

    if emprestimo is not None:
        emprestimo.status = status
        db.session.commit()
    else:
        raise Exception('Emprestimo não existe!')

def remover_emprestimo(id):
    emprestimo = Emprestimo.query.get(id)

    if emprestimo is not None:
        db.session.delete(emprestimo)
        db.session.commit()
    else:
        raise Exception('Emprestimo não existe!')

def alterar_exemplar(id, titulo):
    exemplar = Exemplar.query.get(id)

    if exemplar is not None:
        exemplar.titulo = titulo
        db.session.commit()
    else:
        raise Exception('Exemplar não existe!')

def remover_exemplar(id):
    exemplar = Exemplar.query.get(id)

    if exemplar is not None:
        db.session.delete(exemplar)
        db.session.commit()
    else:
        raise Exception('Exemplar não existe!')

def alterar_autor(id, nome, exemplar = None):
    autor = Autor.query.get(id)

    if autor is not None:
        autor.nome = nome
        autor.exemplares.append(exemplar)
        db.session.commit()
    else:
        raise Exception('Autor não existe!')

def remover_autor(id):
    autor = Autor.query.get(id)

    if autor is not None:
        autor.exemplares.clear()
        db.session.commit()
        db.session.delete(autor)
        db.session.commit()
    else:
        raise Exception('Autor não existe!')