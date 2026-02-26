from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "chave_para_teste"


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


#Rota para criar categorias - faz-se necessária para que possam ser criadas categorias especificas para cada evento
#proteger rota depois - admin
@app.route("/categorias/nova", methods=["GET", "POST"])
def nova_categoria():

    eventos = Evento.query.all()

    if request.method == "POST":
        nome = request.form.get("nome")
        sexo = request.form.get("sexo")
        nivel = request.form.get("nivel")
        evento_id = request.form.get("evento")

        nova = Categoria(
            nome=nome,
            sexo=sexo,
            nivel=nivel,
            evento_id=evento_id
        )

        db.session.add(nova)
        db.session.commit()

        return redirect(url_for("listar_eventos"))

    return render_template("nova_categoria.html", eventos=eventos)





@app.route("/inscricoes/nova", methods=["GET", "POST"])
def nova_inscricao():

    atletas = Atleta.query.all()
    categorias = Categoria.query.all()

    if request.method == "POST":
        atleta1_id = request.form.get("atleta1")
        atleta2_id = request.form.get("atleta2")
        categoria_id = request.form.get("categoria")

        atleta1 = Atleta.query.get(atleta1_id)
        atleta2 = Atleta.query.get(atleta2_id)
        categoria = Categoria.query.get(categoria_id)

        # Não pode ser a mesma pessoa
        if atleta1_id == atleta2_id:
            flash("Selecione atletas diferentes", "error")
            return redirect(url_for("nova_inscricao"))


        # Níveis precisam ser iguais
        if atleta1.nivel.strip().lower() != atleta2.nivel.strip().lower():
            flash("Os atletas devem estar no mesmo nível", "error")
            return redirect(url_for("nova_inscricao"))
 

        # Categoria precisa bater com o nível
        if categoria.nivel.strip().lower() != atleta1.nivel.strip().lower():
            flash("A categoria selecionada deve estar de acordo com nível do atleta", "error")
            return redirect(url_for("nova_inscricao"))
       
        # Sexo precisa bater com a categoria
        if categoria.sexo.strip().lower() != atleta1.sexo.strip().lower() or categoria.sexo.strip().lower() != atleta2.sexo.strip().lower():
            flash("O gênero da categoria não corresponde aos atletas.", "error")       
            return redirect(url_for("nova_inscricao"))



        nova = Inscricao(
            atleta1_id=atleta1_id,
            atleta2_id=atleta2_id,
            categoria_id=categoria_id
        )

        db.session.add(nova)
        db.session.commit()

        flash("Inscrição realizada com sucesso!", "sucess")

        return redirect(url_for("nova_inscricao"))



    return render_template(
        "nova_inscricao.html",
        atletas=atletas,
        categorias=categorias
    )




#Crio a classe/tabela no db Evento
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




class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(20), nullable=False)  
    nivel = db.Column(db.String(20), nullable=False)
    # Cria uma coluna na tabela categoria que só pode armazenar, valores que já existam na coluna id da tabela evento, garantindo a integridade referencial no banco de dados.
    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"), nullable=False)
    evento = db.relationship("Evento", backref="categorias")
    def __repr__(self):
        return f"<Categoria {self.nome}>"



class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atleta1_id = db.Column(db.Integer, db.ForeignKey("atleta.id"), nullable=False)
    atleta2_id = db.Column(db.Integer, db.ForeignKey("atleta.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    # Relacionamentos
    atleta1 = db.relationship("Atleta", foreign_keys=[atleta1_id])
    atleta2 = db.relationship("Atleta", foreign_keys=[atleta2_id])
    categoria = db.relationship("Categoria", backref="inscricoes")
    def __repr__(self):
        return f"<Inscricao {self.id}>"





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