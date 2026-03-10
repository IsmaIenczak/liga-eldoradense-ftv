# Dev Notes — Liga Eldoradense FTV

## Estrutura do Projeto

### app.py
Responsável por:
- Criar a aplicação Flask
- Registrar rotas
- Inicializar extensões

### extensions.py
Arquivo responsável por inicializar extensões do Flask.

Atualmente:
- SQLAlchemy (banco de dados)

### models.py
Define a estrutura do banco de dados.

Models atuais:
- Atleta
- Evento
- Categoria
- Inscricao

---

## Rotas

### atletas.py
CRUD de atletas.

### eventos.py
CRUD de eventos.

### categorias.py
CRUD de categorias.

### inscricoes.py
Gerenciamento de inscrições de duplas.

---

## Observações futuras

- Separar models em arquivos individuais
- Criar API REST
- Criar autenticação de administrador