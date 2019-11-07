from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TODO(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with add new task'

    else:

            tasks = TODO.query.order_by(TODO.date_created).all()
            return render_template('index.jinja2', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = TODO.query.get_or_404(id)
    print(id)
    if request.method == 'GET':
        return render_template('update.jinja2', task=task)
    else:
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Unable to Update'



if __name__ == '__main__':
    app.run()
