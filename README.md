# 🏐 Liga Eldoradense de Futevôlei — Web System (Flask)

A full-stack web application for managing footvolley tournaments, built with **Python, Flask, and SQLAlchemy**, featuring real-world competition rules and role-based user flows.

---

## 🚀 Overview

The application allows:

- Manage athletes, events, and categories
- Create team registrations with full validation
- Allow athletes to create accounts and register themselves
- Ensure data integrity through strong business rules

The system already serves as a solid foundation for future evolution, such as dashboards, bracket generation, and a future mobile app.

---

## 👤 User Roles

### 🔧 Administrator

- Manages the entire system
- Registers athletes, events, categories, and registrations
- Validates athlete levels
- Ensures competition integrity

### 🏐 Athlete

- Creates their own account
- Logs into the system
- Registers for competitions
- Views their own registrations

---

## ⚙️ Features

### 👤 Athlete Management

- Manual registration by admin or self-registration by athlete
- CPF validation (11 digits and unique)
- Phone number field
- Skill level assignment
- Eldorado do Sul residency flag
- Level validation by admin

### 🔐 Authentication

- Login with email and password
- Strong password requirements
- Session management
- Role-based access control

### 🏟️ Event Management

- Create, edit, and delete events
- Full location data
- Dependency validations before deletion

### 🏆 Category Management

- Categories per event
- Modalities: male, female, and mixed
- Levels: beginner, intermediate, and advanced
- Slot rules: minimum of 4 and even number only

### 🧩 Team Registrations

Business rules implemented:

- Athletes must be different
- Athletes must have the same skill level
- Category must match the team's level
- Modality compatibility is enforced
- Duplicate teams are prevented
- An athlete cannot play twice in the same category
- Registrations are blocked when the category is full
- At least one athlete in the team must be from Eldorado do Sul
- Warning is shown when an athlete level has not yet been validated

### 🏐 Athlete Area

- View personal registrations
- Create new registrations
- Choose a partner
- Separate interface from admin area

---

## 🧠 Data Integrity

The system automatically prevents:

- Changes that would invalidate existing registrations
- Slot reduction below the current number of registrations
- Deletions when related dependencies exist
- Inconsistencies between level, category, and team composition

---

## 🏗️ Architecture

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

---

## 🛠️ Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2
- HTML
- CSS
- JavaScript
- python-dotenv

---

## 🖥️ Running the Project

```bash
git clone https://github.com/your-user/liga-eldoradense-ftv.git
cd liga-eldoradense-ftv

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

# create .env file
SECRET_KEY=your_secret_key

python app.py
```

---

## 🔑 Default Admin

```text
Email: admin@admin.com
Password: Admin@Liga2026!
```

---

## 🔮 Future Improvements

- Dashboard with statistics
- Automatic bracket generation
- Athlete profile editing
- Registration cancellation
- Notifications via WhatsApp or email
- REST API
- Mobile app

---

## 👨‍💻 Author

**Ismael Ienczak**
