from flask import Flask, render_template, request, redirect, session, url_for, jsonify,send_file
from flask_mysqldb import MySQL
import json
from ml.ml_manager import get_model_manager

from datetime import datetime
import traceback
import json
import os


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io



app = Flask(__name__)
app.secret_key = "SECRET123"

# ----------------------
# MySQL CONFIG
# ----------------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "hallibaz_neurosense"
app.config["MYSQL_PASSWORD"] = "neurosense@123"
app.config["MYSQL_DB"] = "hallibaz_neurosense"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def index():
    return render_template("patient_login.html")

@app.route("/check")
def check():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, full_name
        FROM patients
        WHERE full_name IS NOT NULL AND full_name != ''
        ORDER BY full_name
    """)
    patients = cur.fetchall()

    return render_template(
        "check.html",
        patients=patients
    )
   

# ---------------------------
# PATIENT SIGNUP
# ---------------------------
@app.route("/patient_signup", methods=["GET","POST"])
def patient_signup():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO patients(full_name,email,password) VALUES(%s,%s,%s)", (name,email,password))
        mysql.connection.commit()

        return redirect(url_for("patient_login"))
    return render_template("patient_signup.html")
    
@app.route("/doctor_register", methods=["GET","POST"])
def doctor_register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO `doctors`( `name`, `email`, `password`)   VALUES(%s,%s,%s)", (name,email,password))
        mysql.connection.commit()

        return redirect(url_for("doctor_login"))
    return render_template("doctor_signup.html")

# ---------------------------
# PATIENT LOGIN
# ---------------------------
@app.route("/patient_login", methods=["GET","POST"])
def patient_login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM patients WHERE email=%s AND password=%s", (email, password))
        user=cur.fetchone()

        if user:
            session["patient_id"]=user["id"]
            session["patient"] = "Patient User"
            return redirect(url_for("patient_dashboard"))
        return "Invalid login"
    return render_template("patient_login.html")

# ---------------------------
# PATIENT DASHBOARD
# ---------------------------


# ==========================================
# UPDATE PROFILE (SAVE CHANGES)
# ==========================================
@app.route("/update", methods=["POST"])
def update_profile():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    pid = session["patient_id"]

    # Get form data
    full_name  = request.form.get("full_name")
    phone      = request.form.get("phone")
    age        = request.form.get("age")
    gender     = request.form.get("gender")
    blood_type = request.form.get("blood_type")
    password   = request.form.get("password")

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            UPDATE patients
            SET
                full_name = %s,
                phone = %s,
                age = %s,
                gender = %s,
                blood_type = %s,
                password = %s
            WHERE id = %s
        """, (
            full_name,
            phone,
            age,
            gender,
            blood_type,
            password,
            pid
        ))

        mysql.connection.commit()

    except Exception as e:
        print("PROFILE UPDATE ERROR:", e)
        mysql.connection.rollback()

    return redirect(url_for("patient_profile"))


@app.route("/timeline")
def patient_timeline():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    pid = session["patient_id"]
    event_type = request.args.get("type")
    disease = request.args.get("disease")

    query = """
        SELECT title, description, disease, event_type, created_at
        FROM health_events
        WHERE patient_id = %s
    """
    params = [pid]

    if event_type:
        query += " AND event_type = %s"
        params.append(event_type)

    if disease:
        query += " AND disease = %s"
        params.append(disease)

    query += " ORDER BY created_at DESC"

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    events = cur.fetchall()

    return render_template(
        "patient_timeline.html",
        events=events,
        active_page="timeline"
    )




