from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

# Formulário para login
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

# Formulário para agendar consulta
class AgendarConsultaForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    date = StringField('Data da Consulta', validators=[DataRequired()])
    submit = SubmitField('Agendar Consulta')

# Decorator para proteger rotas
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Preserva o nome da função original
    return wrap

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title="Página Inicial")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Conectar ao banco e verificar usuário
        username = form.username.data
        password = form.password.data

        import sqlite3
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            # Login bem-sucedido
            flash(f'Bem-vindo, {username}!', 'success')
            session['logged_in'] = True
            session['username'] = username  # Opcional: salvar o usuário na sessão
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/agendar_consultas', methods=['GET', 'POST'])
@login_required
def agendar_consultas():
    form = AgendarConsultaForm()
    if form.validate_on_submit():
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('agendar_consultas.html', title="Agendar Consultas", form=form)

@app.route('/sessao_musicoterapia', methods=['GET'])
@login_required
def sessao_musicoterapia():
    return render_template('sessao_musicoterapia.html', title="Sessão de Musicoterapia")

@app.route('/resultados_consultas', methods=['GET'])
@login_required
def resultados_consultas():
    minutos_ouvidos = 120  # Exemplo de valor
    exercicios_realizados = 5  # Exemplo de valor
    consultas_realizadas = 10  # Exemplo de valor
    horas_sono = 8  # Exemplo de valor
    return render_template('resultados_consultas.html', 
                           title="Resultados de Consultas", 
                           minutos_ouvidos=minutos_ouvidos, 
                           exercicios_realizados=exercicios_realizados,
                           consultas_realizadas=consultas_realizadas, 
                           horas_sono=horas_sono)

@app.route('/playlist_musicas', methods=['GET'])
@login_required
def playlist_musicas():
    return render_template('playlist_musicas.html', title="Playlist de Músicas")

@app.route('/exercicios', methods=['GET'])
@login_required
def exercicios():
    return render_template('exercicios.html', title="Exercícios")

if __name__ == '__main__':
    app.run(debug=True)
