from BisApp import db, models
import unittest
import datetime

class TechAppTestCase(unittest.TestCase):

	def setUp(self):
		db.drop_all()
		db.create_all()


	def test_add_usuario(self):
		#data = datetime.date(2017,9,12)
		#print(data)
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'M'))
		db.session.add(models.Usuario('User3','Senha3', 'Endereco3', '3', 'F'))
		db.session.add(models.Usuario('User4','Senha4', 'Endereco4', '4', 'F'))
		db.session.commit()

		Usuarios = models.Usuario.query.all()
		self.assertEqual(Usuarios[3].nome, 'User4')
		Usuario = models.Usuario.query.filter_by(nome = 'User1').first()
		self.assertEqual(Usuario.nome, 'User1')
		self.assertEqual(len(Usuarios), 4)

	def test_alterar_usuario(self):
		usuario = models.Usuario('User1','Senha1', 'Endereco1', '1', 'M')
		db.session.add(usuario)
		db.session.commit()
		models.alterar_usuario(usuario.id, 'UserAlterado')
		self.assertEqual(usuario.nome, 'UserAlterado')


	def test_remover_usuario(self):
		usuario = models.Usuario('User1','Senha1', 'Endereco1', '1', 'M')
		db.session.add(usuario)
		db.session.commit()
		count = len(models.Usuario.query.all())
		models.remover_usuario(usuario.id)
		self.assertNotEqual(len(models.Usuario.query.all()), count)
		self.assertEqual(len(models.Usuario.query.all()), count-1)



	def test_add_emprestimo(self):
			db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
			db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))
			db.session.add(models.Emprestimo(1, 'pendente'))
			db.session.add(models.Emprestimo(1, 'pendente'))
			db.session.add(models.Emprestimo(2, 'devolvido'))
			db.session.add(models.Emprestimo(2, 'devolvido'))
			db.session.commit()

			emprestimos = models.Emprestimo.query.all()
			self.assertEqual(emprestimos[3].status, 'devolvido')
			emprestimo = models.Emprestimo.query.filter_by(status = 'pendente').first()
			self.assertEqual(emprestimo.status, 'pendente')
			self.assertEqual(len(emprestimos), 4)


	def test_alterar_emprestimo(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		emprestimo = models.Emprestimo(1, 'pendente')
		db.session.add(emprestimo)
		db.session.commit()
		models.alterar_emprestimo(emprestimo.id, 'devolvido')
		self.assertEqual(emprestimo.status, 'devolvido')


	def test_remover_emprestimo(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		emprestimo = models.Emprestimo(1, 'pendente')
		db.session.add(emprestimo)
		db.session.commit()
		count = len(models.Emprestimo.query.all())
		models.remover_emprestimo(emprestimo.id)
		self.assertNotEqual(len(models.Emprestimo.query.all()), count)
		self.assertEqual(len(models.Emprestimo.query.all()), count-1)


	def test_add_exemplar(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(2, 'devolvido'))
		db.session.add(models.Emprestimo(2, 'devolvido'))

		#titulo, editora, edicao, ano_edicao, observacao, quantidade, id_emprestimo
		db.session.add(models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1))
		db.session.add(models.Exemplar('titulo2', 'editora1', 'primeira', 1, 'observacao2', 1, 2))
		db.session.add(models.Exemplar('titulo3', 'editora2', 'segunda', 1, 'observacao3', 1, 3))
		db.session.add(models.Exemplar('titulo4', 'editora2', 'segunda', 1, 'observacao4', 1, 4))
		db.session.commit()

		exemplares = models.Exemplar.query.all()
		self.assertEqual(exemplares[3].titulo, 'titulo4')
		exemplar = models.Exemplar.query.filter_by(titulo = 'titulo1').first()
		self.assertEqual(exemplar.titulo, 'titulo1')
		self.assertEqual(len(exemplares), 4)


	def test_alterar_exemplar(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(2, 'devolvido'))
		db.session.add(models.Emprestimo(2, 'devolvido'))

		exemplar = models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1)
		db.session.add(exemplar)
		db.session.commit()
		models.alterar_exemplar(exemplar.id, 'tituloAlterado')
		self.assertEqual(exemplar.titulo, 'tituloAlterado')


	def test_remover_exemplar(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(2, 'devolvido'))
		db.session.add(models.Emprestimo(2, 'devolvido'))

		exemplar = models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1)
		db.session.add(exemplar)
		db.session.commit()
		count = len(models.Exemplar.query.all())
		models.remover_exemplar(exemplar.id)
		self.assertNotEqual(len(models.Exemplar.query.all()), count)
		self.assertEqual(len(models.Exemplar.query.all()), count-1)


	def test_add_autor(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))

		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		db.session.add(models.Emprestimo(2, 'devolvido'))
		db.session.add(models.Emprestimo(2, 'devolvido'))

		exemplar = models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1)
		exemplar2 = models.Exemplar('titulo2', 'editora2', 'primeira', 1, 'observacao2', 1, 2)
		#exemplar3 = models.Exemplar('titulo3', 'editora3', 'segunda', 1, 'observacao1', 1, 3)
		#exemplar4 = models.Exemplar('titulo4', 'editora4', 'segunda', 1, 'observacao2', 1, 4)
		db.session.add(exemplar)
		db.session.add(exemplar2)
		#db.session.add(exemplar3)
		#db.session.add(exemplar4)

		db.session.add(models.Autor('autor1', 'biografia1', exemplar))
		db.session.add(models.Autor('autor2', 'biografia2', exemplar))
		db.session.add(models.Autor('autor3', 'biografia3', exemplar2))
		db.session.add(models.Autor('autor4', 'biografia4', exemplar2))
		db.session.commit()

		
		autores = models.Autor.query.all()
		self.assertEqual(autores[3].nome, 'autor4')
		self.assertEqual(autores[3].exemplares[0].titulo, 'titulo2')
		autor = models.Autor.query.filter_by(nome = 'autor1').first()
		self.assertEqual(autor.nome, 'autor1')
		self.assertEqual(len(autores), 4)


	def test_alterar_autor(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		exemplar = models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1)
		exemplar2 = models.Exemplar('titulo2', 'editora2', 'primeira', 1, 'observacao2', 1, 2)
		db.session.add(exemplar)
		db.session.add(exemplar2)


		autor = models.Autor('autor1', 'biografia1', exemplar)
		db.session.add(autor)
		db.session.commit()
		models.alterar_autor(autor.id, 'autorAlterado', exemplar2)
		self.assertEqual(autor.nome, 'autorAlterado')


	def test_remover_autor(self):
		db.session.add(models.Usuario('User1','Senha1', 'Endereco1', '1', 'M'))
		db.session.add(models.Usuario('User2','Senha2', 'Endereco2', '2', 'F'))
		db.session.add(models.Emprestimo(1, 'pendente'))
		exemplar = models.Exemplar('titulo1', 'editora1', 'primeira', 1, 'observacao1', 1, 1)
		exemplar2 = models.Exemplar('titulo2', 'editora2', 'primeira', 1, 'observacao2', 1, 2)
		db.session.add(exemplar)
		db.session.add(exemplar2)


		autor = models.Autor('autor1', 'biografia1', exemplar)
		db.session.add(autor)
		db.session.commit()

		count = len(models.Autor.query.all())
		models.remover_autor(autor.id)
		self.assertNotEqual(len(models.Autor.query.all()), count)
		self.assertEqual(len(models.Autor.query.all()), count-1)







