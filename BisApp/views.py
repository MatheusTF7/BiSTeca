from BisApp import app, db, models
from flask import render_template, redirect, url_for, request, session, flash

##################################################################################################
########## dados pré carregados ###########################
db.drop_all()
db.create_all()
db.session.add(models.Usuario('admin','admin', 'Endereco Admin', '111.111.111-11', 'M', 'Adm'))
db.session.add(models.Usuario('user','user', 'Endereco user', '222.222.222-22', 'M', 'User'))
db.session.add(models.Emprestimo(1, 'pendente'))
db.session.add(models.Emprestimo(1, 'devolvido'))
db.session.add(models.Emprestimo(2, 'pendente'))
db.session.add(models.Emprestimo(2, 'devolvido'))
exemplar1 = models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1)
exemplar2 = models.Exemplar('titulo2', 'editora2', 'segunda', 1, 'observacao2', 1, 2)
db.session.add(exemplar1)
db.session.add(exemplar2)
db.session.add(models.Exemplar('titulo3', 'editora3', 'terceira', 1, 'observacao3', 1, 2))
db.session.add(models.Autor('autor3', 'biografia3', exemplar1))
db.session.add(models.Autor('autor4', 'biografia4', exemplar2))
db.session.add(models.Contato('Contato 1', 'email 1', 'cpf 1', 'msg 1'))
db.session.add(models.Contato('Contato 2', 'email 2', 'cpf 2', 'msg 2'))
db.session.add(models.Contato('Contato 3', 'email 3', 'cpf 3', 'msg 3'))
db.session.commit()



app.secret_key = 'senha'
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'usuario' in session:
		return render_template('index.html')
	if request.method == 'POST':
		usuario = request.form['usuario']
		senha = request.form['senha']
		u = models.Usuario.query.filter_by(nome = usuario).first() 

		if(u is not None and u.senha == senha):
			session['usuario'] = u.tipo 
			flash('Login efetuado com sucesso!') 
			return render_template('index.html')
		else:
			flash('Tentativa de Login falhou!')
			return render_template('login.html')
	return render_template('login.html')

@app.route('/logout')
def logout():  
	if 'usuario' in session:
		session.pop('usuario', None)
		flash('Logout efetuado com sucesso!')
	return render_template('index.html')

@app.route('/') 
@app.route('/home')
def homepage():
	return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
	if request.method == 'POST':
		nome = request.form.get('nome')
		email = request.form.get('email')
		cpf = request.form.get('cpf')
		msg = request.form.get('msg')
		db.session.add(models.Contato(nome, email, cpf, msg))
		db.session.commit()
		flash('Contato enviado com sucesso!')
	return render_template('contato.html', Lista = models.Contato.query.all())

