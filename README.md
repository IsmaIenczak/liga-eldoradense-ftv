# 🏐 Liga Eldoradense de Futevôlei

Sistema web full-stack para gestão de torneios de futevôlei, construído com **Python, Flask e SQLAlchemy**, com regras de negócio reais de competição e fluxos de usuário por papel (administrador/atleta).

📖 Leia em: <a href="#-português">Português</a> | <a href="#-english">English</a>

---

<a id="-português"></a>
## 🇧🇷 Português

### 🚀 Visão geral

A aplicação permite:

- Gerenciar atletas, eventos e categorias
- Criar inscrições de duplas com validação completa das regras de negócio
- Permitir que atletas criem contas próprias e se inscrevam sozinhos
- Garantir integridade dos dados através de regras de negócio robustas

O sistema já serve como base sólida para evoluções futuras, como painéis de estatísticas, geração automática de chaveamento e um futuro aplicativo mobile.

### 👤 Papéis de usuário

**🔧 Administrador**
- Gerencia todo o sistema
- Cadastra atletas, eventos, categorias e inscrições
- Valida o nível dos atletas
- Garante a integridade da competição

**🏐 Atleta**
- Cria a própria conta
- Faz login no sistema
- Se inscreve em competições
- Visualiza suas próprias inscrições

### ⚙️ Funcionalidades

**Gestão de Atletas**
- Cadastro manual pelo admin ou autocadastro pelo atleta
- Validação de CPF (11 dígitos e único no sistema)
- Campo de telefone
- Atribuição de nível de habilidade
- Sinalização de residência em Eldorado do Sul
- Validação de nível pelo administrador

**Autenticação**
- Login com email e senha
- Exigência de senha forte
- Gerenciamento de sessão
- Controle de acesso por papel (admin/atleta)

**Gestão de Eventos**
- Criação, edição e exclusão de eventos
- Dados completos de localização
- Validação de dependências antes da exclusão

**Gestão de Categorias**
- Categorias por evento
- Modalidades: masculino, feminino e misto
- Níveis: iniciante, intermediário e avançado
- Regras de vagas: mínimo de 4 e sempre em número par

**Inscrições de Duplas**

Regras de negócio implementadas:
- Os atletas da dupla devem ser diferentes
- Os atletas devem ter o mesmo nível
- A categoria deve ser compatível com o nível da dupla
- Compatibilidade de modalidade é validada (masculino/feminino/misto)
- Duplas duplicadas são bloqueadas
- Um atleta não pode competir duas vezes na mesma categoria
- Inscrições são bloqueadas quando a categoria está lotada
- Pelo menos um atleta da dupla deve ser residente de Eldorado do Sul
- Aviso é exibido quando o nível de um atleta ainda não foi validado

**Área do Atleta**
- Visualização das próprias inscrições
- Criação de novas inscrições
- Escolha de parceiro de dupla
- Interface separada da área administrativa

### 🧠 Integridade de dados

O sistema automaticamente impede:
- Alterações que invalidariam inscrições já existentes
- Redução de vagas abaixo do número de inscrições atuais
- Exclusões quando existem dependências vinculadas
- Inconsistências entre nível, categoria e composição da dupla

### 🏗️ Arquitetura

```bash
routes/
├── auth.py
├── atletas.py
├── eventos.py
├── categorias.py
├── inscricoes.py
└── niveis.py
```

Outros arquivos importantes:
- `models.py` — modelos do banco de dados
- `extensions.py` — inicialização do SQLAlchemy
- `utils.py` — funções utilitárias e decorators
- `templates/` — templates Jinja2

### 🛠️ Stack tecnológica

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- SQLite
- Jinja2
- HTML, CSS, JavaScript
- python-dotenv

### 🖥️ Rodando o projeto

