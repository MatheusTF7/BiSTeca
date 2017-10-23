# coding: utf-8
from BisApp import app, db, models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, name='BiSTeca', template_mode='bootstrap3')
admin.add_view(ModelView(models.Usuario, db.session))
admin.add_view(ModelView(models.Emprestimo, db.session))
admin.add_view(ModelView(models.Exemplar, db.session))
admin.add_view(ModelView(models.Autor, db.session))
admin.add_view(ModelView(models.Contato, db.session))


if __name__ == '__main__':
    app.run() 