@app.route("/timeline_export")
def export_timeline():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    pid = session["patient_id"]
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT title, description, disease, created_at
        FROM health_events
        WHERE patient_id=%s
        ORDER BY created_at DESC
    """, (pid,))
    events = cur.fetchall()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Health Timeline")
    y -= 40

    pdf.setFont("Helvetica", 11)
    for e in events:
        pdf.drawString(50, y, f"{e['created_at']} - {e['title']}")
        y -= 15
        pdf.drawString(60, y, e['description'])
        y -= 20
        pdf.drawString(60, y, f"Disease: {e['disease']}")
        y -= 30

        if y < 100:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Health_Timeline.pdf",
        mimetype="application/pdf"
    )



# ==========================================
# MY EHR PAGE
# ==========================================
@app.route("/ehr")
def patient_ehr():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    pid = session["patient_id"]
    cur = mysql.connection.cursor()

    # Patient info
    cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
    info = cur.fetchone()

    # Assessments
    cur.execute("""
        SELECT diag, created_at
        FROM assessments
        WHERE patient_id=%s
        ORDER BY created_at DESC
    """, (pid,))
    assessments = cur.fetchall()

    # ✅ Parse diag JSON here
    for a in assessments:
        try:
            a["diag"] = json.loads(a["diag"])
        except:
            a["diag"] = {}

    return render_template(
        "patient_ehr.html",
        info=info,
        assessments=assessments,
        active_page="ehr"
    )


# ==========================================
# DOWNLOAD FULL EHR
# ==========================================
@app.route("/ehr_download")
def download_ehr():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    pid = session["patient_id"]
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
    patient = cur.fetchone()

    cur.execute("SELECT diag, created_at FROM assessments WHERE patient_id=%s", (pid,))
    assessments = cur.fetchall()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Electronic Health Record")
    y -= 30

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Name: {patient['full_name']}")
    y -= 15
    pdf.drawString(50, y, f"Email: {patient['email']}")
    y -= 15
    pdf.drawString(50, y, f"Age: {patient['age']}")
    y -= 30

    for a in assessments:
        d = json.loads(a["diag"])
        pdf.drawString(50, y, f"Diagnosis: {d['primary_diagnosis']}")
        y -= 15
        pdf.drawString(60, y, f"Confidence: {d['diagnosis_confidence']}")
        y -= 25

        if y < 100:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="EHR_Report.pdf",
        mimetype="application/pdf"
    )


# ==========================================
# PATIENT PROFILE PAGE
# ==========================================
@app.route("/patient_profile")
def patient_profile():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    pid = session["patient_id"]

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            id,
            full_name,
            email,
            phone,
            age,
            gender,
            blood_type,
            password
        FROM patients
        WHERE id = %s
    """, (pid,))
    info = cur.fetchone()

    return render_template(
        "patient_profile.html",
        active_page="profile",
        info=info
    )


@app.route("/patient_dashboard")
def patient_dashboard():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))
    return render_template("patient_dashboard.html")

# ---------------------------
# START ASSESSMENT (4 STEPS)
# ---------------------------
@app.route("/assessment", methods=["GET","POST"])
def assessment():
    if "patient_id" not in session:
        return redirect(url_for("patient_login"))

    step = int(request.args.get("step",1))

    if "form" not in session:
        session["form"]={}

    if request.method=="POST":
        for k,v in request.form.items():
            session["form"][k]=v

        if step<4:
            return redirect(url_for("assessment", step=step+1))
        else:
            # RUN ML MODEL
            ml=get_model_manager()
            form=session["form"]

            alz = ml.predict_alzheimers_risk(form)
            park = ml.predict_parkinsons_risk(form)
            dem = ml.predict_dementia_risk(form)
            diag = ml.predict_diagnostic(form)

            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO assessments(patient_id, form_data, alz, park, dem, diag) VALUES (%s,%s,%s,%s,%s,%s)",
                (session["patient_id"], json.dumps(form),
                 json.dumps(alz.__dict__), json.dumps(park.__dict__),
                 json.dumps(dem.__dict__), json.dumps(diag.__dict__)
                ))
            mysql.connection.commit()

            session.pop("form")

            return render_template(
                "assessment_result.html",
                risk_scores=[alz.__dict__, park.__dict__, dem.__dict__],
                diagnostic=diag.__dict__,
            )

    return render_template(f"assessment_step{step}.html", step=step)

