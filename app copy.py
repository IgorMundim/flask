import os
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
Bootstrap(app)

# database setup.
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'todo.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# application models.

casts = db.Table(
    "casts", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")), 
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)



class User (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    """:type : str"""
    
    task = db.relationship("Task", backref="user")
    categorys = db.relationship("Category", secondary=casts)

    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.name}, content: {self.password}"


class Category (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    """:type : int"""

    name = db.Column(db.String(200), nullable=False)
    """:type : str"""

    task = db.relationship("Task", backref="category")
    users = db.relationship("User", secondary=casts)
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
    """:type : datetime"""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        """override __repr__ method"""
        return f"Task: #{self.id}, content: {self.description}, content: {self.situation}, content: {self.date_finished}, content: {self.hours}, content: {self.category_id}"





# routes and handlers.
db.create_all()
def timespent(task):
    s = task.date_created.strftime("%Y/%m/%d %H:%M:%S")
    t = task.date_finished.strftime("%Y/%m/%d %H:%M:%S")
    f = '%Y/%m/%d %H:%M:%S'
    dif = (datetime.strptime(t, f) - datetime.strptime(s, f))
    return dif

@app.route('/', methods=['GET', 'POST'])
def index():
    """root route"""
    if request.method == 'POST':
        task = Task(description=request.form['description'],situation=request.form['situation'],hours=request.form['hours'],category_id=request.form['categoryid'])
        
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Houve um erro, ao inserir a tarefa"
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        categorys = Category.query.order_by(Category.name).all()
        return render_template('index.html', tasks=tasks, timespent=timespent, categorys=categorys)
    

@app.route('/delete/<int:id>')
def delete(id):
    """delete a task"""
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Houve um erro, ao inserir a tarefa"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """update route"""
    task = Task.query.get_or_404(id)
    categorys = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
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

@app.route('/category', methods=['GET', 'POST'])
def category():
    """root route"""
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        
        try:
            db.session.add(category)
            db.session.commit()
            return redirect('/')
        except:
            return "Houve um erro, ao inserir a tarefa"
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        categorys = Category.query.order_by(Category.name).all()
        return render_template('index.html', tasks=tasks, timespent=timespent, categorys=categorys)
  