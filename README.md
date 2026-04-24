# 🛡️ CyberShield — Cybersecurity Incident Tracking System

CyberShield is a full-stack web application designed to help Security 
Operations Center (SOC) teams manage, track, and analyze cybersecurity 
incidents in real time. Built with Python Flask, MySQL, and Bootstrap 5.

---

## 📌 Table of Contents
- [About the Project](#about-the-project)
- [Tech Stack](#tech-stack)
- [Database Design](#database-design)
- [Features](#features)
- [How to Run](#how-to-run)
- [Screenshots](#screenshots)
- [References](#references)

---

## 📖 About the Project
CyberShield was developed as a Database Systems course project at the 
University of North Texas. The goal is to provide a centralized platform 
where security analysts can log incidents, assign team members, track 
threats, and generate analytical reports — all backed by a normalized 
relational MySQL database.

---

## 🛠️ Tech Stack
| Layer      | Technology          |
|------------|---------------------|
| Backend    | Python 3, Flask     |
| Database   | MySQL, PyMySQL      |
| Frontend   | HTML5, CSS3, Bootstrap 5 |
| Templating | Jinja2              |
| Version Control | Git, GitHub   |

---

## 🗄️ Database Design
The database consists of 5 normalized tables in BCNF:

- **INCIDENT** — stores all security incident records
- **USER** — stores analyst profiles and roles
- **THREAT** — stores known cybersecurity threat types
- **INCIDENT_ASSIGNMENT** — bridge table linking incidents to analysts
- **INCIDENT_THREAT** — bridge table linking incidents to threats

---

## ⚙️ Features
- ✅ Add, view, update, and delete security incidents
- ✅ Search incidents by keyword across title, description, and asset
- ✅ Assign analysts to incidents
- ✅ Link threats to incidents
- ✅ View analyst assignment reports via multi-table JOIN queries
- ✅ Generate aggregate reports by severity, status, and threat confidence
- ✅ Fully normalized relational database (BCNF)
- ✅ SQL injection prevention using parameterized queries

---

## 🚀 How to Run

### Prerequisites
- Python 3.x installed
- MySQL Server installed and running
- Git installed

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/cybershield.git
cd cybershield
```

2. **Install dependencies**
```bash
pip install flask pymysql
```

3. **Set up the database**
- Open MySQL and run the provided SQL script:
```bash
mysql -u root -p < cybershield_db.sql
```

4. **Configure database connection**
- Open `app.py` and update the database credentials:
```python
connection = pymysql.connect(
    host='localhost',
    user='your_mysql_username',
    password='your_mysql_password',
    database='cybershield'
)
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
7. http://127.0.0.1:5000
8. ## 📚 References
1. Flask Official Documentation — https://flask.palletsprojects.com
2. PyMySQL Official Documentation — https://pymysql.readthedocs.io
3. MySQL Official Documentation — https://dev.mysql.com/doc/
4. Bootstrap 5 Documentation — https://getbootstrap.com/docs/5.0/
5. W3Schools SQL Reference — https://www.w3schools.com/sql/
