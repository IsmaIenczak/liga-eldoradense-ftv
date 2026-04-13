🏐 Liga Eldoradense de Futevôlei — Sistema Web (Flask)

Sistema web completo para gerenciamento de campeonatos de futevôlei, desenvolvido com Python, Flask e SQLAlchemy, com regras reais de competição e fluxo de uso para administradores e atletas.

🚀 Visão Geral

A aplicação permite:

Gerenciar atletas, eventos e categorias
Realizar inscrições de duplas com validações completas
Permitir que atletas criem contas e se inscrevam nos campeonatos
Garantir integridade de dados com regras de negócio robustas

O sistema já funciona como uma base sólida para evolução futura (dashboard, chaveamento, app mobile, etc.).

👤 Tipos de Usuário
🔧 Administrador
Gerencia todo o sistema
Cadastra atletas, eventos, categorias e inscrições
Valida nível dos atletas
Controla integridade das competições
🏐 Atleta
Cria conta própria
Faz login no sistema
Realiza suas próprias inscrições
Visualiza suas participações
⚙️ Funcionalidades
👤 Atletas
Cadastro manual (admin) ou auto cadastro (atleta)
Validação de CPF (único e com 11 dígitos)
Campo de telefone
Definição de nível
Indicação de residência em Eldorado do Sul
Validação de nível pelo admin
🔐 Autenticação
Login com email e senha
Senha com critérios de segurança:
mínimo 8 caracteres
1 letra maiúscula
1 número
1 caractere especial
Sessão com expiração
Controle de acesso por tipo de usuário
🏟️ Eventos
Cadastro de eventos com:
nome
data
local completo
Edição e exclusão (com validação de dependências)
🏆 Categorias
Criadas por evento
Definições:
modalidade: masculino, feminino ou misto
nível: iniciante, intermediário ou avançado
número de vagas (par e mínimo de 4)
Regras:
Não permite duplicidade de categoria no mesmo evento
Não permite edição que invalide inscrições
Não permite reduzir vagas abaixo do número de inscritos
🧩 Inscrições (Duplas)
Realizadas por admin ou pelo próprio atleta
Seleção dinâmica por evento
Regras implementadas:

✔ atletas devem ser diferentes
✔ atletas devem ter mesmo nível
✔ categoria deve corresponder ao nível
✔ compatibilidade com modalidade (M/F/Misto)
✔ impedir dupla duplicada
✔ impedir atleta em mais de uma dupla na mesma categoria
✔ impedir inscrição em categoria lotada
✔ pelo menos 1 atleta deve ser residente de Eldorado do Sul
✔ aviso quando nível do atleta ainda não foi validado

📊 Área do Atleta
Visualização das próprias inscrições
Criação de nova inscrição escolhendo parceiro
Interface separada da área administrativa
🧠 Regras de Integridade

O sistema protege automaticamente contra inconsistências:

Alteração de atleta não pode invalidar inscrições existentes
Alteração de categoria respeita duplas já inscritas
Exclusões bloqueadas quando há vínculos
Validações completas no backend (não dependem do front-end)
🏗️ Arquitetura

Projeto organizado com Blueprints do Flask:

  routes/
├── atletas.py
├── eventos.py
├── categorias.py
├── inscricoes.py
├── niveis.py
└── auth.py


Outros componentes:

models.py → modelos do banco
extensions.py → configuração do SQLAlchemy
utils.py → utilitários (auth, validações)
templates/ → páginas HTML (Jinja2)
.env → variáveis de ambiente

⚙️ Tecnologias Utilizadas
Python 3
Flask
Flask-SQLAlchemy
SQLite
Jinja2
HTML5 + CSS
JavaScript (Fetch API)
python-dotenv
🖥️ Instalação
1. Clonar repositório:
 bash:
    git clone https://github.com/seu-usuario/liga-eldoradense-ftv.git
    cd liga-eldoradense-ftv

2. Criar ambiente virtual:
  python -m venv venv


Ativar:

Windows:
  venv\Scripts\activate

Linux/macOS
  source venv/bin/activate


3. Instalar dependências:
  bash:
  pip install -r requirements.txt


4. Configurar variáveis de ambiente:

  Criar arquivo .env: 
    SECRET_KEY=sua_chave_secreta_aqui


5. Executar aplicação
  bash:
    python app.py


🔑 Acesso inicial

Um administrador padrão é criado automaticamente:

Email: admin@admin.com
Senha: Admin@Liga2026!


🗄️ Banco de Dados
  SQLite (liga.db)
  Criado automaticamente na primeira execução


📊 Estrutura de Dados (Resumo)
Evento
 └── Categoria
       └── Inscrição (dupla)

Atleta
 └── Usuario (login)


 🔮 Próximas Evoluções
Dashboard com estatísticas
Sistema de chaveamento automático
Cancelamento de inscrição pelo atleta em tempo hábil
Edição de perfil do atleta
Notificações (WhatsApp / email)
Interface responsiva
API para app mobile
Aplicativo mobile (Flutter ou React Native)



👨‍💻 Autor

Desenvolvido por Ismael Ienczak

Projeto real para gestão da Liga Eldoradense de Futevôlei, utilizado como sistema funcional e portfólio profissional.