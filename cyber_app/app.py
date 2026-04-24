from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # ← your MySQL password
        database="cyber_incident_db"
    )

# ── DASHBOARD ──
@app.route('/')
def index():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM INCIDENT")
    stats = cur.fetchone()
    cur.execute("SELECT COUNT(*) AS open_count FROM INCIDENT WHERE status='Open'")
    open_stats = cur.fetchone()
    cur.execute("SELECT COUNT(*) AS total FROM THREAT")
    threat_count = cur.fetchone()
    cur.execute("SELECT COUNT(*) AS total FROM USER")
    user_count = cur.fetchone()
    cur.execute("SELECT * FROM INCIDENT ORDER BY reported_time DESC LIMIT 5")
    recent = cur.fetchall()
    db.close()
    return render_template('index.html',
                           stats=stats,
                           open_stats=open_stats,
                           threat_count=threat_count,
                           user_count=user_count,
                           recent=recent)

# ── INCIDENTS ──
@app.route('/incidents')
def incidents():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM INCIDENT ORDER BY reported_time DESC")
    rows = cur.fetchall()
    db.close()
    return render_template('incidents.html', incidents=rows)

@app.route('/incidents/add', methods=['GET', 'POST'])
def add_incident():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO INCIDENT (title, description, severity, category, status, affected_asset)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            request.form['title'],
            request.form['description'],
            request.form['severity'],
            request.form['category'],
            request.form['status'],
            request.form['affected_asset']
        ))
        db.commit()
        db.close()
        return redirect(url_for('incidents'))
    return render_template('add_incident.html')

@app.route('/incidents/edit/<int:id>', methods=['GET', 'POST'])
def edit_incident(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    if request.method == 'POST':
        cur.execute("""
            UPDATE INCIDENT
            SET title=%s, description=%s, severity=%s,
                category=%s, status=%s, affected_asset=%s
            WHERE incident_id=%s
        """, (
            request.form['title'],
            request.form['description'],
            request.form['severity'],
            request.form['category'],
            request.form['status'],
            request.form['affected_asset'],
            id
        ))
        db.commit()
        db.close()
        return redirect(url_for('incidents'))
    cur.execute("SELECT * FROM INCIDENT WHERE incident_id = %s", (id,))
    incident = cur.fetchone()
    db.close()
    return render_template('edit_incident.html', incident=incident)

@app.route('/incidents/delete/<int:id>')
def delete_incident(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM INCIDENT_THREAT WHERE incident_id = %s", (id,))
    cur.execute("DELETE FROM INCIDENT_ASSIGNMENT WHERE incident_id = %s", (id,))
    cur.execute("DELETE FROM INCIDENT WHERE incident_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('incidents'))

# ── USERS ──
@app.route('/users')
def users():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM USER")
    rows = cur.fetchall()
    db.close()
    return render_template('users.html', users=rows)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO USER (name, email, role, department)
            VALUES (%s, %s, %s, %s)
        """, (
            request.form['name'],
            request.form['email'],
            request.form['role'],
            request.form['department']
        ))
        db.commit()
        db.close()
        return redirect(url_for('users'))
    return render_template('add_user.html')

# ── THREATS ──
@app.route('/threats')
def threats():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM THREAT")
    rows = cur.fetchall()
    db.close()
    return render_template('threats.html', threats=rows)

# ── SEARCH ──
@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM INCIDENT
            WHERE title LIKE %s OR description LIKE %s OR affected_asset LIKE %s
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        results = cur.fetchall()
        db.close()
    return render_template('search.html', results=results, query=query)

# ── ASSIGNMENTS (JOIN) ──
@app.route('/assignments')
def assignments():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT I.title, I.severity, U.name, U.department, A.role_on_incident
        FROM INCIDENT_ASSIGNMENT A
        JOIN INCIDENT I ON A.incident_id = I.incident_id
        JOIN USER U ON A.user_id = U.user_id
    """)
    rows = cur.fetchall()
    db.close()
    return render_template('assignments.html', assignments=rows)

# ── REPORTS (AGGREGATE) ──
@app.route('/reports')
def reports():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT severity, COUNT(*) AS total
        FROM INCIDENT GROUP BY severity ORDER BY total DESC
    """)
    by_severity = cur.fetchall()

    cur.execute("""
        SELECT status, COUNT(*) AS total
        FROM INCIDENT GROUP BY status
    """)
    by_status = cur.fetchall()

    cur.execute("""
        SELECT T.threat_name, COUNT(*) AS linked_incidents,
               ROUND(AVG(IT.detection_confidence), 1) AS avg_confidence
        FROM INCIDENT_THREAT IT
        JOIN THREAT T ON IT.threat_id = T.threat_id
        GROUP BY T.threat_name
    """)
    threat_stats = cur.fetchall()

    cur.execute("""
        SELECT U.name, COUNT(*) AS total_assigned
        FROM INCIDENT_ASSIGNMENT A
        JOIN USER U ON A.user_id = U.user_id
        GROUP BY U.name ORDER BY total_assigned DESC
    """)
    analyst_load = cur.fetchall()

    db.close()
    return render_template('reports.html',
                           by_severity=by_severity,
                           by_status=by_status,
                           threat_stats=threat_stats,
                           analyst_load=analyst_load)

if __name__ == '__main__':
    app.run(debug=True)
