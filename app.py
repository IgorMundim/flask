
import os
from datetime import datetime


from flask import Flask, render_template, request, redirect, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
app = Flask(__name__)
app.secret_key = "session"
Bootstrap(app)

# database setup.
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'todo.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# application models.

class User (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    """:type : str"""
    
    task = db.relationship("Task", backref="user")

    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.name}, content: {self.password}"


class Category (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    name = db.Column(db.String(200), nullable=False)
    """:type : str"""

    task = db.relationship("Task", backref="category")
    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.name}"

class Task(db.Model):
    """model to store a task data"""

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    hours = db.Column(db.String(150), default="00:00")
    description = db.Column(db.String(200), nullable=False)
    situation = db.Column(db.String(150))
    """:type : str"""

    date_created = db.Column(db.DateTime, default=datetime.now)
    date_finished = db.Column(db.DateTime, default=datetime.now)
    date_initial = db.Column(db.DateTime, default=datetime.now)
    """:type : datetime"""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.description}, content: {self.situation}, content: {self.date_finished}, content: {self.hours}, content: {self.category_id}, content: {self.user_id}"





# routes and handlers.
db.create_all()
def timespent(task):
    s = task.date_initial.strftime("%Y/%m/%d %H:%M:%S")
    t = task.date_finished.strftime("%Y/%m/%d %H:%M:%S")
    f = '%Y/%m/%d %H:%M:%S'
    dif = (datetime.strptime(t, f) - datetime.strptime(s, f))
    return dif


@app.route('/', methods=['GET', 'POST'])
def index():
    """root route"""
    username = ''
    tasks = []
    categorys = []
    categorylist = []
    if "username" in session:

        if request.method == 'POST':
            task = Task(description=request.form['description'],situation=request.form['situation'],hours=request.form['hours'], category_id=request.form['categoryid'], user_id=session["id"])
            if request.form['situation'] == "To do":
                task.date_initial = None
            
            try:
                db.session.add(task)
                db.session.commit()
                return redirect('/')
            except:
                return "Houve um erro, ao inserir a tarefa"
        else:
            username = session["username"]
            tasks = Task.query.filter_by(user_id=session["id"]).all()
            categorylist = Category.query.order_by(Category.name).all()
                
            for category in categorylist:
                for task in tasks:
                    if category.id == task.category_id:
                        categorys.append(category)
                        break
    return render_template('index.html', tasks=tasks, timespent=timespent, categorys=categorys, categorylist=categorylist, username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST" and request.form["username"] != "" and request.form["password"] != "":
        missing = User.query.filter_by(name=request.form["username"].upper()).first()
        if missing is not None:
            if missing.password == request.form["password"]:
                session["username"] = request.form["username"].upper()
                session["id"] = missing.id
                return redirect('/')
            return render_template("login.html", msg="Invalid password")
        return render_template("login.html", msg="Non-existent user")
    return render_template("login.html")  

@app.route("/user", methods=["GET", "POST"])
def user():
    print(request.form)
    if request.method == "POST" and request.form["username"] != "" and request.form["password"] != "":
        missing = User.query.filter_by(name=request.form["username"].upper()).first()
        if missing is None:
            user = User(name=request.form['username'].upper(),password=request.form['password'])
            try:
                db.session.add(user)
                db.session.commit()
                session["username"] = request.form["username"].upper()
                session["id"] = user.id
                return redirect('/')
            except:
                return "Houve um erro, ao inserir a tarefa"
        return render_template("user.html", msg="User is already register!")
    return render_template("user.html")  

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("id", None)
    return redirect(url_for("index"))

@app.route('/delete/<int:id>')
def delete(id):
    """delete a task"""
    if "username" in session:
        task = Task.query.get_or_404(id)
        try:
            db.session.delete(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Houve um erro, ao inserir a tarefa"
    else:
        return "<h1>Not found</h1>"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """update route"""
    if "username" in session:
        task = Task.query.get_or_404(id)
        categorys = Category.query.order_by(Category.id).all()

        if request.method == 'POST':

            if request.form['situation'] == "Done":
                if not task.date_initial:
                    task.date_initial = datetime.now()
                task.date_finished = datetime.now()
            elif request.form['situation'] == "Doing":
                task.date_initial = datetime.now()
                task.date_finished = None
            else:
                task.date_finished = None
                task.date_initial = None
            

            task.description = request.form['description']
            task.situation = request.form['situation']
            task.hours = request.form['hours']
            task.category_id = request.form['categoryid']
            if task.situation == "Done":
                task.date_finished = datetime.now()
            
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "Houve um erro, ao atualizar a tarefa"
        else:
            return render_template('update.html', task=task,categorys=categorys)
    else:
        return "<h1>Not found</h1>"

@app.route('/category', methods=['GET', 'POST'])
def category():
    """root route"""
    if "username" in session:
        if request.method == 'POST':
            category = Category(name=request.form['category'])
            
            try:
                db.session.add(category)
                db.session.commit()
                return redirect('/')
            except:
                return "Houve um erro, ao inserir a tarefa"
        else:
           
            return "<h1>Not found</h1>"
    else:
        return "<h1>Not found</h1>"