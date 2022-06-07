from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime as dt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todolist.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(), unique=False, nullable=False)
    todo_text = db.Column(db.String(50), unique=False, nullable=False)
    todo_status = db.Column(db.String(), unique=False, nullable=False)

db.create_all()

@app.route("/", methods=["POST", "GET"])
def home():
    todo_list = ToDo.query.all()
    if request.method == "POST":
        new_todo = ToDo(
            date = dt.datetime.now().strftime("%d %b"),
            todo_text = request.form['todo'],
            todo_status = "In progress"
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html", todo_list=todo_list)

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_to_delete = ToDo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/finished/<int:todo_id>")
def finished(todo_id):
    finished_todo = ToDo.query.get(todo_id)
    finished_todo.todo_status = "Finished"
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)