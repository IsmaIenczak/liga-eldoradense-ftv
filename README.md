# 🏐 Liga Eldoradense de Futevôlei – Sistema Web com Flask

Aplicação web desenvolvida com Flask para gerenciamento de atletas e etapas da Liga Eldoradense de Futevôlei, utilizando arquitetura baseada em templates (Jinja2) e integração com banco de dados relacional via SQLAlchemy.

---

## 🚀 Tecnologias utilizadas

- Python  
- Flask  
- SQLAlchemy  
- SQLite  
- HTML5  
- Jinja2  

---

## 📌 Funcionalidades atuais

- Estrutura base do projeto
- Configuração de banco de dados com SQLAlchemy
- Criação do modelo `Atleta`
- Template base com herança (Jinja2)
- Servidor Flask rodando em modo desenvolvimento

---

## 📂 Estrutura do projeto


liga-eldoradense-ftv/
│
├── app.py
├── templates/
├── static/
├── instance/ (não versionado)
├── venv/ (não versionado)
├── requirements.txt
└── README.md


---

## ⚙️ Como rodar o projeto localmente

1. Clone o repositório:


git clone https://github.com/seu-usuario/liga-eldoradense-ftv.git


2. Crie o ambiente virtual:


python -m venv venv


3. Ative o ambiente virtual:

Windows:

venv\Scripts\activate


4. Instale as dependências:


pip install -r requirements.txt


5. Execute o projeto:


python app.py


O servidor estará disponível em:


http://127.0.0.1:5000


---

## 🔐 Boas práticas adotadas

- Uso de ambiente virtual (venv)
- Arquivos sensíveis ignorados via `.gitignore`
- Banco de dados não versionado
- Estrutura preparada para expansão com CRUD completo
- Separação entre lógica de backend e templates

---

## 🚧 Projeto em desenvolvimento

Este projeto faz parte do meu aprendizado em desenvolvimento web com Flask e será expandido com funcionalidades como:

- CRUD completo de atletas
- Validação de dados
- Melhorias de segurança
- Organização modular do código
- Autenticação de usuários (futuro)

---

Desenvolvido por **Ismael Ribeiro**