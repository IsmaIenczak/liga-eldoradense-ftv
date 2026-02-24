from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Configuro o banco de dados do app atraves do metodo config do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Crio o banco de dados para o app através da classe SQLAlchemy
db = SQLAlchemy(app)


class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    cpf = db.Column(db.String(11), nullable=False, unique=True)

    sexo = db.Column(db.String(10), nullable=False)

    nivel = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Atleta {self.nome}>"



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



#defino a rota para criação de cadastros
@app.route("/atletas/novo", methods=["GET", "POST"])
def cadastrar_atleta():
    
    if request.method == "POST":

        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        sexo = request.form.get("sexo")
        nivel = request.form.get("nivel")

        #Validação de formato CPF
        if not cpf.isdigit() or len(cpf) != 11:
            return render_template(
                "novo_atleta.html",
                erro="CPF deve conter exatamente 11 números."
            )
        
        #Verificação de duplicidade CPF
        cpf_existente = Atleta.query.filter_by(cpf=cpf).first()
        if cpf_existente:
            return render_template(
                "novo_atleta.html",
                erro="CPF já cadastrado no sistema."
            )

        novo_atleta = Atleta(
            nome=nome,
            cpf=cpf,
            sexo=sexo,
            nivel=nivel
        )


        db.session.add(novo_atleta)
        db.session.commit()

        return redirect(url_for("listar_atletas"))
    
    return render_template("novo_atleta.html")




#Crio a classe Evento
from datetime import datetime
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)

    arena = db.Column(db.String(100), nullable=False)
    rua = db.Column(db.String(150), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"<Evento {self.nome}>"   

#defino a rota para mostrar os eventos vigentes
@app.route("/eventos")
def listar_eventos():
    eventos = Evento.query.all()
    return render_template("eventos.html", eventos=eventos)


#Defino a rota para cadastar eventos - Adicionar proteção à essa rota futuramente - somente admin
@app.route("/eventos/novo", methods=["GET", "POST"])
def cadastrar_evento():

    if request.method == "POST":
        nome = request.form.get("nome")
        data_str = request.form.get("data")
        arena = request.form.get("arena")
        rua = request.form.get("rua")
        cidade = request.form.get("cidade")
        cep = request.form.get("cep")
        numero = request.form.get("numero")

        data = datetime.strptime(data_str, "%Y-%m-%d").date()

        novo_evento = Evento(
            nome=nome,
            data=data,
            arena = arena,
            rua = rua,
            cidade = cidade,
            cep = cep,
            numero = numero,

        )

        db.session.add(novo_evento)
        db.session.commit()

        return redirect(url_for("listar_eventos"))

    return render_template("novo_evento.html")








# Ativa o contexto da aplicação Flask para permitir acesso às configurações
# e cria no banco de dados todas as tabelas definidas pelas classes
# que herdam de db.Model (caso ainda não existam)
with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)