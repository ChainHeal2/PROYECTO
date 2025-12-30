"""
Todo lo que tiene que ver con Login y register de usuarios nuevos
"""
import functools
from flask import (Blueprint,flash,g,render_template,url_for,session,redirect,request)
from werkzeug.security import check_password_hash,generate_password_hash
from backend.db import get_db
from backend.func.funciones import campos_limpios,devolver_espacios

bp = Blueprint('auth',__name__)
@bp.route('/',methods = ['GET','POST'])
def index():
    """Pagina de index"""
    return render_template('base.html')
@bp.route('/register',methods = ['GET','POST'])
def register():
    """Pagina de registro"""
    if request.method == 'POST':
        campos = campos_limpios(request.form['usuario'],request.form['password'])
        if campos:
            username = campos[0]
            password = campos[1]
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
                (username,generate_password_hash(password.replace(" ",""))))
                db.commit()
                return redirect(url_for('auth.login'))
        error = 'El largo de ambos campos debe ser mayor a 8'
        flash(error)
    return render_template('auth/register.html')
@bp.route('/login',methods = ['GET','POST'])
def login():
    """Pagina de login"""
    if request.method == 'POST':
        error = None
        campos = campos_limpios(request.form['usuario'],request.form['password'])
        print(campos)
        if campos:
            username = campos[0]
            password = campos[1]
            print(password)
            db ,c = get_db()
            c.execute('select id_user,usuario,password from usuario where usuario = %s',(username,))
            user = c.fetchone()
            if username is None:
                error = 'Usuario o contraseña incorrecta '
            elif not check_password_hash(user['password'],password):
                error = 'Usuario o contraseña incorrecta password '
            if error is None:
                session.clear()
                session['user_id'] = user['id_user']
                session['username'] = user['usuario']
                return redirect(url_for('auth.index'))
        flash(error)
    return render_template('auth/login.html')
@bp.route('/logout')
def logout():
    """Cerrar sesion"""
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
