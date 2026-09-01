# HR Manager — Web-Based Human Resources Management System

A modern, web-based HR management system built with Flask and integrated with Anthropic's Claude AI. Developed as a final year internship project (Projet de Fin d'Études) at **Benman Partners**.

---

## Features

- **Authentication** — Secure login and registration with PBKDF2-SHA256 password hashing and session management
- **Employee Management** — Full CRUD operations with avatar initials, role badges, and department assignment
- **Department Management** — Organize company structure with automatic employee headcount display
- **Contract Management** — Issue and track CDI, CDD, Internship, and Freelance contracts with automatic Active/Expired status calculation
- **Project Management & Kanban Board** — Create projects and manage tasks via an interactive drag-and-drop Kanban board (To Do / In Progress / Done)
- **Dashboard** — Real-time overview of key company metrics (employees, departments, active contracts, projects)
- **RaedAI** — Intelligent conversational assistant powered by Anthropic Claude API, answering HR-related questions based on live company data

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-Login, Flask-SQLAlchemy |
| Database | SQLite, SQLAlchemy ORM |
| Frontend | HTML5, Jinja2, CSS3, JavaScript (Vanilla) |
| Drag & Drop | SortableJS |
| Icons | Font Awesome 6 |
| Font | Google Fonts — Inter |
| AI | Anthropic Claude API (claude-sonnet-4-6) |
| Version Control | Git, GitHub |

---

## Architecture

The application follows the **MVC (Model-View-Controller)** architectural pattern:

```
hr-manager/
├── app.py               # Application entry point
├── config.py            # Configuration and environment variables
├── extensions.py        # SQLAlchemy and Flask-Login instances
├── requirements.txt     # Python dependencies
├── .env                 # Secret keys (not committed)
├── .gitignore
├── models/              # Database models (User, Employee, Department, Contract, Project, Task)
├── routes/              # Flask Blueprints (auth, employees, departments, contracts, projects, dashboard)
├── templates/           # Jinja2 HTML templates
│   └── base.html        # Global layout (sidebar, topbar, chatbot widget)
└── static/              # CSS stylesheet and JavaScript files
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/hr-manager.git
cd hr-manager

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the .env file
cp .env.example .env
# Then edit .env and add your keys

# 5. Run the application
python app.py
```

The app will be available at `http://127.0.0.1:5000`

---

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your_secret_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

---

## Default Admin Account

If no admin account exists, the application automatically creates one on first run:

- **Username:** `admin`
- **Password:** `admin123`

> Change these credentials immediately after first login.

---

## RaedAI — How It Works

When the administrator sends a message in the chatbot widget:

1. A JavaScript function fetches a real-time JSON snapshot of all employees, contracts, and projects from the internal `/api/context` endpoint
2. The snapshot is injected into the Claude API system prompt alongside strict behavioral instructions
3. Claude processes the query and returns a concise, natural language response
4. The response is displayed instantly in the chat widget without any page reload

RaedAI is restricted to HR-related questions only and always responds in a short, professional manner.

---

## Security

- Passwords are hashed using **PBKDF2-SHA256** via Werkzeug — never stored in plain text
- All routes are protected with `@login_required`
- Sessions are signed with `SECRET_KEY` to prevent client-side tampering
- Two-layer form validation: client-side (HTML5 + JavaScript) and server-side (Flask routes)
- Sensitive configuration stored in `.env`, excluded from version control via `.gitignore`

---

## Future Improvements

- Role-Based Access Control (RBAC) — HR Manager, Team Lead, Employee roles
- Employee Self-Service Portal
- Advanced Reporting & Analytics with charts
- Email notifications for contract expiration and task deadlines
- File attachments for employee records and contracts
- RaedAI multi-turn conversation support and action execution
- Production deployment with Gunicorn + Nginx + PostgreSQL

---

## Author

**Raed Zheni**
Final Year Internship — Benman Partners

---

## License

This project was developed as part of an academic internship. All rights reserved.
