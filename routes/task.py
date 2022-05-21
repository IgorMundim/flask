from flask import (
    Blueprint, render_template, request, redirect, session
)
from datetime import datetime

from extensions import db

from models.task import Task
from models.category import Category

bp = Blueprint('task', __name__)

# @routes_blueprint.route('/')
# def index():
#     """root route"""
#     return "aki"

def timespent(task):
    s = task.date_initial.strftime("%Y/%m/%d %H:%M:%S")
    t = task.date_finished.strftime("%Y/%m/%d %H:%M:%S")
    f = '%Y/%m/%d %H:%M:%S'
    dif = (datetime.strptime(t, f) - datetime.strptime(s, f))
    return dif


@bp.route('/', methods=['GET', 'POST'])
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

@bp.route('/delete/<int:id>')
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


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
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

