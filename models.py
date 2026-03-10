from extensions import db


class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    sexo = db.Column(db.String(10), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Atleta {self.nome}>"


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

    atleta1 = db.relationship("Atleta", foreign_keys=[atleta1_id])
    atleta2 = db.relationship("Atleta", foreign_keys=[atleta2_id])
    categoria = db.relationship("Categoria", backref="inscricoes")

    def __repr__(self):
        return f"<Inscricao {self.id}>"