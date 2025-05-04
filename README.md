# 🌾 Grains Web App

A simple web-based grain management platform built using **Flask**, with role-based dashboards for **Admins**, **Managers**, and **Employees**.

---

## 📁 Features

- 🔐 User Authentication (Login / Logout)
- 👤 Role-based Access Control (`admin`, `manager`, `employee`)
- 🧑‍💼 Admin: View all users
- 📦 Manager & Employee: Custom dashboards
- 🔑 Forgot Password with a secret question (favorite pet)
- ✅ Clean project structure using Flask Blueprints

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/grains-web-app.git
cd grains-web-app

///////////////////////////////

2. Create & Activate Virtual Environment

python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

 _________________________
|________________________|

3. Install Dependencies

pip install -r requirements.txt


4. Run the app
run app.py

Open your browser and go to:
👉 http://localhost:5000/login



👤 Default Admin Login
Username	Password
---------------------
admin	    admin



🗂️ Project Structure

grains-web-app/
│
├── app.py                 # App factory and entry point
├── blueprints/            # Modularized routes
│   ├── auth/              # Auth routes (login, forgot, etc.)
│   └── dashboard/         # Role-based dashboards
│
├── models.py              # SQLAlchemy models
├── templates/             # Jinja2 HTML templates
│
├── static/                # CSS, JS, images (if needed)
├── requirements.txt       # Python dependencies
└── README.md              # You're here!