'''
	def test_anything(self):
		db.session.add(models.Loja('maravilhas 1'))
		db.session.add(models.Loja('maravilhas 2'))
		db.session.add(models.Loja('maravilhas 3'))
		db.session.add(models.Loja('maravilhas 4'))
		db.session.add(models.Loja('maravilhas 5'))
		db.session.commit()
		lojas = models.obter_lojas()

		self.assertEqual(len(lojas),5)
		self.assertEqual(lojas[0].titulo,'maravilhas 1')
		self.assertEqual(lojas,models.Loja.query.all())

	def test_inserir_loja(self):
		self.assertEqual(models.inserir_loja(titulo = 'UMI'), True)

		lojas = models.obter_lojas()
		self.assertEqual(lojas[0].titulo, 'UMI')
		loja = models.Loja.query.filter_by(titulo = 'UMI').first()
		self.assertEqual(loja.titulo, 'UMI')

	def test_alterar_loja(self):
		loja = models.Loja('maravilhas 1')
		db.session.add(loja)
		db.session.commit()
		models.alterar_loja(loja.id, 'ONE')
		self.assertEqual(loja.titulo, 'ONE')

	def test_remover_loja(self):
		loja = models.Loja('maravilhas 1')
		db.session.add(loja)
		db.session.commit()
		count = len(models.Loja.query.all())
		models.remover_loja(loja.id)
		self.assertNotEqual(len(models.Loja.query.all()), count)
		self.assertEqual(len(models.Loja.query.all()), count-1)
'''


if __name__ == '__main__':
	unittest.main()