# ---------------------------
# DOCTOR LOGIN
# ---------------------------
@app.route("/doctor_login", methods=["GET","POST"])
def doctor_login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM doctors WHERE email=%s AND password=%s", (email,password))
        doc=cur.fetchone()

        if doc:
            session["doctor_id"]=doc["id"]
            return redirect(url_for("doctor_dashboard"))
        return "Invalid doctor login"
    return render_template("doctor_login.html")

# ---------------------------
# DOCTOR DASHBOARD
# ---------------------------
@app.route("/doctor_dashboard")
def doctor_dashboard():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    cur = mysql.connection.cursor()

    # Total patients
    cur.execute("SELECT COUNT(*) AS total FROM patients")
    total_patients = cur.fetchone()["total"]

    # High risk patients
    cur.execute("""
        SELECT COUNT(*) AS high_risk
        FROM diagnostic_reports
        WHERE diagnosis_confidence >= 0.7
    """)
    high_risk = cur.fetchone()["high_risk"]

    # Pending cases
    cur.execute("""
        SELECT COUNT(*) AS pending
        FROM diagnostic_reports
        WHERE diagnosis_confidence < 0.7
    """)
    pending = cur.fetchone()["pending"]

    # Alerts (high severity events)
    cur.execute("""
        SELECT COUNT(*) AS alerts
        FROM health_events
        WHERE severity = 'high'
    """)
    alerts = cur.fetchone()["alerts"]

    # Patient roster
    cur.execute("""
        SELECT id, full_name, age, gender
        FROM patients
        ORDER BY id DESC
        LIMIT 5
    """)
    patients = cur.fetchall()

    # Recent activity
    cur.execute("""
        SELECT title, created_at
        FROM health_events
        ORDER BY created_at DESC
        LIMIT 5
    """)
    activities = cur.fetchall()

    return render_template(
        "doctor_dashboard.html",
        total_patients=total_patients,
        high_risk=high_risk,
        pending=pending,
        alerts=alerts,
        patients=patients,
        activities=activities
    )

# ---------------------------
# DOCTOR - PATIENT MANAGEMENT
# ---------------------------
@app.route("/doctor_patients")
def doctor_patients():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    search = request.args.get("search", "").strip()

    cur = mysql.connection.cursor()

    if search:
        cur.execute("""
            SELECT id, full_name, email, age, gender
            FROM patients
            WHERE full_name LIKE %s OR email LIKE %s
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%"))
    else:
        cur.execute("""
            SELECT id, full_name, email, age, gender
            FROM patients
            ORDER BY id DESC
        """)

    patients = cur.fetchall()

    return render_template(
        "patient_management.html",
        patients=patients,
        search=search
    )



@app.route("/doctor_diagnostics_dash")
def doctor_diagnostics_page():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, full_name
        FROM patients
        WHERE full_name IS NOT NULL AND full_name != ''
        ORDER BY full_name
    """)
    patients = cur.fetchall()

    return render_template(
        "diagnostics.html",
        patients=patients
    )





