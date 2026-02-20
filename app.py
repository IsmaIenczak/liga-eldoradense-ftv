from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Configuro o banco de dados do app atraves do metodo config do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Crio o banco de dados para o app através da classe SQLAlchemy
db = SQLAlchemy(app)


#criação da classe atleta herdando a classe db.model do SQLAlchemy, facilitando a crianção da tabela de banco de dados
class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    modalidade = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Atleta {self.nome}>'



@app.route("/")
def home():
    nome_liga = "Liga Eldoradense de Futevôlei"
    proxima_etapa = "Etapa verão 2026"

    return render_template("index.html")


#defino a rota "atletas" onde serão listados todos atletas cadastrados no DB.
@app.route("/atletas")
def listar_atletas():
    atletas = Atleta.query.all() 
    #Executa uma query na tabela representada pela classe Atleta, retornando todos os registros como uma lista de objetos.
    return render_template("atletas.html", atletas = atletas) 
    # Envia a lista de atletas para o template, tornando-a disponível no front-end.




# Ativa o contexto da aplicação Flask para permitir acesso às configurações
# e cria no banco de dados todas as tabelas definidas pelas classes
# que herdam de db.Model (caso ainda não existam)
with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)