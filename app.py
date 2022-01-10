from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toDo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)


@app.route('/',methods=["POST","GET"])
def index():  # put application's code here
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)


@app.route('/add', methods=["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")

    newTodo = Todo(title=title, content=content, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def complete(id):
    todo = Todo.query.filter_by(id=id).first()
    if(todo.complete == False):
        todo.complete = True
    else:
        todo.complete = False
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
