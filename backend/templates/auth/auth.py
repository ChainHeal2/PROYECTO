"""
Todo lo que tiene que ver con Login y register de usuarios nuevos
"""
from flask import (Blueprint,flash,g,render_template,url_for,session,redirect,request)
from werkzeug.security import check_password_hash,generate_password_hash
from backend.db import get_db
import functools

bp = Blueprint('auth',__name__)
@bp.route('/',methods = ['GET','POST'])
def index():
    """Pagina de index"""
    return render_template('base.html')
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
            error = 'El usuario ya se encuentra registrado'
        if error is None:
            c.execute('insert into usuario (usuario,password) values (%s,%s)',
            (username,generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
        print("fuera de todos los if")
        flash(error)
    return render_template('auth/register.html')
@bp.route('/login',methods = ['GET','POST'])
def login():
    """Pagina de login"""
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        db ,c = get_db()
        error = None
        c.execute('select * from usuario where usuario = %s',(username,))
        user = c.fetchone()
        if user is None:
            error = 'Usuario o contraseña incorrecta '
        elif not check_password_hash(user['password'],password):
            error = 'Usuario o contraseña incorrecta '
        if error is None:
            session.clear()
            session['user_id'] = user['id_user']
            session['username'] = user['usuario']
            print(session)
            print(username)
            return redirect(url_for('auth.index'))
    return render_template('auth/login.html')
@bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.pop(user_id,None)
    session.clear()
    return redirect(url_for('auth.login'))
@bp.before_app_request
def load_logged_in_user():
    """antes de cada peticion del usuario"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user= None
    else:
        db,c = get_db()
        c.execute('select * from usuario where id_user = %s',(user_id,))
        g.user= c.fetchone()
def loguin_required(view):
    """protege las rutas"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
