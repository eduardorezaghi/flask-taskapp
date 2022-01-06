from logging import debug
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from werkzeug.exceptions import TooManyRequests
from werkzeug.utils import redirect

# CONFIGURAÇÕES DO APP
# --------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# CONFIGURAÇÕES DO MODEL
# --------------------
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id


# CONFIGURAÇÕES DAS ROTAS
# --------------------

# ROTA RAIZ
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Houve um erro ao adicionar a tarefa.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)



# ROTA RAIZ
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Não foi possível deletar essa tarefa.'



# ROTA PARA ATUALIZAR TAREFA COM DETERMINADO ID
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):

    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Não foi possível atualizar essa tarefa.'
    else:
        return render_template('update.html', task=task)



# Se o módulo for executado diretamente "python app.py"
# rode o app em modo debug.
if __name__ == '__main__':
    app.run(debug=True)