```bash
git clone https://github.com/seu-usuario/liga-eldoradense-ftv.git
cd liga-eldoradense-ftv

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```
SECRET_KEY=sua_chave_secreta_aqui
```

Aplique as migrations para criar o banco de dados:

```bash
flask db upgrade
```

Crie o usuário administrador padrão:

```bash
flask seed-admin
```

Inicie a aplicação:

```bash
flask run
```

### 🔑 Administrador padrão

```
Email: admin@admin.com
Senha: Admin@Liga2026!
```

⚠️ Essas são credenciais de desenvolvimento. Em produção, recomenda-se alterá-las e movê-las para variáveis de ambiente.

### 🔮 Melhorias futuras

- Painel com estatísticas
- Geração automática de chaveamento
- Edição de perfil pelo atleta
- Cancelamento de inscrição
- Notificações via WhatsApp ou email
- API REST
- Aplicativo mobile
- Proteção CSRF nos formulários
- Suíte de testes automatizados
- Paginação nas listagens

### 👨‍💻 Autor


**Ismael Ienczak**





---

<a id="-english"></a>
## 🇬🇧 English

### 🚀 Overview

The application allows:

- Managing athletes, events, and categories
- Creating team registrations with full business-rule validation
- Allowing athletes to create their own accounts and register themselves
- Ensuring data integrity through robust business rules

The system already serves as a solid foundation for future evolution, such as statistics dashboards, automatic bracket generation, and a future mobile app.

### 👤 User Roles

**🔧 Administrator**
- Manages the entire system
- Registers athletes, events, categories, and registrations
- Validates athlete levels
- Ensures competition integrity

**🏐 Athlete**
- Creates their own account
- Logs into the system
- Registers for competitions
- Views their own registrations

### ⚙️ Features

**Athlete Management**
- Manual registration by admin or self-registration by athlete
- CPF validation (11 digits, unique in the system)
- Phone number field
- Skill level assignment
- Eldorado do Sul residency flag
- Level validation by admin

**Authentication**
- Login with email and password
- Strong password requirements
- Session management
- Role-based access control (admin/athlete)

**Event Management**
- Create, edit, and delete events
- Full location data
- Dependency validation before deletion

**Category Management**
- Categories per event
- Modalities: male, female, and mixed
- Levels: beginner, intermediate, and advanced
- Slot rules: minimum of 4, always an even number

**Team Registrations**

Business rules implemented:
- Athletes must be different
- Athletes must share the same skill level
- Category must match the team's level
- Modality compatibility is enforced (male/female/mixed)
- Duplicate teams are prevented
- An athlete cannot play twice in the same category
- Registrations are blocked once the category is full
- At least one athlete in the team must reside in Eldorado do Sul
- A warning is shown when an athlete's level has not yet been validated

**Athlete Area**
- View personal registrations
- Create new registrations
- Choose a partner
- Interface separate from the admin area

### 🧠 Data Integrity

The system automatically prevents:
- Changes that would invalidate existing registrations
- Slot reduction below the current number of registrations
- Deletions when related dependencies exist
- Inconsistencies between level, category, and team composition

### 🏗️ Architecture

```bash
routes/
├── auth.py
├── atletas.py
├── eventos.py
├── categorias.py
├── inscricoes.py
└── niveis.py
```

Other important files:
- `models.py` — database models
- `extensions.py` — SQLAlchemy initialization
- `utils.py` — utility functions and decorators
- `templates/` — Jinja2 templates

### 🛠️ Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- SQLite
- Jinja2
- HTML, CSS, JavaScript
- python-dotenv

### 🖥️ Running the Project

```bash
git clone https://github.com/your-user/liga-eldoradense-ftv.git
cd liga-eldoradense-ftv

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key_here
```

Apply the database migrations:

```bash
flask db upgrade
```

Create the default admin user:

```bash
flask seed-admin
```

Start the application:

```bash
flask run
```

### 🔑 Default Admin

```
Email: admin@admin.com
Password: Admin@Liga2026!
```

⚠️ These are development credentials. In production, they should be changed and moved to environment variables.

### 🔮 Future Improvements

- Statistics dashboard
- Automatic bracket generation
- Athlete profile editing
- Registration cancellation
- Notifications via WhatsApp or email
- REST API
- Mobile app
- CSRF protection on forms
- Automated test suite
- Pagination for listings

### 👨‍💻 Author

**Ismael Ienczak**