@app.route('/contato/excluir/<int:index>')
def removerContato(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.remover_contato(index)
	flash('Contato excluído com sucesso!')
	return redirect(url_for('contato'))

@app.route('/contato/alterar/<int:index>', methods=['GET', 'POST'])
def alterarContato(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		nome = request.form.get('nome')
		email = request.form.get('email')
		cpf = request.form.get('cpf')
		msg = request.form.get('msg')
		models.alterar_contato(index, nome, email, cpf, msg)
		flash('Contato alterado com sucesso!')
		return redirect(url_for('contato'))
	contato = models.Contato.query.get(index)
	return render_template('contato.html', Informacoes = contato, index = index, Lista = models.Contato.query.all())


@app.route('/cadusuario', methods=['GET', 'POST'])
def cadusuario():
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		nome = request.form.get('nome')
		endereco = request.form.get('endereco')
		cpf = request.form.get('cpf')
		sexo = request.form.get('sexo')
		#usuario = request.form['usuario']
		tipo = request.form.get('tipo')
		senha = request.form.get('senha')
		confSenha = request.form.get('confirmarSenha')
		if (senha == confSenha):
			db.session.add(models.Usuario(nome, senha, endereco, cpf, sexo, tipo))
			db.session.commit()
			flash('Usuário cadastrado com sucesso!')
		else:
			return flash('Falha no cadastro. Senhas não correspondem!')
		return render_template('cadastro-usuario.html', Lista = models.Usuario.query.all())
	return render_template('cadastro-usuario.html', Lista = models.Usuario.query.all())

@app.route('/cadusuario/excluir/<int:index>')
def removerUsuario(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.remover_usuario(index)
	flash('Usuário excluído com sucesso!')
	return redirect(url_for('cadusuario'))

@app.route('/cadusuario/alterar/<int:index>', methods=['GET', 'POST'])
def alterarUsuario(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		nome = request.form.get('nome')
		endereco = request.form.get('endereco')
		cpf = request.form.get('cpf')
		sexo = request.form.get('sexo')
		#usuario = request.form['usuario']
		tipo = request.form.get('tipo')
		senha = request.form.get('senha')
		confSenha = request.form.get('confirmarSenha')
		models.alterar_usuario(index, nome, endereco, cpf, sexo, tipo, senha)
		flash('Usuário alterado com sucesso!')
		return redirect(url_for('cadusuario'))
	usuario = models.Usuario.query.get(index)
	return render_template('cadastro-usuario.html', Informacoes = usuario, index = index, Lista = models.Usuario.query.all())


@app.route('/cadlivro', methods=['GET', 'POST'])
def cadlivro():
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		titulo = request.form.get('titulo')
		editora = request.form.get('editora')
		edicao = request.form.get('edicao')
		ano_edicao = request.form.get('ano_edicao')
		qtde = request.form.get('qtde')
		#autor = request.form['autor']
		#emprestimo = request.form.get('emprestimo')
		obs = request.form.get('obs')
		db.session.add(models.Exemplar(titulo, editora, edicao, ano_edicao, obs, qtde, 0))
		db.session.commit()
		flash('Livro cadastrado com sucesso!')
		#return render_template('cadastro-livro.html', autores = models.Autor.query.all(),  emprestimos = models.Emprestimo.query.all())
	return render_template('cadastro-livro.html', autores = models.Autor.query.all(), Lista = models.Exemplar.query.all())


@app.route('/cadlivro/excluir/<int:index>')
def removerExemplar(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.remover_exemplar(index)
	flash('Livro excluído com sucesso!')
	return redirect(url_for('cadlivro'))

@app.route('/cadlivro/alterar/<int:index>', methods=['GET', 'POST'])
def alterarExemplar(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		titulo = request.form.get('titulo')
		editora = request.form.get('editora')
		edicao = request.form.get('edicao')
		ano_edicao = request.form.get('ano_edicao')
		qtde = request.form.get('qtde')
		#autor = request.form['autor']
		#emprestimo = request.form.get('emprestimo')
		obs = request.form.get('obs')
		models.alterar_exemplar(index, titulo, editora, edicao, ano_edicao, obs, qtde, 0)
		flash('Livro alterado com sucesso!')
		#db.session.add(models.Exemplar(titulo, editora, edicao, ano_edicao, obs, qtde, 0))
		return redirect(url_for('cadlivro'))
	livro = models.Exemplar.query.get(index)
	return render_template('cadastro-livro.html', Informacoes = livro, index = index, Lista = models.Exemplar.query.all())

@app.route('/cadautor', methods=['GET', 'POST'])
def cadautor():
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		nome = request.form.get('nome')
		exemplar = request.form.get('exemplar')
		#print(exemplar)
		biografia = request.form.get('biografia')
		if (exemplar is not None):
			exemplar_add = models.Exemplar.query.filter_by(id = exemplar).first()
		db.session.add(models.Autor(nome, biografia, exemplar_add))
		db.session.commit()
		flash('Autor cadastrado com sucesso!')
	return render_template('cadastro-autor.html', exemplares = models.Exemplar.query.all(), Lista = models.Autor.query.all(), sec = session)

@app.route('/cadautor/excluir/<int:index>')
def removerAutor(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.remover_autor(index)
	flash('Autor excluído com sucesso!')
	return redirect('cadautor')

@app.route('/cadautor/alterar/<int:index>', methods=['GET', 'POST'])
def alterarAutor(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		nome = request.form.get('nome')
		biografia = request.form.get('biografia')
		exemplar = request.form.get('exemplar')
		if (exemplar is not None):
			exemplar_add = models.Exemplar.query.filter_by(id = exemplar).first()

		models.alterar_autor(index, nome, exemplar_add, biografia)
		flash('Autor alterado com sucesso!')
		return redirect(url_for('cadautor'))
	autor = models.Autor.query.get(index)
	return render_template('cadastro-autor.html', Informacoes = autor, index = index, Lista = models.Autor.query.all(), exemplares = models.Exemplar.query.all(), sec = session)


@app.route('/consacervo')
def consacervo():
    return render_template('cadastro-livro.html', consulta = 'c', Lista = models.Exemplar.query.all(), sec = session)


@app.route('/emprestimo', methods=['GET', 'POST'])
def emprestimo():
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	if request.method == 'POST':
		usuario = request.form.get('usuario')
		#exemplar = request.form['exemplar']
		status = request.form.get('status')
		db.session.add(models.Emprestimo(usuario, status))
		db.session.commit()
		flash('Empréstimo cadastrado com sucesso!')
	return render_template('emprestimo.html', exemplares =  models.Exemplar.query.all(), usuarios =  models.Usuario.query.all(), Lista = models.Emprestimo.query.all(), sec = session)

@app.route('/emprestimo/excluir/<int:index>')
def removerEmprestimo(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.remover_emprestimo(index)
	flash('Empréstimo excluído com sucesso!')
	return redirect(url_for('emprestimo'))

@app.route('/emprestimo/devolver/<int:index>', methods=['GET', 'POST'])
def devolverEmprestimo(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.alterar_emprestimo(index, 'devolvido')
	flash('Empréstimo devolvido com sucesso!')
	return redirect(url_for('emprestimo'))
	autor = models.Autor.query.get(index)
	return render_template('emprestimo.html', index = index, Lista = models.Emprestimo.query.all(), sec = session)

@app.route('/emprestimo/reabrir/<int:index>', methods=['GET', 'POST'])
def reabrirEmprestimo(index):
	if 'usuario' not in session or session['usuario'] != 'Adm':
		return render_template('index.html', sec = session)
	models.alterar_emprestimo(index, 'pendente')
	flash('Empréstimo alterado para pendente com sucesso!')
	return redirect(url_for('emprestimo'))
	autor = models.Autor.query.get(index)
	return render_template('emprestimo.html', index = index, Lista = models.Emprestimo.query.all(), sec = session)



########################################################################
########## área de testes ##############################################
#ver apenas a estrutura da pagina layuot da pagina
@app.route('/cleanhome')
def homepageclean():
	return render_template('index.html')


@app.route('/teste')
def teste():
	return render_template('contato.html')