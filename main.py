from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.secret_key = "87b273ctxr9o78gynbgwor"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
db = SQLAlchemy(app)


class tasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.String(100), nullable=False)

    def __init__(self, data):
        self.data = data


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        task = request.form["task_data"]
        if task:
            new_task = tasks(data=task)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added!", "info")
            return redirect("/")
    data = tasks.query.all()
    return render_template("index.html", data=data)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task_to_delete = tasks.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash("Task deleted!", "info")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
with app.app_context():
    db.create_all()