def insert_diagnostic_report(data):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO diagnostic_reports
        (patient_id, doctor_id, primary_diagnosis, diagnosis_confidence,
         secondary_diagnoses, disease_probabilities, key_findings, recommendations,
         mmse_score, cdr_score, csf_tau_level, csf_abeta42_level, apoe_status,
         mri_file_path, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
    """, (
        data["patient_id"],
        data["doctor_id"],
        data["primary_diagnosis"],
        data["diagnosis_confidence"],
        json.dumps(data["secondary_diagnoses"]),
        json.dumps(data["disease_probabilities"]),
        json.dumps(data["key_findings"]),
        json.dumps(data["recommendations"]),
        data["mmse_score"],
        data["cdr_score"],
        data["csf_tau_level"],
        data["csf_abeta42_level"],
        data["apoe_status"],
        data["mri_file_path"]
    ))
    mysql.connection.commit()
    return cur.lastrowid

# -------------------------------------------------------------------
# MAIN ROUTE — RUN DIAGNOSTICS

@app.route("/doctor_patient_latest-assessment/<int:patient_id>")
def get_latest_assessment(patient_id):
    if "doctor_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT diag
        FROM assessments
        WHERE patient_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (patient_id,))

    row = cur.fetchone()

    if not row:
        return jsonify({"status": "empty"})

    try:
        diag = json.loads(row["diag"])
    except:
        diag = {}

    return jsonify({
        "status": "success",
        "primary_diagnosis": diag.get("primary_diagnosis", ""),
        "diagnosis_confidence": diag.get("diagnosis_confidence", ""),
        "secondary_diagnoses": ", ".join(diag.get("secondary_diagnoses", [])),
        "recommendations": ", ".join(diag.get("recommendations", [])),
        "key_findings": ", ".join(diag.get("key_findings", []))
    })

@app.route("/doctor_diagnostics", methods=["POST"])
def run_diagnostics():
    try:
        data = request.get_json()
        model_manager = get_model_manager()

        patient_id = data.get("patient_id")
        doctor_id = data.get("doctor_id")

        if not patient_id or not doctor_id:
            return jsonify({"status": "error", "message": "Missing patient or doctor"}), 400

        # ----------------------------------
        # 1. RUN ML MODEL
        # ----------------------------------
        try:
            result = model_manager.predict_diagnostic(data)
        except Exception as e:
            print("⚠️ ML Error → fallback:", e)
            result = model_manager._fallback_diagnostic(data)

        # ----------------------------------
        # 2. INSERT DIAGNOSTIC REPORT
        # ----------------------------------
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO diagnostic_reports
            (patient_id, doctor_id, primary_diagnosis, diagnosis_confidence,
             secondary_diagnoses, disease_probabilities, key_findings,
             recommendations, mmse_score, cdr_score,
             csf_tau_level, csf_abeta42_level, apoe_status,
             mri_file_path, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
        """, (
            patient_id,
            doctor_id,
            result.primary_diagnosis,
            result.diagnosis_confidence,
            json.dumps(result.secondary_diagnoses),
            json.dumps(result.disease_probabilities),
            json.dumps(result.key_findings),
            json.dumps(result.recommendations),
            data.get("mmse_score"),
            data.get("cdr_score"),
            data.get("csf_tau_level"),
            data.get("csf_abeta42_level"),
            data.get("apoe_status"),
            data.get("mri_file_path")
        ))

        mysql.connection.commit()
        report_id = cur.lastrowid   # ✅ GUARANTEED

        # ----------------------------------
        # 3. INSERT HEALTH EVENT
        # ----------------------------------
        cur.execute("""
            INSERT INTO health_events
            (patient_id, event_type, title, description, severity, disease, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,NOW())
        """, (
            patient_id,
            "diagnosis",
            f"Diagnostic Report: {result.primary_diagnosis}",
            f"Primary diagnosis confirmed: {result.primary_diagnosis}",
            "high" if result.diagnosis_confidence >= 0.7 else "moderate",
            result.primary_diagnosis
        ))

        mysql.connection.commit()

        # ----------------------------------
        # 4. AUDIT LOG
        # ----------------------------------
        cur.execute("""
            INSERT INTO audit_log
            (user_id, action, table_name, record_id, changes, created_at)
            VALUES (%s,%s,%s,%s,%s,NOW())
        """, (
            doctor_id,
            "CREATE",
            "diagnostic_reports",
            report_id,
            json.dumps({"diagnosis": result.primary_diagnosis})
        ))

        mysql.connection.commit()

        # ----------------------------------
        # 5. FINAL RESPONSE (IMPORTANT)
        # ----------------------------------
        return jsonify({
            "status": "success",
            "report_id": report_id,
            "primary_diagnosis": result.primary_diagnosis,
            "diagnosis_confidence": result.diagnosis_confidence,
            "secondary_diagnoses": result.secondary_diagnoses,
            "disease_probabilities": result.disease_probabilities,
            "key_findings": result.key_findings,
            "recommendations": result.recommendations,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        print("🔥 CRITICAL ERROR:", e, traceback.format_exc())

        return jsonify({
            "status": "error",
            "report_id": None,
            "primary_diagnosis": "Pending Medical Evaluation",
            "diagnosis_confidence": 0.5,
            "recommendations": ["Consult a healthcare professional"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route("/upload_mri", methods=["POST"])
def upload_mri():
    if "doctor_id" not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    if "mri_file" not in request.files:
        return jsonify({"status": "error", "message": "No file provided"})

    file = request.files["mri_file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "Empty filename"})

    upload_dir = "uploads/mri"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)

    file.save(filepath)

    return jsonify({
        "status": "success",
        "message": "MRI uploaded successfully",
        "file": filepath
    })


@app.route("/doctor_patients_add", methods=["GET", "POST"])
def add_patient():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form.get("phone")
        age = request.form.get("age")
        gender = request.form.get("gender")
        blood_type = request.form.get("blood_type")
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO patients
            (full_name, email, phone, age, gender, blood_type, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            full_name,
            email,
            phone,
            age,
            gender,
            blood_type,
            password
        ))
        mysql.connection.commit()

        return redirect(url_for("doctor_patients"))

    return render_template("add_patient.html")



# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("patient_login"))

# ---------------------------
# DOCTOR - INTERVENTIONS
# ---------------------------
@app.route("/doctor_interventions", methods=["GET", "POST"])
def doctor_interventions():
    if "doctor_id" not in session:
        return redirect(url_for("doctor_login"))

    cur = mysql.connection.cursor()

    # -------------------------------
    # SAVE INTERVENTION
    # -------------------------------
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        diagnosis = request.form["diagnosis"]
        intervention_type = request.form["intervention_type"]
        details = request.form["details"]

        cur.execute("""
            INSERT INTO health_events
            (patient_id, event_type, title, description, severity, disease, created_at)
            VALUES (%s,'intervention',%s,%s,'moderate',%s,NOW())
        """, (
            patient_id,
            f"{intervention_type} Intervention",
            details,
            diagnosis
        ))
        mysql.connection.commit()

        return redirect(url_for("doctor_interventions"))

    # -------------------------------
    # FETCH PATIENTS
    # -------------------------------
    cur.execute("""
        SELECT id, full_name
        FROM patients
        WHERE full_name IS NOT NULL AND full_name != ''
        ORDER BY full_name
    """)
    patients = cur.fetchall()

    # -------------------------------
    # FETCH INTERVENTIONS
    # -------------------------------
    cur.execute("""
        SELECT 
            he.id,
            p.full_name,
            he.title,
            he.description,
            he.disease,
            he.created_at
        FROM health_events he
        JOIN patients p ON he.patient_id = p.id
        WHERE he.event_type = 'intervention'
        ORDER BY he.created_at DESC
        LIMIT 10
    """)
    interventions = cur.fetchall()

    return render_template(
        "interventions.html",
        patients=patients,
        interventions=interventions
    )



@app.route("/add_note", methods=["POST"])
def run_diagnostics_flask():
    try:
        body = request.json
        model_manager = get_model_manager()

        patient_id = body.get("patient_id")
        doctor_id = body.get("doctor_id")

        print("=== Starting Diagnostics for Patient:", patient_id, "===")

        # -------------------------------
        # STEP 1 — MODEL PREDICTION
        # -------------------------------
        try:
            diagnostic_result = model_manager.predict_diagnostic(body)
        except Exception as e:
            print("⚠️ Model Error — Using fallback:", e)
            diagnostic_result = model_manager._fallback_diagnostic(body)

        if not diagnostic_result:
            diagnostic_result = model_manager._fallback_diagnostic(body)

        # -------------------------------
        # STEP 2 — INSERT DIAGNOSTIC REPORT INTO DB
        # -------------------------------
        report_id = None
        try:
            cur = mysql.connection.cursor()

            cur.execute("""
                INSERT INTO diagnostic_reports 
                (patient_id, doctor_id, primary_diagnosis, diagnosis_confidence,
                 secondary_diagnoses, disease_probabilities, key_findings, recommendations,
                 mmse_score, cdr_score, csf_tau_level, csf_abeta42_level, apoe_status, 
                 mri_file_path, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())
            """, (
                patient_id,
                doctor_id,
                diagnostic_result.primary_diagnosis,
                diagnostic_result.diagnosis_confidence,
                json.dumps(diagnostic_result.secondary_diagnoses),
                json.dumps(diagnostic_result.disease_probabilities),
                json.dumps(diagnostic_result.key_findings),
                json.dumps(diagnostic_result.recommendations),
                body.get("mmse_score"),
                body.get("cdr_score"),
                body.get("csf_tau_level"),
                body.get("csf_abeta42_level"),
                body.get("apoe_status"),
                body.get("mri_file_path")
            ))

            mysql.connection.commit()
            report_id = cur.lastrowid

        except Exception as e:
            print("⚠️ DB Error inserting diagnostic report:", e)
            report_id = f"temp_{int(datetime.utcnow().timestamp())}"

        # -------------------------------
        # STEP 3 — INSERT HEALTH EVENT
        # -------------------------------
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO health_events
                (patient_id, event_type, title, description, severity, disease, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (
                patient_id,
                "diagnosis",
                f"Diagnostic Report: {diagnostic_result.primary_diagnosis}",
                f"Primary diagnosis: {diagnostic_result.primary_diagnosis}",
                "high" if diagnostic_result.diagnosis_confidence > 0.7 else "moderate",
                diagnostic_result.primary_diagnosis
            ))
            mysql.connection.commit()
        except Exception as e:
            print("⚠️ Error inserting health event:", e)

        # -------------------------------
        # STEP 4 — AUDIT LOG
        # -------------------------------
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO audit_log
                (user_id, action, table_name, record_id, changes, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (
                doctor_id,
                "CREATE",
                "diagnostic_reports",
                report_id,
                json.dumps({"diagnosis": diagnostic_result.primary_diagnosis})
            ))
            mysql.connection.commit()
        except Exception as e:
            print("⚠️ Error inserting audit log:", e)

        # -------------------------------
        # FINAL SUCCESS RESPONSE
        # -------------------------------
        return jsonify({
            "report_id": report_id,
            "patient_id": patient_id,
            "primary_diagnosis": diagnostic_result.primary_diagnosis,
            "diagnosis_confidence": diagnostic_result.diagnosis_confidence,
            "secondary_diagnoses": diagnostic_result.secondary_diagnoses,
            "disease_probabilities": diagnostic_result.disease_probabilities,
            "key_findings": diagnostic_result.key_findings,
            "recommendations": diagnostic_result.recommendations,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        print("🔥 CRITICAL ERROR:", e, traceback.format_exc())

        return jsonify({
            "report_id": f"error_{int(datetime.utcnow().timestamp())}",
            "patient_id": request.json.get("patient_id"),
            "primary_diagnosis": "Pending Medical Evaluation",
            "diagnosis_confidence": 0.5,
            "secondary_diagnoses": [],
            "disease_probabilities": {"pending": 1.0},
            "key_findings": ["Requires additional clinical evaluation"],
            "recommendations": ["Consult your healthcare provider"],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
