"""
ModelTrainer Module for Crop Recommendation Expert System
Trains Random Forest, Decision Tree, and Naive Bayes classifiers,
evaluates accuracy and confusion matrices, and exports the top-performing
model to a joblib pickle file.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class ModelTrainer:
    def __init__(self, data_path=None, model_dir=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if data_path is None:
            candidates = [
                os.path.join(base_dir, "data", "crop.csv"),
                os.path.join(os.getcwd(), "crop_expert_system", "data", "crop.csv"),
                os.path.join(os.getcwd(), "data", "crop.csv")
            ]
            self.data_path = next((p for p in candidates if os.path.exists(p)), candidates[0])
        else:
            self.data_path = data_path

        if model_dir is None:
            self.model_dir = os.path.join(base_dir, "models")
        else:
            self.model_dir = model_dir
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.results = {}
        self.best_model_name = None
        self.best_model = None

    def load_dataset(self):
        """Loads dataset and verifies integrity."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"[ModelTrainer] Loaded {len(self.df)} rows across {self.df['label'].nunique()} crop classes.")
        missing = self.df.isnull().sum().sum()
        if missing > 0:
            print(f"[ModelTrainer] Found {missing} missing values. Imputing...")
            self.df = self.df.dropna()
        else:
            print("[ModelTrainer] No missing values found in dataset.")
        return self.df

    def preprocess(self):
        """Prepares features and targets with an 80/20 train/test split."""
        feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        X = self.df[feature_cols]
        y = self.df['label']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )
        print(f"[ModelTrainer] Preprocessing complete. Training set: {len(self.X_train)}, Testing set: {len(self.X_test)}")
        return self.X_train, self.X_test, self.y_train, self.y_test

    def train(self):
        """Trains Random Forest, Decision Tree, and Naive Bayes classifiers."""
        self.models = {
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Naive Bayes": GaussianNB()
        }

        print("\n--- Training Machine Learning Models ---")
        best_acc = 0.0
        for name, clf in self.models.items():
            clf.fit(self.X_train, self.y_train)
            y_pred = clf.predict(self.X_test)
            acc = accuracy_score(self.y_test, y_pred)
            self.results[name] = {
                "model": clf,
                "accuracy": acc,
                "report": classification_report(self.y_test, y_pred, output_dict=True),
                "confusion_matrix": confusion_matrix(self.y_test, y_pred).tolist()
            }
            print(f"  > {name} Accuracy: {acc * 100:.2f}%")
            if acc > best_acc:
                best_acc = acc
                self.best_model_name = name
                self.best_model = clf

        print(f"[ModelTrainer] Best model selected: {self.best_model_name} ({best_acc * 100:.2f}%)")
        return self.results

    def evaluate(self):
        """Displays comparative evaluation summary."""
        print("\n=== Model Comparison Summary ===")
        for name, res in self.results.items():
            print(f"Model: {name:<15} | Accuracy: {res['accuracy'] * 100:.2f}%")
        return self.results

    def save_model(self, filename="crop_model.pkl"):
        """Saves best model along with metadata to joblib file."""
        os.makedirs(self.model_dir, exist_ok=True)
        save_path = os.path.join(self.model_dir, filename)
        
        payload = {
            "model": self.best_model,
            "model_name": self.best_model_name,
            "accuracy": self.results[self.best_model_name]["accuracy"],
            "classes": list(self.best_model.classes_),
            "features": ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'],
            "comparison": {k: v["accuracy"] for k, v in self.results.items()}
        }
        joblib.dump(payload, save_path)
        print(f"[ModelTrainer] Successfully saved trained expert model to {save_path}")
        return save_path

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.load_dataset()
    trainer.preprocess()
    trainer.train()
    trainer.evaluate()
    trainer.save_model()
