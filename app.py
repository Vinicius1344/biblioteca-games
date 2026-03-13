from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca_jogos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    jogos = Jogo.query.all()
    return render_template('index.html', jogos=jogos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        novo_jogo = Jogo(
            nome=request.form['nome'],
            genero=request.form['genero'],
            plataforma=request.form['plataforma']
        )
        db.session.add(novo_jogo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    jogo = Jogo.query.get_or_404(id)
    if request.method == 'POST':
        jogo.nome = request.form['nome']
        jogo.genero = request.form['genero']
        jogo.plataforma = request.form['plataforma']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', jogo=jogo)

@app.route('/delete/<int:id>')
def delete(id):
    jogo = Jogo.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)