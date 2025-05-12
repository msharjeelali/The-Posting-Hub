# 📝 The Posting Hub – A Developer-Focused Blog Platform

A full-stack Django-based web application that enables developers to share posts, interact through likes and comments, and engage with a vibrant coding community.

![Built With](https://img.shields.io/badge/stack-Django%20%26%20HTML%2FCSS-blue.svg)  
![Status](https://img.shields.io/badge/status-Active-lightgrey.svg)

---

## ✨ Overview

The Posting Hub is a community blogging platform tailored for developers. It allows users to register, create and manage posts, like and comment on content, and report inappropriate users — all within a clean and modern UI. The app aims to foster collaborative knowledge sharing among coders.

---

## 🚀 Features

- 🔐 User Authentication – Secure signup, login, and logout.
- 📝 Post Creation – Write, edit, and delete blog posts with rich formatting.
- ❤️ Likes and 💬 Comments – Engage with other posts and foster discussion.
- 🧾 User Dashboard – View your own posts, likes, and comments in one place.
- 👤 Profile View – Browse public user profiles.
- 🚩 Report Users – Report inappropriate behavior with modal submission form.
- 🎨 Glassmorphism UI – Modern and sleek front-end with CSS effects.

---

## 🏗️ Tech Stack

- 💻 Frontend: HTML5, CSS3, JavaScript
- ⚙️ Backend: Python, Django
- 🗃️ Database: SQLite (default Django DB, switchable)
- 🧰 Tools: Django Admin, Bootstrap (optional), Git

---

## 📂 Project Structure

```bash
The-Posting-Hub/
│
├── thepostinghub/             # Main Django project settings
│
├── core/                      # Core app (posts, users, profiles)
│   ├── models.py              # Post, Comment, Like, Report, Profile models
│   ├── views.py               # Handles all business logic and routing
│   ├── forms.py               # Django forms for login, signup, posts
│   ├── urls.py                # App URL configurations
│   ├── templates/             # HTML templates (login, signup, dashboard, etc.)
│   └── static/                # CSS, JS, and image assets
│
├── templates/                 # Base templates
│   └── base.html              # Root HTML layout with navbars
│
├── static/                    # Global static files
│   ├── css/                   # Stylesheets (glassmorphism.css, etc.)
│   ├── js/                    # Frontend interactions
│
├── db.sqlite3                 # SQLite Database
└── manage.py                  # Django entry point
```

---

## 🧪 How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/msharjeelali/The-Posting-Hub.git
cd The-Posting-Hub
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

5. Open your browser and go to http://127.0.0.1:8000/

---

## 🛡️ Security & Reporting

- All posts and actions are authenticated and tied to a user session.
- The report modal allows users to submit reasons and details.
- Admin moderation can be extended from Django Admin.