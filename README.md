🏐 Liga Eldoradense de Futevôlei — Sistema Web (Flask)

Aplicação web desenvolvida em Python + Flask + SQLAlchemy para gerenciamento completo de campeonatos de futevôlei, permitindo administrar atletas, eventos, categorias e inscrições de duplas com regras reais de competição.

O sistema foi projetado para evoluir futuramente para um modelo com usuários e inscrições self-service.

🚀 Funcionalidades:
👤 Atletas

- Cadastro de atletas

- Listagem de atletas

- Edição de dados

- Exclusão com validação de dependência

- Validação de CPF (11 dígitos numéricos e único)

- Proteção contra edição que invalide inscrições existentes

🏟️ Eventos (Etapas):

- Cadastro de eventos com data e local

- Listagem de eventos

- Edição de eventos

- Exclusão com verificação de categorias vinculadas

🏆 Categorias:

- Cadastro de categorias por evento

- Modalidade: Masculino / Feminino / Misto

- Nível: Iniciante / Intermediário / Avançado

- Definição de número de vagas por categoria

  Validação de vagas:

- obrigatório

- número inteiro

- par

- mínimo de 4 duplas

 Listagem com:

- total de inscritos

- vagas restantes

- status (Aberta ou Lotada)

- Edição com validação contra inscrições existentes

- Exclusão bloqueada se houver inscrições

🧩 Inscrições (Duplas):

- Inscrição de duplas em categorias específicas

- Seleção dinâmica de categorias por evento (via API interna)

Regras de negócio implementadas:

✔ atletas devem ser diferentes
✔ atletas devem ter mesmo nível da categoria
✔ compatibilidade com modalidade (masculino, feminino ou misto)
✔ impedir dupla duplicada na mesma categoria
✔ impedir atleta jogar duas vezes na mesma categoria
✔ impedir inscrição quando categoria está lotada
✔ validações completas no backend

🧠 Regras de Integridade Implementadas:

- O sistema protege automaticamente contra inconsistências, incluindo:

- Edição de atleta não pode invalidar inscrições existentes

- Edição de categoria não pode gerar incompatibilidade com duplas já inscritas

- Não é possível reduzir vagas abaixo do número atual de inscritos

- Eventos com categorias vinculadas não podem ser excluídos

- Categorias com inscrições não podem ser excluídas

🏗️ Arquitetura

O projeto foi modularizado usando Blueprints do Flask, separando responsabilidades por domínio:

routes/
├── atletas.py
├── eventos.py
├── categorias.py
└── inscricoes.py

Outros componentes:

- models.py — modelos SQLAlchemy

- extensions.py — inicialização do banco

- templates/ — páginas Jinja2

- .env — variáveis de ambiente

- SQLite como banco de dados

⚙️ Tecnologias Utilizadas

- Python 3

- Flask

- Flask-SQLAlchemy

- SQLite

- Jinja2 Templates

- HTML5 + CSS básico

- python-dotenv

- JavaScript (fetch API para requisições assíncronas)

🖥️ Instalação e Execução:

1. Clonar o repositório:
 git clone https://github.com/seu-usuario/liga-eldoradense-ftv.git
  cd liga-eldoradense-ftv

2. Criar ambiente virtual:
   python -m venv venv

Ativar:

  Windows:
     Bash
       venv\Scripts\activate

  Linux / macOS:
    Bash:
      source venv/bin/activate


3. Instalar dependências:
   Bash
     pip install flask flask-sqlalchemy python-dotenv
  
4. Configurar variáveis de ambiente:
  Criar arquivo .env
  No arquivo .env adicionar:
    SECRET_KEY=sua_chave_secreta_aqui

5. Executar a aplicação:
  Bash
    python app.py


O banco SQLite será criado automaticamente na primeira execução.


📊 Estrutura de Dados (Resumo):

Evento
 └── Categoria (vagas configuráveis)
       └── Inscrição (dupla de atletas)

Atleta
 └── participa de inscrições

 🔮 Melhorias Futuras:

Planejadas para evolução do sistema:

Sistema de autenticação (Admin / Usuário)

Inscrições self-service pelos atletas

Dashboard com estatísticas do campeonato

Controle de status das categorias

Geração automática de chaveamento

Exportação de dados

Interface responsiva

👨‍💻 Autor

Desenvolvido por *Ismael Lenczak*

*Projeto criado para gestão da Liga Eldoradense de Futevôlei e portfólio - sistema real e robusto de gestão de campeonatos de futevôlei.*
