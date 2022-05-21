from models.user import User
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

from flask import (
    Blueprint, render_template, request, redirect, session, url_for
)

bp = Blueprint('user', __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST" and request.form["username"] != "" and request.form["password"] != "":
        missing = User.query.filter_by(name=request.form["username"].upper()).first()
        if missing is not None:
            if check_password_hash(missing.password,  request.form["password"]):
                session["username"] = request.form["username"].upper()
                session["id"] = missing.id
                return redirect('/')
            return render_template("login.html", msg="Invalid password")
        return render_template("login.html", msg="Non-existent user")
    return render_template("login.html")  


@bp.route("/register", methods=["GET", "POST"])
def register():
     
    if request.method == "POST" and request.form["username"] != "" and request.form["password"] != "":
        missing = User.query.filter_by(name=request.form["username"].upper()).first()
        if missing is None:
        
            user = User(name=request.form['username'].upper(), password=generate_password_hash(request.form['password']))
            try:
                db.session.add(user)
                db.session.commit()
                session["username"] = request.form["username"].upper()
                session["id"] = user.id
                return redirect('/')
            except:
                return "Houve um erro, ao inserir a tarefa"
        return render_template("register.html", msg="User is already register!")
    return render_template("register.html")  


@bp.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("id", None)
    return redirect(url_for("task.index"))