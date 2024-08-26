from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to-do.db"
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Integer, nullable=False)
    task_text = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return 'Task %r' % self.id


@app.route('/', methods=['GET', 'POST'])
# @app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    # Подгружаем все задачи из базы данных
    tasks_list = Task.query.order_by(Task.id.desc()).all()

    # Обрабатываем создание новой задачи
    if request.method == 'POST':
        print()
        print("> POST Method <")
        print()
        task_text = request.form['task']
        
        if len(task_text) > 0:
            task = Task(task_text=task_text, completed=0)
            try:
                db.session.add(task)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                pprint(e)
                return "Shit happend bro... There is a trouble with saving your task :("
        else:
            return render_template("components/warning.html", tasks_list=tasks_list)
    
    # Просто рендерим страницу
    return render_template("tasks.html", tasks_list=tasks_list)


@app.route('/tasks_2', methods=['GET', 'POST'])
# @app.route('/tasks', methods=['GET', 'POST'])
def tasks_2():
    # Подгружаем все задачи из базы данных
    tasks_list = Task.query.order_by(Task.id.desc()).all()

    # Обрабатываем создание новой задачи
    if request.method == 'POST':
        print()
        print("> POST Method <")
        print()
        task_text = request.form['task']
        
        if len(task_text) > 0:
            task = Task(task_text=task_text, completed=0)
            try:
                db.session.add(task)
                db.session.commit()
                return redirect('/tasks_2')
            except Exception as e:
                pprint(e)
                return "Shit happend bro... There is a trouble with saving your task :("
        else:
            return render_template("components/warning_2.html", tasks_list=tasks_list)
    
    # Просто рендерим страницу
    return render_template("tasks_2.html", tasks_list=tasks_list)


@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    
    except Exception as e:
        pprint(e)
        return "Shit happend bro... We can't delete your task :("


@app.route('/update/<int:id>')
def check(id):
    task = Task.query.get_or_404(id)
    task.completed = 0 if task.completed else 1

    try:
        db.session.commit()
        return redirect('/tasks_2')
    
    except Exception as e:
        pprint(e)
        return "Shit happend bro... We can't delete your task :("


# @app.route('/statistics')
# def statistics():
#     return render_template("statistics.html")


# @app.route('/about')
# def about():
#     return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)