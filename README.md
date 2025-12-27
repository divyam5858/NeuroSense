# NeuroSense – AI-Powered Neurodegenerative Risk Assessment Platform

## Overview

**NeuroSense** is a clinical decision support system designed for early risk assessment and management of neurodegenerative diseases. The platform integrates multimodal clinical data, cognitive assessment tools, biomarkers, and machine learning models to provide physicians and patients with actionable risk predictions for **Alzheimer's Disease**, **Parkinson's Disease**, and **Dementia**.

Built as a comprehensive web-based application, NeuroSense bridges clinical expertise with computational intelligence, enabling:
- **Objective risk quantification** across multiple neurodegenerative conditions using ensemble ML models
- **Longitudinal patient monitoring** with timeline-based event tracking and historical analysis
- **Clinician-driven diagnostic workflows** with multimodal clinical feature integration
- **Patient-centric health management** with secure access to personal health records
- **Evidence-based clinical recommendations** derived from AI-assisted risk stratification

The system is designed for deployment in clinical practices, research institutions, and telemedicine platforms, supporting both diagnostic accuracy and preventive care strategies.

**Live Application**: [NeuroSense](https://urbanupscaleproperties.com/neurosense/)

---

## Key Features

### 1. Multimodal Machine Learning-Based Risk Prediction
- **Disease-Specific Risk Scoring**: Independent predictive models for Alzheimer's Disease, Parkinson's Disease, and Dementia
- **Ensemble Architecture**: Combines XGBoost, LightGBM, and TensorFlow/Keras models for robust predictions
- **Confidence-Based Uncertainty Quantification**: Risk scores normalized to 0-100% with calibrated confidence levels (60-90%)
- **Graceful Degradation**: Fallback rule-based scoring using clinical heuristics if ML models unavailable
- **Risk Stratification**: Automatic classification into High (≥70%), Moderate (40-70%), or Low (<40%) risk categories

### 2. Comprehensive 4-Step Assessment Framework
- **Structured Questionnaire**: Progressive multi-step data collection across demographics, cognitive symptoms, neurological features, and lifestyle factors
- **Voice-Assisted Input**: Accessibility support using Web Speech API for voice-based assessment entry
- **Clinical Biomarker Integration**: Support for MMSE scores, CDR assessments, CSF tau/amyloid-beta levels, and APOE genotyping
- **MRI Image Upload**: Direct integration of neuroimaging data with timestamp tracking
- **Session-Based State Management**: Form data accumulated across assessment steps with validation

### 3. Doctor Dashboard & Clinical Decision Support
- **Patient Management System**: Search, register, and manage patient records with demographic tracking
- **Automated Diagnostic Reporting**: Comprehensive report generation with primary/secondary diagnoses, probability distributions, findings, and recommendations
- **Intervention Logging**: Document and track therapeutic interventions with disease classification
- **High-Risk Alerting**: Automatic severity classification for clinical triage
- **Comprehensive Audit Logging**: Complete record of all diagnostic activities for compliance
- **KPI Dashboard**: Real-time metrics (total patients, high-risk cases, pending diagnoses, active alerts)

### 4. Patient Portal & Electronic Health Records
- **Secure Authentication**: Session-based login with credential encryption
- **Profile Management**: Self-service updates to demographic and medical information
- **Assessment History**: Longitudinal view of all completed assessments with timestamped results
- **Electronic Health Record (EHR) Export**: PDF generation of complete diagnostic reports and health timelines
- **Health Event Timeline**: Visual chronology of assessments, interventions, and clinical events
- **Portable Health Data**: Download and export complete health records for continuity of care

### 5. Multi-Condition Risk Analysis
- **Alzheimer's Disease Risk Assessment**: Specialized model incorporating age, family history, memory complaints, and neurological symptoms
- **Parkinson's Disease Risk Evaluation**: Dual-model approach integrating motor symptoms and disease-specific biomarkers
- **Dementia Risk Stratification**: OASIS-based staging scale with progression rate modeling
- **Differential Diagnosis**: Comparative risk analysis to identify primary vs. secondary diagnoses

### 6. PDF Report Generation & Data Export
- **Automated Report Creation**: Professional health timeline and assessment reports in PDF format
- **EHR Downloads**: Complete patient records in portable format
- **Assessment Result Cards**: Visual risk score representation with color-coded severity indicators
- **Clinical Recommendations Export**: Printable, patient-friendly guidance for follow-up care

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT TIER (Frontend)                   │
├─────────────────────────────────────────────────────────────┤
│ • Patient Portal (Dashboard, Assessment, EHR, Timeline)     │
│ • Doctor Interface (KPIs, Patient Management, Diagnostics)  │
│ • 4-Step Assessment Wizard                                  │
│ • Results Visualization (Risk Scores, Diagnoses)            │
│ • MRI Upload Interface                                      │
│ • PDF Export Functionality                                  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/AJAX
┌────────────────────────▼────────────────────────────────────┐
│               APPLICATION TIER (Backend)                    │
├─────────────────────────────────────────────────────────────┤
│ • Flask Web Framework (25+ Routes)                          │
│ • RESTful API Endpoints                                     │
│ • Authentication & Session Management                      │
│ • File Handling (MRI Uploads)                              │
│ • PDF Report Generation (ReportLab)                        │
│ • Form Data Validation & Processing                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│          ML INFERENCE TIER (ML Model Manager)               │
├─────────────────────────────────────────────────────────────┤
│ • Feature Extraction & Preprocessing                        │
│ • XGBoost Model Predictions                                │
│ • LightGBM Alternative Models                              │
│ • TensorFlow/Keras Multimodal Ensemble                     │
│ • Risk Score Aggregation & Interpretation                  │
│ • Fallback Rule-Based Scoring                              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│             DATA PERSISTENCE TIER (Database)               │
├─────────────────────────────────────────────────────────────┤
│ • MySQL Relational Database (InnoDB)                       │
│ • Tables: patients, doctors, assessments,                  │
│           diagnostic_reports, health_events, audit_log      │
│ • JSON Storage for Diagnostic Results                      │
│ • Foreign Key Relationships & ACID Compliance              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

**Patient Assessment → ML Inference → Report Generation → Database → Clinical Review**

1. **Data Collection**: Patient completes 4-step structured questionnaire
2. **Feature Engineering**: Raw form data extracted into ML-ready feature vectors
3. **Model Inference**: Ensemble predictions from disease-specific models
4. **Risk Scoring**: Model scores aggregated and normalized to 0-100 percentage scale
5. **Report Generation**: Automated synthesis of findings and recommendations
6. **Database Persistence**: Results stored with audit trail
7. **Clinician Review**: Doctor accesses formatted results via dashboard

---

## Technology Stack

### Frontend
- **HTML5** – Semantic markup and accessibility standards
- **CSS3** – Responsive design with modern layout (flexbox, grid)
- **JavaScript (Vanilla)** – Client-side interactivity, form handling, AJAX requests
- **Web Speech API** – Voice input support for accessible assessments

### Backend
- **Python 3.x** – Core application language
- **Flask 2.x** – Lightweight web framework for routing and request handling
- **Flask-MySQLdb** – MySQL database connectivity and cursor management
- **ReportLab** – PDF document generation for health timelines and EHR exports
- **JSON** – Data serialization for diagnostic results

### Machine Learning & Data Science
- **XGBoost** – Gradient boosted decision trees for disease-specific risk models
- **LightGBM** – High-performance gradient boosting framework
- **TensorFlow/Keras** – Deep learning models for multimodal feature fusion
- **NumPy** – Numerical array operations and matrix computations
- **scikit-learn** – StandardScaler for feature normalization and preprocessing

### Database
- **MySQL 5.7+** – Relational database management system
- **InnoDB** – ACID-compliant transactional storage engine
- **Schema**: Optimized for healthcare workflows with JSON columns for flexible result storage

---

## Machine Learning Pipeline

### Data Integration

The ML pipeline accepts multimodal clinical inputs:

- **Demographic Data**: Age, gender, weight, height
- **Cognitive Assessment**: Memory complaints severity, MMSE score, CDR stage
- **Neurological Symptoms**: Documented symptom list and severity
- **Biomarkers**: CSF tau level, CSF amyloid-beta 42, APOE genotype
- **Medical History**: Family history of neurodegenerative diseases
- **Lifestyle Factors**: Alcohol consumption, physical activity patterns

### Feature Engineering

Raw clinical data is extracted into an 8-dimensional feature vector:

```python
features = [
    age,                          # Continuous (years)
    weight,                       # Continuous (kg)
    height,                       # Continuous (cm)
    gender_encoded,              # Binary (0=Female, 1=Male)
    alcohol_consumption,         # Continuous (units/week)
    family_history_alzheimers,  # Binary indicator
    family_history_parkinsons,  # Binary indicator
    family_history_dementia,    # Binary indicator
]
```

All features are normalized using disease-specific StandardScaler objects loaded at startup.

### Models Used

#### Alzheimer's Disease Risk Model
- **Primary**: `alzheimer_model1_xgb.json` (XGBoost classifier)
- **Alternative**: `best_model_v2_complete.pt` (TensorFlow multimodal model)
- **Input**: 8-dimensional normalized feature vector
- **Output**: Probability [0, 1] normalized to [0, 100] percentage
- **Confidence**: 85-90%

#### Parkinson's Disease Risk Model
- **Model 1**: `parkinsons_model1_xgb.json` (XGBoost)
- **Model 2**: `parkinsons_model2_xgb.json` (Alternative XGBoost)
- **Scalers**: `parkinsons_scaler1.pkl`, `parkinsons_scaler2.pkl`
- **Output**: Risk score with confidence calibration
- **Confidence**: 80-88%

#### Dementia Progression Model
- **OASIS**: `dementia_oasis_model.json` (validated staging scale)
- **Progression**: `dementia_progression_model.json` (progression rate prediction)
- **Scaler**: `dementia_scaler.pkl`
- **Output**: Dementia stage probability distribution
- **Confidence**: 75-87%

#### Multimodal Ensemble Model
- **Framework**: TensorFlow/Keras
- **File**: `best_model_v2_complete.pt` or equivalent
- **Purpose**: Cross-disease evidence aggregation
- **Output**: Unified probability distribution

### Inference Flow

```
Raw Clinical Data
    ↓
Feature Extraction (8-dimensional vector)
    ↓
StandardScaler Normalization
    ↓
┌──────────────────────────────────────┐
│ Ensemble Prediction                  │
├──────────────────────────────────────┤
│ XGBoost Model 1 → Score₁             │
│ XGBoost Model 2 → Score₂             │
│ TensorFlow Model → Score₃            │
│ Average Ensemble → Final Score       │
└──────────────────────────────────────┘
    ↓
Risk Normalization (0-100%)
    ↓
Risk Level Classification
    ├─ High Risk: score ≥ 70%
    ├─ Moderate: 40% ≤ score < 70%
    └─ Low Risk: score < 40%
    ↓
Confidence Calibration (60-90%)
    ↓
Diagnostic Report Generation
```

### Risk Score Interpretation

- **High Risk (≥70%)**: Specialist neurological consultation recommended; neuroimaging and biomarker testing indicated
- **Moderate Risk (40-70%)**: Baseline cognitive assessment advised; lifestyle modifications and 6-12 month follow-up
- **Low Risk (<40%)**: Standard preventive care; annual cognitive screening recommended

### Fallback Mechanism

If models fail to load or inference errors occur:
- System activates **rule-based heuristic scoring** using clinical features
- Age-weighted: Age ≥ 70 → +30 points
- Memory complaints: Moderate/severe → +25 points
- Neurological symptoms: +5 points per symptom
- Ensures continuous availability without ML models

---

## Application Workflow

### Patient User Journey

#### 1. Registration & Authentication
```
Patient Signup → Create Account → Store Credentials
                      ↓
              Patient Login → Authenticate
                      ↓
            Initialize Session → Patient Dashboard
```

#### 2. Assessment Completion
```
Start Assessment
    ↓
Step 1: Demographics & Family History
    ↓
Step 2: Cognitive Symptoms & Memory
    ↓
Step 3: Neurological Symptoms & Lifestyle
    ↓
Step 4: Biomarkers (MMSE, CDR, CSF, APOE)
    ↓
Submit for ML Analysis
    ↓
ML Model Inference (Ensemble Prediction)
    ↓
Generate Diagnostic Report
    ↓
Display Risk Scores & Recommendations
    ↓
Save to Database (assessments table)
```

#### 3. Health Management
```
Patient EHR
    ├─ View Assessment History
    ├─ Primary Diagnosis & Confidence
    ├─ Secondary Diagnoses & Probabilities
    └─ Clinical Recommendations
    ↓
Health Timeline
    ├─ Filter by Event Type (diagnosis, intervention)
    ├─ Filter by Disease
    └─ View Chronological Events
    ↓
Export Options
    ├─ Download EHR as PDF
    └─ Export Timeline as PDF
    ↓
Profile Management
    └─ Update Demographics & Medical Info
```

### Doctor User Journey

#### 1. Registration & Authentication
```
Doctor Signup → Create Account → Store Credentials
                      ↓
             Doctor Login → Authenticate
                      ↓
          Initialize Session → Doctor Dashboard
```

#### 2. Dashboard Overview
```
Doctor Dashboard displays:
    ├─ Total Patients Count
    ├─ High-Risk Cases (confidence ≥ 70%)
    ├─ Pending Diagnoses (confidence < 70%)
    ├─ Active Alerts (high severity events)
    ├─ Recent Patient Roster
    └─ Activity Log (recent events)
```

#### 3. Patient Management
```
Patient Management
    ├─ View Patient Roster
    ├─ Search Patients (name, email)
    └─ Add New Patient (manual registration)
```

#### 4. Diagnostic Workflow
```
Diagnostics Page
    ↓
Select Patient
    ↓
Optional: Upload MRI Image
    ↓
Enter Clinical Biomarkers
    ├─ MMSE Score (0-30)
    ├─ CDR Score (0-3)
    ├─ CSF Tau Level
    ├─ CSF Amyloid-beta 42
    └─ APOE Genotype
    ↓
Optional: Load Latest Assessment
    ↓
Submit for Analysis
    ↓
ML Model Inference
    ↓
INSERT Diagnostic Report
    ├─ Primary diagnosis
    ├─ Confidence level
    ├─ Secondary diagnoses
    ├─ Disease probabilities
    └─ Recommendations
    ↓
INSERT Health Event
    └─ Track diagnosis in patient timeline
    ↓
INSERT Audit Log
    └─ Record diagnostic activity
    ↓
Display Results (JSON Response)
```

#### 5. Intervention Management
```
Interventions Page
    ↓
Select Patient
    ↓
Select Diagnosis (disease)
    ↓
Select Intervention Type
    ↓
Enter Details
    ↓
Log to health_events Table
    ↓
Display Intervention History
    ↓
Patient Sees in Timeline
```

---

## API Overview

### Patient Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Landing page |
| POST | `/patient_signup` | Register new patient |
| POST | `/patient_login` | Authenticate patient |
| GET | `/patient_dashboard` | Patient home page |
| GET | `/patient_profile` | View/edit profile |
| POST | `/update` | Update patient profile |
| GET | `/assessment?step=1-4` | Assessment questionnaire |
| POST | `/assessment` | Submit assessment step |
| GET | `/ehr` | Electronic health record |
| GET | `/ehr_download` | Export EHR as PDF |
| GET | `/timeline` | Health event timeline |
| GET | `/timeline_export` | Export timeline as PDF |
| GET | `/logout` | Clear session |

### Doctor Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/doctor_register` | Register new doctor |
| POST | `/doctor_login` | Authenticate doctor |
| GET | `/doctor_dashboard` | Doctor home with KPIs |
| GET | `/check` | Patient selection page |
| GET | `/doctor_patients` | Patient roster |
| GET | `/doctor_patients_add` | Add patient form |
| POST | `/doctor_patients_add` | Create new patient |
| GET | `/doctor_diagnostics_dash` | Diagnostics form |
| POST | `/doctor_diagnostics` | Run ML diagnosis (JSON) |
| GET | `/doctor_patient_latest-assessment/<pid>` | Get last assessment |
| POST | `/upload_mri` | Upload MRI file |
| GET | `/doctor_interventions` | Intervention manager |
| POST | `/doctor_interventions` | Log intervention |
| POST | `/add_note` | Alternative diagnosis endpoint |

### Response Format Example

**Diagnostic Result (JSON)**:
```json
{
  "status": "success",
  "report_id": 142,
  "primary_diagnosis": "Alzheimer's Disease",
  "diagnosis_confidence": 0.87,
  "secondary_diagnoses": ["Dementia", "Parkinson's Disease"],
  "disease_probabilities": {
    "Alzheimer's Disease": 0.52,
    "Dementia": 0.35,
    "Parkinson's Disease": 0.13
  },
  "key_findings": ["Primary risk detected: Alzheimer's Disease"],
  "recommendations": [
    "Consult neurologist for specialized evaluation",
    "Consider MRI/CT neuroimaging",
    "Maintain cognitive and lifestyle modifications"
  ],
  "timestamp": "2025-12-27T10:30:45.123456"
}
```

---

## Installation & Setup

### Prerequisites

- **Python 3.8+**
- **MySQL 5.7+** (or MySQL 8.0)
- **pip** (Python package manager)

### Backend Setup

#### 1. Clone Repository
```bash
git clone https://github.com/divyam5858/NeuroSense.git
cd NeuroSense
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
```
Flask==2.3.0
Flask-MySQLdb==1.1.0
XGBoost==1.7.0
LightGBM==3.3.0
TensorFlow==2.12.0
NumPy==1.24.0
scikit-learn==1.2.0
ReportLab==4.0.0
```

#### 4. Configure MySQL Database

Create database and user:
```sql
CREATE DATABASE hallibaz_neurosense;

CREATE USER 'hallibaz_neurosense'@'localhost' IDENTIFIED BY 'neurosense@123';

GRANT ALL PRIVILEGES ON hallibaz_neurosense.* TO 'hallibaz_neurosense'@'localhost';

FLUSH PRIVILEGES;
```

Create required tables:
```sql
USE hallibaz_neurosense;

CREATE TABLE patients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    phone VARCHAR(20),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    blood_type VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    form_data LONGTEXT,
    alz LONGTEXT,
    park LONGTEXT,
    dem LONGTEXT,
    diag LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE diagnostic_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT,
    primary_diagnosis VARCHAR(255),
    diagnosis_confidence FLOAT,
    secondary_diagnoses LONGTEXT,
    disease_probabilities LONGTEXT,
    key_findings LONGTEXT,
    recommendations LONGTEXT,
    mmse_score INT,
    cdr_score FLOAT,
    csf_tau_level FLOAT,
    csf_abeta42_level FLOAT,
    apoe_status VARCHAR(10),
    mri_file_path VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE health_events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    event_type ENUM('diagnosis', 'intervention', 'medication', 'assessment'),
    title VARCHAR(255),
    description LONGTEXT,
    severity ENUM('low', 'moderate', 'high'),
    disease VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(50),
    table_name VARCHAR(100),
    record_id INT,
    changes LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. Verify ML Models

Ensure models exist in `ml/Models/`:
```
alzheimer_model1_xgb.json
parkinsons_model1_xgb.json
parkinsons_model2_xgb.json
dementia_oasis_model.json
dementia_progression_model.json
best_model_v2_complete.pt
dementia_scaler.pkl
parkinsons_scaler1.pkl
parkinsons_scaler2.pkl
```

#### 6. Create Upload Directory
```bash
mkdir -p uploads/mri
```

### Configuration

Update database credentials in `app.py`:
```python
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "hallibaz_neurosense"
app.config["MYSQL_PASSWORD"] = "neurosense@123"
app.config["MYSQL_DB"] = "hallibaz_neurosense"
app.secret_key = "SECRET123"  # Change for production
```

### Running Locally

```bash
source venv/bin/activate
python app.py
```

Access at `http://localhost:5000`:
- **Patient Login**: `/patient_login`
- **Doctor Login**: `/doctor_login`
- **Patient Signup**: `/patient_signup`
- **Doctor Signup**: `/doctor_register`

---

## Deployment

### Development Deployment
- **Server**: Flask built-in development server (debug=True)
- **Database**: Local MySQL instance
- **File Storage**: Local filesystem (`uploads/mri/`)

### Production Deployment Architecture

**Recommended Stack**:
1. **Application Server**: Gunicorn or uWSGI with Flask
2. **Reverse Proxy**: Nginx or Apache
3. **Database**: MySQL 8.0+ with master-slave replication
4. **File Storage**: Cloud object storage (AWS S3, Azure Blob, GCP Cloud Storage)
5. **Container**: Docker for application isolation
6. **Orchestration**: Kubernetes or Docker Swarm for scaling

**Deployment Diagram**:
```
Internet
    ↓
[Nginx/Load Balancer]
    ↓
[Gunicorn App Containers (multiple instances)]
    ↓
[MySQL Master - Write] + [MySQL Slave - Read Replicas]
    ↓
[Cloud Storage - MRI uploads, PDF exports]
```

### Security Considerations

- **SSL/TLS**: Enable HTTPS encryption for all endpoints
- **Flask Secret Key**: Change from default to cryptographically secure value
- **Environment Variables**: Use `.env` file for sensitive credentials
- **Rate Limiting**: Implement on API endpoints to prevent abuse
- **CORS Headers**: Enable appropriate cross-origin policies
- **SQL Injection Prevention**: All queries use parameterized statements (already implemented)
- **Password Hashing**: Upgrade from plaintext to bcrypt/argon2
- **Database Encryption**: Enable at-rest encryption for sensitive data
- **Audit Logging**: Full record of all diagnostic and administrative actions

### Scaling Considerations

- **Horizontal Scaling**: Deploy multiple Gunicorn workers behind load balancer
- **Database Scaling**: Read replicas for assessment queries
- **ML Inference**: GPU acceleration with CUDA for TensorFlow models
- **Caching**: Redis for session management and prediction caching
- **CDN**: Static asset delivery via content delivery network

---

## Project Structure

```
NeuroSense/
│
├── app.py                           # Main Flask application (1038 lines)
│                                    # 25+ routes for auth, dashboards, assessments
│
├── ml/
│   ├── ml_manager.py               # ML Model Manager (singleton pattern)
│   │                               # - Feature extraction & normalization
│   │                               # - Model prediction logic
│   │                               # - Ensemble scoring
│   │                               # - Fallback mechanism
│   │
│   └── Models/                     # Pre-trained machine learning models
│       ├── alzheimer_model1_xgb.json
│       ├── parkinsons_model1_xgb.json
│       ├── parkinsons_model2_xgb.json
│       ├── dementia_oasis_model.json
│       ├── dementia_progression_model.json
│       ├── best_model_v2_complete.pt
│       ├── multitask_model_complete.pt
│       ├── dementia_scaler.pkl
│       ├── parkinsons_scaler1.pkl
│       └── (additional scalers & models)
│
├── templates/                      # Jinja2 HTML templates (server-side rendering)
│   ├── base.html                   # Base layout
│   ├── index.html                  # Landing page
│   ├── patient_login.html          # Patient authentication
│   ├── patient_signup.html         # Patient registration
│   ├── patient_dashboard.html      # Patient home
│   ├── patient_profile.html        # Patient profile editor
│   ├── patient_ehr.html            # Electronic health record
│   ├── patient_timeline.html       # Health event timeline
│   ├── assessment_step1.html       # Demographics & family history
│   ├── assessment_step2.html       # Cognitive symptoms
│   ├── assessment_step3.html       # Neurological symptoms
│   ├── assessment_step4.html       # Biomarkers
│   ├── assessment_result.html      # Risk scores & recommendations
│   ├── doctor_login.html           # Doctor authentication
│   ├── doctor_signup.html          # Doctor registration
│   ├── doctor_dashboard.html       # Doctor home with KPIs
│   ├── patient_management.html     # Patient roster
│   ├── add_patient.html            # Add patient form
│   ├── diagnostics.html            # Diagnostic form
│   ├── interventions.html          # Intervention tracking
│   ├── check.html                  # Utility page
│   └── clinic.html                 # Clinic information
│
├── static/                         # Static web assets
│   ├── styles.css                  # Global stylesheet (204 lines)
│   │                               # - Login card styling
│   │                               # - Form input styles
│   │                               # - Dashboard layout
│   │
│   └── css/
│       └── style.css               # Assessment form styling
│
├── uploads/                        # User-uploaded files
│   └── mri/                        # MRI image storage
│
└── README.md                       # This documentation
```

### Key Components

- **app.py**: Core Flask application with 25+ routes covering authentication, assessment workflow, diagnostic analysis, and report generation
- **ml_manager.py**: ML model management with support for XGBoost, LightGBM, and TensorFlow with fallback scoring
- **Models/**: Collection of pre-trained risk prediction models and feature scalers
- **templates/**: 23 Jinja2 templates for responsive patient and doctor interfaces
- **static/**: CSS styling for consistent visual design across all pages
- **uploads/**: Server-side storage for patient MRI images and generated PDF reports

---

## Use Cases

### 1. Clinical Practice – Neurologist Risk Screening
**Scenario**: A neurologist wants to objectively quantify patient neurodegenerative risk.

**Workflow**:
1. Register patient in doctor portal
2. Conduct clinical evaluation, document MMSE and CDR scores
3. Input patient data and optional MRI into diagnostics form
4. Run ML-powered assessment
5. Review multimodal risk report
6. Use risk stratification to guide specialist referrals and testing
7. Log interventions and plan follow-up visits

**Benefits**: Standardized risk quantification, evidence-based recommendations, longitudinal tracking, compliance documentation

### 2. Patient Self-Monitoring – Preventive Care
**Scenario**: A 72-year-old patient with Alzheimer's family history monitors cognitive health.

**Workflow**:
1. Self-register on patient portal
2. Complete 4-step assessment questionnaire
3. Receive immediate risk score report
4. Review personalized recommendations
5. Export EHR as PDF to share with physician
6. Access health timeline showing assessment history
7. Repeat assessment after 6 months for comparison

**Benefits**: Convenient self-service access, objective health metrics, portable health records, provider continuity

### 3. Research Institution – Algorithm Validation
**Scenario**: A neuroscience research center validates NeuroSense algorithms.

**Workflow**:
1. Create study-specific doctor accounts
2. Enroll research cohort via standardized assessments
3. Collect multimodal clinical data and biomarkers
4. Access participant EHRs with consent
5. Export assessment data for analysis
6. Validate system predictions against gold-standard diagnoses
7. Publish validation findings

**Benefits**: Standardized data collection, interoperable data structure, regulatory compliance, evidence generation

### 4. Telemedicine – Remote Assessment Integration
**Scenario**: A telemedicine provider integrates NeuroSense into routine virtual care.

**Workflow**:
1. Patient completes assessment during telehealth appointment
2. Provider reviews risk report in real-time
3. Provider discusses findings with patient
4. Provider orders additional testing if indicated
5. Provider documents intervention plan
6. Patient receives summary and action items
7. Follow-up scheduled based on risk stratification

**Benefits**: Scalable remote assessment, integrated decision support, improved engagement, data-driven coordination

---

## Future Enhancements

### Clinical Features
- **Biomarker Integration**: Direct laboratory API integration for real-time CSF/plasma biomarker data
- **Genetic Testing**: APOE/GRN/MAPT genotyping with genetic counseling modules
- **Neuroimaging Analysis**: Automated MRI analysis using deep learning for atrophy detection
- **Longitudinal Prediction**: Model disease progression trajectories over 5-10 years
- **Treatment Response**: ML-driven prediction of medication efficacy
- **Clinical Trial Matching**: Automated matching to eligible trials based on risk profile

### Technical Scalability
- **Microservices Architecture**: Refactor monolithic app into independent services
- **GraphQL API**: Flexible data querying for third-party integrations
- **Real-Time Alerts**: WebSocket-based notifications for high-risk diagnoses
- **Distributed ML Inference**: TensorFlow Serving or Seldon Core for low-latency predictions
- **Big Data Pipeline**: Apache Spark/Kafka for real-time data processing
- **Multi-Tenancy**: Support multiple healthcare organizations on single platform

### Research & Analytics
- **Natural Language Processing**: Automatic clinical note extraction
- **Model Explainability**: SHAP/LIME-based prediction interpretability
- **Population Health Analytics**: Aggregate risk profiling by demographics
- **Adverse Event Detection**: Active surveillance for unexpected outcomes
- **Model Monitoring**: Drift detection and automated retraining

### Regulatory & Compliance
- **FDA 510(k) Pathway**: Submit for clinical device classification
- **HIPAA Compliance**: Full encryption, access controls, audit logging
- **HL7/FHIR Interoperability**: EHR integration via healthcare standards
- **GDPR/CCPA Compliance**: Data governance and consent management
- **Data Anonymization**: De-identification pipelines for research

### User Experience
- **Mobile Apps**: Native iOS/Android applications
- **Voice Assistants**: Alexa/Google Assistant integration
- **Wearable Integration**: Apple Watch/Fitbit data enrichment
- **Patient Education**: Interactive disease prevention modules
- **Predictive Visualization**: Risk trajectory charts and dashboards
- **Peer Support Network**: Community features for patients

---

## License

**Academic & Educational Use**

NeuroSense is provided for academic research, educational purposes, and clinical evaluation as a research prototype.

**Terms**:
- Non-commercial use only without express written permission
- Attribution to NeuroSense development team required in publications
- No commercial redistribution or derivative commercialization
- Research institutions may use with project approval
- Consult development team for licensing beyond academic scope

**Disclaimer**:
This platform is a **research prototype**. It is **not an FDA-approved medical device** and **not cleared for diagnostic use in clinical practice**. Clinical implementation requires:
- Independent clinical validation in target population
- Regulatory approval from appropriate healthcare authorities
- Integration with institutional governance and quality assurance processes
- Informed consent from patients regarding research prototype status
- Compliance with applicable healthcare regulations (HIPAA, GDPR, etc.)

Users are solely responsible for ensuring compliance with all applicable laws and regulations before clinical deployment.

---

## Acknowledgments

**Development Team**: NeuroSense Development Project

**Technologies**: Built with Flask, XGBoost, LightGBM, TensorFlow, NumPy, scikit-learn, and MySQL

**Inspiration**: Academic literature on neurodegenerative disease assessment, cognitive screening instruments (MMSE, CDR, OASIS), biomarker interpretation, and clinical decision support systems

**Research Prototype**: Developed for academic and educational evaluation of AI-assisted clinical decision support in neurodegenerative disease screening.

---

**Repository**: [NeuroSense](https://github.com/divyam5858/NeuroSense)

**Live Application**: [NeuroSense](https://urbanupscaleproperties.com/neurosense/)

**Version**: 1.0.0

**Last Updated**: December 27, 2025
