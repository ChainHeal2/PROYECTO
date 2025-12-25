"""
Todo lo que tiene que ver con Login y register de usuarios nuevos
"""
from flask import (Blueprint,flash,g,render_template,url_for,session,redirect,request)
from werkzeug.security import check_password_hash,generate_password_hash
from backend.db import get_db

bp = Blueprint('auth',__name__)
@bp.route('/',methods = ['GET','POST'])
@bp.route('/register',methods = ['GET','POST'])
def register():
    """Pagina de registro"""
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        db ,c = get_db()
        error = None
        c.execute('select id_user from usuario where usuario = %s',(username,))
        if not username:
            error ='Username es requerido'
        if not password:
            error = 'password es requerido'
        elif c.fetchone() is not None:
            error = f'Usuario {username} se encuentra registrado.'
        if error is None:
            c.execute('insert into usuario (usuario,password) values (%s,%s)',
            (username,generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')
@bp.route('/login',methods = ['GET','POST'])
def login():
    """Pagina de login"""
    return render_template('auth/login.html')