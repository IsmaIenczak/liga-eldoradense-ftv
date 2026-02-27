import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")


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
        modalidade = request.form.get("modalidade")
        nivel = request.form.get("nivel")
        evento_id = request.form.get("evento")

        # Impedir categoria duplicada no mesmo evento (mesma modalidade + nível)
        existente = Categoria.query.filter_by(
            evento_id=int(evento_id),
            modalidade=modalidade,
            nivel=nivel
        ).first()

        if existente:
            flash("Essa categoria já existe neste evento.", "error")
            return redirect(url_for("nova_categoria"))

        nova = Categoria(
        modalidade=modalidade,
        nivel=nivel,
        evento_id=int(evento_id))


        db.session.add(nova)
        db.session.commit()

        flash("Categoria criada com sucesso!", "success")
        return redirect(url_for("listar_eventos"))

    return render_template("nova_categoria.html", eventos=eventos)





@app.route("/api/eventos/<int:evento_id>/categorias")
def api_categorias_por_evento(evento_id):
    categorias = Categoria.query.filter_by(evento_id=evento_id).all()
    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "nivel": c.nivel,
            "modalidade": c.modalidade
        }
        for c in categorias
    ])







@app.route("/inscricoes/nova", methods=["GET", "POST"])
def nova_inscricao():
    atletas = Atleta.query.all()
    eventos = Evento.query.all()

    # Se não houver eventos cadastrados, não faz sentido permitir inscrição
    if not eventos:
        flash("Cadastre um evento antes de criar inscrições.", "error")
        return render_template("nova_inscricao.html", atletas=atletas, eventos=[], categorias=[], selected_evento_id=None)

    # Evento selecionado (GET: via querystring, POST: via form)
    selected_evento_id = request.args.get("evento")
    if selected_evento_id is None:
        selected_evento_id = str(eventos[0].id)  # default: primeiro evento

    categorias = Categoria.query.filter_by(evento_id=int(selected_evento_id)).all()

    if request.method == "POST":
        evento_id = request.form.get("evento")
        atleta1_id = request.form.get("atleta1")
        atleta2_id = request.form.get("atleta2")
        categoria_id = request.form.get("categoria")

        atleta1 = Atleta.query.get(atleta1_id)
        atleta2 = Atleta.query.get(atleta2_id)
        categoria = Categoria.query.get(categoria_id)

        if not atleta1 or not atleta2 or not categoria or not evento_id:
            flash("Dados inválidos.", "error")
            return redirect(url_for("nova_inscricao"))

        # Garante consistência: categoria precisa pertencer ao evento selecionado
        if categoria.evento_id != int(evento_id):
            flash("A categoria selecionada não pertence ao evento escolhido.", "error")
            return redirect(url_for("nova_inscricao", evento=evento_id))

        # Não pode ser a mesma pessoa
        if atleta1_id == atleta2_id:
            flash("Selecione atletas diferentes", "error")
            return redirect(url_for("nova_inscricao", evento=evento_id))

        # Níveis precisam ser iguais
        if atleta1.nivel.strip().lower() != atleta2.nivel.strip().lower():
            flash("Os atletas devem estar no mesmo nível", "error")
            return redirect(url_for("nova_inscricao", evento=evento_id))

        # Categoria precisa bater com o nível
        if categoria.nivel.strip().lower() != atleta1.nivel.strip().lower():
            flash("A categoria selecionada deve estar de acordo com nível do atleta", "error")
            return redirect(url_for("nova_inscricao", evento=evento_id))

        # Sexo precisa bater com a categoria (modalidade)
        modalidade = (categoria.modalidade or "").strip().lower()
        sexo1 = atleta1.sexo.strip().lower()
        sexo2 = atleta2.sexo.strip().lower()

        if modalidade == "masculino":
            if sexo1 != "masculino" or sexo2 != "masculino":
                flash("Essa categoria aceita apenas atletas do sexo masculino.", "error")
                return redirect(url_for("nova_inscricao", evento=evento_id))

        elif modalidade == "feminino":
            if sexo1 != "feminino" or sexo2 != "feminino":
                flash("Essa categoria aceita apenas atletas do sexo feminino.", "error")
                return redirect(url_for("nova_inscricao", evento=evento_id))

        elif modalidade == "misto":
            if sexo1 == sexo2:
                flash("Categoria mista requer um atleta do sexo masculino e um atleta do sexo feminino.", "error")
                return redirect(url_for("nova_inscricao", evento=evento_id))

        # Filtra inscrições só daquela categoria
        inscricoes_categoria = Inscricao.query.filter_by(categoria_id=categoria_id).all()

        # Impedir dupla duplicada na mesma categoria
        for inscricao in inscricoes_categoria:
            atletas_existentes = {inscricao.atleta1_id, inscricao.atleta2_id}
            novos_atletas = {int(atleta1_id), int(atleta2_id)}
            if atletas_existentes == novos_atletas:
                flash("Essa dupla já está inscrita nesta categoria.", "error")
                return redirect(url_for("nova_inscricao", evento=evento_id))

        # Impedir atleta jogar duas vezes na mesma categoria
        for inscricao in inscricoes_categoria:
            if (
                int(atleta1_id) in [inscricao.atleta1_id, inscricao.atleta2_id] or
                int(atleta2_id) in [inscricao.atleta1_id, inscricao.atleta2_id]
            ):
                flash("Um dos atletas já está inscrito para competir nesta categoria.", "error")
                return redirect(url_for("nova_inscricao", evento=evento_id))

        nova = Inscricao(
            atleta1_id=atleta1_id,
            atleta2_id=atleta2_id,
            categoria_id=categoria_id
        )

        db.session.add(nova)
        db.session.commit()

        flash("Inscrição realizada com sucesso!", "success")
        return redirect(url_for("nova_inscricao", evento=evento_id))

    return render_template(
        "nova_inscricao.html",
        atletas=atletas,
        eventos=eventos,
        categorias=categorias,
        selected_evento_id=int(selected_evento_id)
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
    modalidade = db.Column(db.String(20), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)

    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"), nullable=False)
    evento = db.relationship("Evento", backref="categorias")

    # Nome calculado dinamicamente
    @property
    def nome(self):
        return f"{self.modalidade} {self.nivel}"

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