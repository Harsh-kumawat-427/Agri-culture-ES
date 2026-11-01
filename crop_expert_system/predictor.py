"""
CropPredictor Module for Smart Crop & Fertilizer Advisor Expert System.
Loads saved ML model from joblib file and provides:
- predict_crop(): top predicted crop
- top_n_crops(): top N candidate crops with confidence probabilities
- confidence(): prediction confidence percentage
- SoilInput validation
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional

class SoilInput:
    """Represents raw farmer soil test parameters and weather readings."""
    def __init__(self, N: float, P: float, K: float, ph: float, rainfall: float, temperature: float, humidity: float):
        self.N = float(N)
        self.P = float(P)
        self.K = float(K)
        self.ph = float(ph)
        self.rainfall = float(rainfall)
        self.temperature = float(temperature)
        self.humidity = float(humidity)

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Checks parameter ranges according to agronomic feasibility."""
        if not (0 <= self.N <= 300):
            return False, "Nitrogen (N) must be between 0 and 300 kg/ha."
        if not (0 <= self.P <= 300):
            return False, "Phosphorus (P) must be between 0 and 300 kg/ha."
        if not (0 <= self.K <= 400):
            return False, "Potassium (K) must be between 0 and 400 kg/ha."
        if not (0.0 <= self.ph <= 14.0):
            return False, "pH must be between 0.0 and 14.0."
        if not (-10.0 <= self.temperature <= 65.0):
            return False, "Temperature must be between -10.0°C and 65.0°C."
        if not (0.0 <= self.humidity <= 100.0):
            return False, "Relative Humidity must be between 0% and 100%."
        if not (0.0 <= self.rainfall <= 1000.0):
            return False, "Rainfall must be between 0 mm and 1000 mm."
        return True, None

    def to_dict(self) -> Dict[str, float]:
        return {
            "N": self.N,
            "P": self.P,
            "K": self.K,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "ph": self.ph,
            "rainfall": self.rainfall
        }

    def to_df(self) -> pd.DataFrame:
        cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        return pd.DataFrame([[self.N, self.P, self.K, self.temperature, self.humidity, self.ph, self.rainfall]], columns=cols)


class CropPredictor:
    """Inference class that loads the trained classifier to forecast optimal crop labels."""
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            candidates = [
                os.path.join(base_dir, "models", "crop_model.pkl"),
                os.path.join(os.getcwd(), "crop_expert_system", "models", "crop_model.pkl"),
                os.path.join(os.getcwd(), "models", "crop_model.pkl")
            ]
            self.model_path = next((p for p in candidates if os.path.exists(p)), candidates[0])
        else:
            self.model_path = model_path
        self.model = None
        self.model_name = None
        self.classes = []
        self.load_model()

    def load_model(self):
        """Loads model file from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}. Run train_model.py first.")
        data = joblib.load(self.model_path)
        self.model = data["model"]
        self.model_name = data.get("model_name", "Random Forest Classifier")
        self.classes = data.get("classes", list(self.model.classes_))
        print(f"[CropPredictor] Successfully loaded {self.model_name} from {self.model_path}")

    def predict_crop(self, soil_input: SoilInput) -> str:
        """Predicts single most suitable crop."""
        valid, err = soil_input.validate()
        if not valid:
            raise ValueError(err)
        df_input = soil_input.to_df()
        pred = self.model.predict(df_input)[0]
        return str(pred)

    def top_n_crops(self, soil_input: SoilInput, n: int = 3) -> List[Dict[str, Any]]:
        """Returns top N crop recommendations ranked by confidence probability."""
        valid, err = soil_input.validate()
        if not valid:
            raise ValueError(err)
        df_input = soil_input.to_df()
        
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(df_input)[0]
            top_indices = np.argsort(probs)[::-1][:n]
            results = []
            for idx in top_indices:
                crop_label = str(self.classes[idx])
                conf = float(probs[idx])
                results.append({
                    "crop": crop_label,
                    "confidence": round(conf * 100, 2),
                    "probability": conf
                })
            return results
        else:
            best = self.predict_crop(soil_input)
            return [{"crop": best, "confidence": 100.0, "probability": 1.0}]

    def confidence(self, soil_input: SoilInput) -> float:
        """Returns highest prediction confidence score percentage."""
        top = self.top_n_crops(soil_input, n=1)
        return top[0]["confidence"] if top else 0.0

if __name__ == "__main__":
    predictor = CropPredictor()
    test_soil = SoilInput(N=80, P=45, K=40, ph=6.5, rainfall=220, temperature=24, humidity=82)
    best_crop = predictor.predict_crop(test_soil)
    top_crops = predictor.top_n_crops(test_soil, n=3)
    print(f"Best Crop: {best_crop}")
    print(f"Top 3: {top_crops}")
