# 🏐 Liga Eldoradense de Futevôlei

Sistema web desenvolvido em Flask para gerenciamento da Liga Eldoradense de Futevôlei.

O objetivo do projeto é permitir o cadastro e organização de:

- Atletas
- Eventos (etapas)
- Categorias por evento
- Inscrições de duplas por categoria

---

## 🚀 Tecnologias utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML (Jinja2 Templates)
- python-dotenv

---

## 📌 Funcionalidades atuais

### 👤 Atletas
- Cadastro de atletas
- Validação de CPF (11 dígitos numéricos)
- Impede CPF duplicado

### 🏟 Eventos
- Cadastro de eventos (etapas)
- Informações de local e data

### 🏆 Categorias
- Criadas por evento
- Definidas por:
  - Modalidade (Masculino, Feminino, Misto)
  - Nível (Iniciante, Intermediário, Avançado)
- Impede categoria duplicada no mesmo evento
- Nome da categoria é gerado dinamicamente (Modalidade + Nível)

### 📝 Inscrições
- Inscrição de dupla por categoria
- Validações implementadas:
  - Atletas devem ser diferentes
  - Devem ter o mesmo nível
  - Categoria deve corresponder ao nível da dupla
  - Modalidade deve corresponder ao sexo dos atletas
  - Impede dupla duplicada na mesma categoria
  - Impede atleta inscrito duas vezes na mesma categoria
  - Categoria deve pertencer ao evento selecionado

---

## 🔄 Fluxo recomendado de uso

1. Criar um evento
2. Criar categorias vinculadas ao evento
3. Cadastrar atletas
4. Realizar inscrições

### Atletas devem ser previamente cadastrados na rota global

---

## ⚙️ Como rodar localmente

1) - Clonar o repositório
bash
git clone https://github.com/IsmaIenczak/liga-eldoradense-ftv.git
cd liga-eldoradense-ftv

--------------------------------------------------------------------------------

2) Criar e ativar ambiente virtual:

python -m venv venv

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

--------------------------------------------------------------------------------

3) Instalar dependências
pip install -r requirements.txt

--------------------------------------------------------------------------------


4) Criar arquivo .env

⚠️ O arquivo .env não deve ser versionado.

Crie um arquivo chamado .env na raiz do projeto:

SECRET_KEY=sua-chave-super-secreta-aqui

Se não existir SECRET_KEY, o app usa um fallback de desenvolvimento (dev-key).
Para produção, configure uma chave forte (e nunca versione o .env).

--------------------------------------------------------------------------------

5) Executar
python app.py

Acesse:

http://127.0.0.1:5000

🗄️ Banco de dados

Banco local em SQLite

Arquivo: liga.db

As tabelas são criadas automaticamente no start via db.create_all().

--------------------------------------------------------------------------------

📁 Estrutura do projeto:

liga-eldoradense-ftv/
│
├── app.py
├── requirements.txt
├── README.md
├── .env (não versionado)
│
└── templates/
    ├── base.html
    ├── novo_atleta.html
    ├── novo_evento.html
    ├── nova_categoria.html
    ├── nova_inscricao.html

--------------------------------------------------------------------------------


🛣️ Próximos passos (ideias)

- Modularização do sistema

- CRUD completo (editar/excluir) para atletas, eventos, categorias e inscrições

- Painel administrativo (proteção de rotas)

- Melhorias de UX no front (ex.: selects dependentes e listagens melhores)

- Relatórios por evento/categoria (ex.: lista de inscritos por categoria)

- Seed de dados para desenvolvimento

    👤 Autor

    > Desenvolvido por ***Ismael Ribeiro.***