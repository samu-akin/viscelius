from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title="Página Inicial")

@app.route('/agendar_consultas', methods=['GET', 'POST'])
def agendar_consultas():
    form = AgendarConsultaForm()
    if form.validate_on_submit():
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('agendar_consultas.html', title="Agendar Consultas", form=form)

@app.route('/sessao_musicoterapia', methods=['GET'])
def sessao_musicoterapia():
    return render_template('sessao_musicoterapia.html', title="Sessão de Musicoterapia")

@app.route('/resultados_consultas', methods=['GET'])
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
def playlist_musicas():
    return render_template('playlist_musicas.html', title="Playlist de Músicas")

@app.route('/exercicios', methods=['GET'])
def exercicios():
    return render_template('exercicios.html', title="Exercícios")

if __name__ == '__main__':
    app.run(debug=True)
