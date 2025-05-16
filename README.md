# 🌾 Grains Web App

A minimal, modern web platform for managing grain inventory and users, built with **Flask**.

---

## ✨ Features

- 🔐 **Authentication**: Secure login/logout
- 👤 **Role-based Dashboards**: `admin`, `manager`, `employee`
- 👥 **User Management**: Register managers/employees, view all users
- 📦 **Product Management**: Add, update, buy, sell, and list products
- 🧾 **Order Management**: Record buy/sell orders, view order history
- 💾 **Backup**: Download CSV/ZIP backups for products and orders
- 🔑 **Password Reset**: Secure password recovery with verification
- 🗂️ **Clean Structure**: Flask Blueprints, SQLAlchemy models

---

## 🚀 Quick Start

```bash
git clone https://github.com/evilpatrik/Grain_web_app.git
cd grains-web-app

python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt

python app.py
```

Open [http://localhost:5000/login](http://localhost:5000/login) in your browser.

---

## 👤 Default Users

| Role      | Username   | Password     |
|-----------|------------|-------------|
| Admin     | admin      | admin       |
| Manager   | manager    | manager123  |
| Employee  | employee   | employee123 |

---

## 🗂️ Project Structure

```
grains-web-app/
│
├── app.py                  # App entry point
├── blueprints/             # Modular routes (auth, dashboard)
│   ├── auth/
│   └── dashboard/
├── database/               # Models & CRUD logic
├── templates/              # HTML templates
├── static/                 # CSS, images
├── requirements.txt
└── README.md
```

---

## 📚 Usage Highlights

- **Admins**: Register/view managers, backup project, view all users
- **Managers**: Register/view employees, manage products, backup data
- **Employees**: Buy/sell products, add new products, view orders

---

## 🛠️ Tech Stack

- Python, Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-Migrate
- Bootstrap 5 (UI)

---

## 💡 Tips

- Use the built-in backup features to save your data.
- For database changes, use Flask-Migrate to keep your data safe.

---

Enjoy managing your grains! 🌾
