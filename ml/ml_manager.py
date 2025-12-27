"""
ML Model Loading & Inference Module (Flask Compatible)
Now supports: TensorFlow / Keras Models
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

import xgboost as xgb
import lightgbm as lgb
import tensorflow as tf   # ← NEW
from sklearn.preprocessing import StandardScaler


# -----------------------------
# DATA CLASSES
# -----------------------------
@dataclass
class RiskPrediction:
    disease: str
    score: float
    confidence: float
    risk_level: str
    top_factors: List[List]


@dataclass
class DiagnosticResult:
    primary_diagnosis: str
    diagnosis_confidence: float
    secondary_diagnoses: List[str]
    disease_probabilities: Dict[str, float]
    key_findings: List[str]
    recommendations: List[str]


# -----------------------------
# MODEL MANAGER
# -----------------------------
class MLModelManager:

    def __init__(self, models_path: str = "ml/Models"):
        self.models_path = Path(models_path)
        self.models = {}
        self.scalers = {}
        self.fallback_mode = False
        self._load_all_models()

    # =============================
    # LOAD ALL MODELS
    # =============================
    def _load_all_models(self):
        try:
            # XGBoost Models
            self._load_xgb("alzheimer_model1_xgb", "alzheimer_model1_xgb.json")
            self._load_xgb("alzheimer_model2_xgb", "alzheimer_model2_lgbm.pkl")

            self._load_xgb("parkinsons_model1_xgb", "parkinsons_model1_xgb.json")
            self._load_xgb("parkinsons_model2_xgb", "parkinsons_model2_xgb.json")

            self._load_xgb("dementia_oasis_model", "dementia_oasis_model.json")
            self._load_xgb("dementia_progression_model", "dementia_progression_model.json")

            # TensorFlow Model
            self._load_tf("tf_neuro_model", "tf_multimodal_model.h5")

            # Scalers
            self._load_scaler("dementia_scaler", "dementia_scaler.pkl")
            self._load_scaler("parkinsons_scaler1", "parkinsons_scaler1.pkl")

            if len(self.models) == 0:
                print("⚠️ No ML models found → fallback mode enabled")
                self.fallback_mode = True

        except Exception as e:
            print("❌ MODEL LOAD ERROR:", e)
            self.fallback_mode = True

    # =============================
    # LOADERS
    # =============================
    def _load_xgb(self, name, file):
        path = self.models_path / file
        if path.exists():
            try:
                model = xgb.Booster()
                model.load_model(str(path))
                self.models[name] = model
                print(f"✔ Loaded XGBoost: {name}")
            except:
                pass

    def _load_lgbm(self, name, file):
        path = self.models_path / file
        if path.exists():
            try:
                with open(path, "rb") as f:
                    self.models[name] = pickle.load(f)
                print(f"✔ Loaded LightGBM: {name}")
            except:
                pass

    def _load_tf(self, name, file):
        """Load TensorFlow / Keras Model"""
        path = self.models_path / file
        if path.exists():
            try:
                self.models[name] = tf.keras.models.load_model(path)
                print(f"✔ Loaded TensorFlow Model: {name}")
            except Exception as e:
                print("TensorFlow load error:", e)

    def _load_scaler(self, name, file):
        path = self.models_path / file
        if path.exists():
            with open(path, "rb") as f:
                self.scalers[name] = pickle.load(f)
            print(f"✔ Loaded Scaler: {name}")

    # =============================
    # TENSORFLOW PREDICTION
    # =============================
    def _predict_tf(self, name, fv):
        """Predict using TensorFlow model"""
        if name not in self.models:
            return None
        try:
            model = self.models[name]
            fv = fv.reshape(1, -1)
            result = model.predict(fv)[0][0]
            return float(result)
        except Exception as e:
            print("TF Prediction Error:", e)
            return None

    # =============================
    # DISEASE RISK MODELS
    # =============================
    def predict_alzheimers_risk(self, f):
        if self.fallback_mode:
            return self._fallback_risk("Alzheimer's", f)

        fv = self._extract_features(f)
        p1 = self._predict_xgb("alzheimer_model1_xgb", fv)
        p2 = self._predict_tf("tf_neuro_model", fv)  # ← TensorFlow added

        if p1 is None and p2 is None:
            return self._fallback_risk("Alzheimer's", f)

        score = float(np.mean([p for p in [p1, p2] if p is not None]) * 100)

        return RiskPrediction(
            disease="Alzheimer's",
            score=score,
            confidence=90,
            risk_level=self._risk(score),
            top_factors=self._top_factors(f, score)
        )

    def predict_parkinsons_risk(self, f):
        if self.fallback_mode:
            return self._fallback_risk("Parkinson's", f)

        fv = self._extract_features(f)
        p1 = self._predict_xgb("parkinsons_model1_xgb", fv)
        p2 = self._predict_tf("tf_neuro_model", fv)

        if p1 is None and p2 is None:
            return self._fallback_risk("Parkinson's", f)

        score = float(np.mean([p for p in [p1, p2] if p is not None]) * 100)

        return RiskPrediction(
            disease="Parkinson's",
            score=score,
            confidence=88,
            risk_level=self._risk(score),
            top_factors=self._top_factors(f, score)
        )

    def predict_dementia_risk(self, f):
        if self.fallback_mode:
            return self._fallback_risk("Dementia", f)

        fv = self._extract_features(f)
        d1 = self._predict_xgb("dementia_oasis_model", fv)
        d2 = self._predict_tf("tf_neuro_model", fv)

        if d1 is None and d2 is None:
            return self._fallback_risk("Dementia", f)

        score = float(np.mean([p for p in [d1, d2] if p is not None]) * 100)

        return RiskPrediction(
            disease="Dementia",
            score=score,
            confidence=87,
            risk_level=self._risk(score),
            top_factors=self._top_factors(f, score)
        )

    # =============================
    # MULTIMODAL DIAGNOSTIC
    # =============================
    def predict_diagnostic(self, f):
        alz = self.predict_alzheimers_risk(f)
        dem = self.predict_dementia_risk(f)
        park = self.predict_parkinsons_risk(f)

        preds = sorted(
            [(alz.disease, alz.score),
             (dem.disease, dem.score),
             (park.disease, park.score)],
            key=lambda x: x[1], reverse=True
        )

        primary = preds[0][0]

        probs = {d[0]: d[1] / sum(p[1] for p in preds) for d in preds}

        return DiagnosticResult(
            primary_diagnosis=primary,
            diagnosis_confidence=round(preds[0][1] / 100, 2),
            secondary_diagnoses=[p[0] for p in preds[1:]],
            disease_probabilities=probs,
            key_findings=[f"Primary risk detected: {primary}"],
            recommendations=[
                "Consult neurologist",
                "Consider MRI/CT scan",
                "Maintain lifestyle modifications"
            ]
        )

    # =============================
    # HELPERS
    # =============================
    def _extract_features(self, f):
        return np.array([
            float(f.get("age", 65)),
            float(f.get("weight", 70)),
            float(f.get("height", 170)),
            1 if f.get("gender") == "Male" else 0,
            float(f.get("alcoholConsumption", 0)),
            1 if "Alzheimer's Disease" in f.get("familyHistory", []) else 0,
            1 if "Parkinson's Disease" in f.get("familyHistory", []) else 0,
            1 if "Dementia" in f.get("familyHistory", []) else 0,
        ], dtype=np.float32)

    def _risk(self, s):
        return "high" if s >= 70 else "moderate" if s >= 40 else "low"

    def _top_factors(self, f, s):
        factors = []
        if f.get("age", 0) >= 70: factors.append(["Age", 90])
        if f.get("memoryComplaints") in ["moderate", "severe"]: factors.append(["Memory", 80])
        if len(f.get("neurologicalSymptoms", [])) > 1: factors.append(["Neuro Symptoms", 85])
        return factors[:5]

    def _fallback_risk(self, disease, f):
        score = float(self._fallback_score(f))
        return RiskPrediction(
            disease=disease,
            score=score,
            confidence=75,
            risk_level=self._risk(score),
            top_factors=self._top_factors(f, score)
        )

    def _fallback_score(self, f):
        score = 0
        if f.get("age", 0) >= 70: score += 30
        if f.get("memoryComplaints") in ["moderate", "severe"]: score += 25
        score += len(f.get("neurologicalSymptoms", [])) * 5
        return score


# =============================
# SINGLETON
# =============================
_model_manager = None

def get_model_manager():
    global _model_manager
    if _model_manager is None:
        _model_manager = MLModelManager()
    return _model_manager
