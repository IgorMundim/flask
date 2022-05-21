from flask import (
    Blueprint, render_template, request, redirect, session
)
from extensions import db
from models.category import Category

bp = Blueprint('category', __name__)

@bp.route('/category', methods=['GET', 'POST'])
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