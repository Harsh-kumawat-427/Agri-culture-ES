"""
Dataset generator for Crop Recommendation and Fertilizer datasets.
Generates realistic data matching the 2,200 row, 22 crop Kaggle Crop Recommendation dataset
and the fertilizer prediction dataset with crop nutrient targets and soil types.
"""
import os
import numpy as np
import pandas as pd

np.random.seed(42)

# 22 crops with mean and standard deviation for:
# N, P, K, temperature (°C), humidity (%), ph, rainfall (mm)
CROP_PROFILES = {
    "rice": {
        "N": (79.89, 11.9), "P": (47.58, 8.1), "K": (39.87, 3.2),
        "temperature": (23.69, 2.1), "humidity": (82.27, 2.4),
        "ph": (6.43, 0.4), "rainfall": (236.18, 30.2)
    },
    "maize": {
        "N": (77.76, 11.5), "P": (48.44, 7.8), "K": (19.79, 3.1),
        "temperature": (22.39, 2.3), "humidity": (65.09, 5.2),
        "ph": (6.25, 0.4), "rainfall": (84.77, 14.5)
    },
    "chickpea": {
        "N": (40.09, 11.2), "P": (67.79, 7.5), "K": (79.92, 3.2),
        "temperature": (18.87, 1.2), "humidity": (16.86, 1.5),
        "ph": (7.34, 0.5), "rainfall": (80.05, 9.8)
    },
    "kidneybeans": {
        "N": (20.75, 10.8), "P": (67.54, 7.6), "K": (20.05, 3.1),
        "temperature": (20.12, 2.8), "humidity": (21.61, 1.8),
        "ph": (5.75, 0.2), "rainfall": (105.92, 25.1)
    },
    "pigeonpeas": {
        "N": (20.73, 11.4), "P": (67.73, 7.6), "K": (20.29, 3.2),
        "temperature": (27.74, 4.1), "humidity": (48.06, 12.3),
        "ph": (5.79, 0.7), "rainfall": (149.46, 32.6)
    },
    "mothbeans": {
        "N": (21.44, 11.5), "P": (48.01, 7.9), "K": (20.23, 3.2),
        "temperature": (28.19, 2.1), "humidity": (53.16, 8.4),
        "ph": (6.83, 1.2), "rainfall": (51.20, 11.2)
    },
    "mungbean": {
        "N": (20.99, 10.9), "P": (47.28, 7.8), "K": (19.87, 3.1),
        "temperature": (28.53, 0.8), "humidity": (85.50, 2.8),
        "ph": (6.72, 0.3), "rainfall": (48.40, 7.2)
    },
    "blackgram": {
        "N": (40.02, 11.3), "P": (67.47, 7.7), "K": (19.24, 3.1),
        "temperature": (29.98, 2.8), "humidity": (65.12, 2.8),
        "ph": (7.13, 0.4), "rainfall": (67.88, 4.3)
    },
    "lentil": {
        "N": (18.77, 10.9), "P": (68.36, 7.8), "K": (19.41, 3.1),
        "temperature": (24.51, 3.2), "humidity": (64.80, 2.8),
        "ph": (6.93, 0.5), "rainfall": (45.68, 5.8)
    },
    "pomegranate": {
        "N": (18.87, 11.3), "P": (18.75, 4.9), "K": (40.21, 3.1),
        "temperature": (21.84, 1.9), "humidity": (90.13, 2.8),
        "ph": (6.43, 0.4), "rainfall": (107.53, 4.2)
    },
    "banana": {
        "N": (100.23, 11.8), "P": (82.01, 7.8), "K": (50.05, 3.1),
        "temperature": (27.38, 1.4), "humidity": (80.36, 2.8),
        "ph": (5.98, 0.3), "rainfall": (104.63, 8.8)
    },
    "mango": {
        "N": (20.07, 11.3), "P": (27.18, 7.2), "K": (29.92, 3.1),
        "temperature": (31.21, 2.4), "humidity": (50.16, 2.8),
        "ph": (5.77, 0.6), "rainfall": (94.70, 3.8)
    },
    "grapes": {
        "N": (23.18, 11.2), "P": (132.53, 7.5), "K": (200.11, 3.1),
        "temperature": (23.85, 7.8), "humidity": (81.88, 1.8),
        "ph": (6.03, 0.3), "rainfall": (69.61, 3.2)
    },
    "watermelon": {
        "N": (99.42, 11.5), "P": (17.00, 4.8), "K": (50.22, 3.1),
        "temperature": (25.59, 1.2), "humidity": (85.16, 2.8),
        "ph": (6.50, 0.3), "rainfall": (50.79, 5.4)
    },
    "muskmelon": {
        "N": (100.32, 11.2), "P": (17.72, 4.9), "K": (50.08, 3.1),
        "temperature": (28.65, 0.8), "humidity": (92.34, 1.8),
        "ph": (6.36, 0.3), "rainfall": (24.69, 2.8)
    },
    "apple": {
        "N": (20.80, 11.2), "P": (134.22, 7.4), "K": (199.89, 3.1),
        "temperature": (22.63, 1.2), "humidity": (92.33, 1.8),
        "ph": (5.93, 0.3), "rainfall": (112.65, 8.2)
    },
    "orange": {
        "N": (19.58, 11.2), "P": (16.55, 4.8), "K": (10.01, 3.1),
        "temperature": (22.77, 4.8), "humidity": (92.17, 1.8),
        "ph": (7.01, 0.5), "rainfall": (110.47, 4.8)
    },
    "papaya": {
        "N": (49.88, 11.2), "P": (59.05, 7.8), "K": (50.04, 3.1),
        "temperature": (33.72, 4.8), "humidity": (92.40, 1.8),
        "ph": (6.74, 0.2), "rainfall": (142.63, 40.2)
    },
    "coconut": {
        "N": (21.98, 11.2), "P": (16.90, 4.8), "K": (30.05, 3.1),
        "temperature": (27.41, 1.2), "humidity": (94.84, 1.8),
        "ph": (5.98, 0.3), "rainfall": (175.69, 28.5)
    },
    "cotton": {
        "N": (117.77, 11.6), "P": (46.24, 7.8), "K": (19.56, 3.1),
        "temperature": (23.99, 1.2), "humidity": (79.85, 2.8),
        "ph": (6.91, 0.5), "rainfall": (80.40, 11.8)
    },
    "jute": {
        "N": (78.40, 11.2), "P": (46.86, 7.8), "K": (39.99, 3.1),
        "temperature": (24.96, 1.2), "humidity": (79.64, 5.2),
        "ph": (6.73, 0.4), "rainfall": (174.79, 14.8)
    },
    "coffee": {
        "N": (101.20, 11.4), "P": (28.74, 7.2), "K": (29.94, 3.1),
        "temperature": (25.54, 1.8), "humidity": (58.87, 4.8),
        "ph": (6.79, 0.4), "rainfall": (158.07, 24.2)
    }
}

def generate_crop_dataset(output_path, samples_per_crop=100):
    rows = []
    for crop, features in CROP_PROFILES.items():
        for _ in range(samples_per_crop):
            row = {}
            for feat, (mean, std) in features.items():
                val = np.random.normal(mean, std)
                if feat in ["N", "P", "K"]:
                    val = max(0, round(val))
                elif feat == "ph":
                    val = max(3.5, min(9.5, round(val, 2)))
                else:
                    val = max(0, round(val, 2))
                row[feat] = val
            row["label"] = crop
            rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records for {len(CROP_PROFILES)} crops -> {output_path}")
    return df

def generate_fertilizer_dataset(output_path):
    """
    Creates fertilizer knowledge mapping dataset:
    Soil Type, Crop Type, Nitrogen, Phosphorus, Potassium, Recommended Fertilizer, Typical Dosage (kg/ha)
    """
    data = [
        {"soil_type": "Sandy", "crop_type": "Maize", "N": 60, "P": 30, "K": 20, "fertilizer": "Urea", "dosage_kg_ha": 50},
        {"soil_type": "Loamy", "crop_type": "Rice", "N": 50, "P": 40, "K": 40, "fertilizer": "Urea", "dosage_kg_ha": 65},
        {"soil_type": "Clayey", "crop_type": "Cotton", "N": 70, "P": 25, "K": 20, "fertilizer": "NPK 19:19:19", "dosage_kg_ha": 75},
        {"soil_type": "Black", "crop_type": "Chickpea", "N": 20, "P": 45, "K": 30, "fertilizer": "DAP", "dosage_kg_ha": 60},
        {"soil_type": "Red", "crop_type": "Coffee", "N": 50, "P": 15, "K": 20, "fertilizer": "Urea", "dosage_kg_ha": 55},
        {"soil_type": "Alluvial", "crop_type": "Banana", "N": 60, "P": 50, "K": 35, "fertilizer": "MOP", "dosage_kg_ha": 45},
        {"soil_type": "Loamy", "crop_type": "Grapes", "N": 15, "P": 80, "K": 120, "fertilizer": "MOP", "dosage_kg_ha": 70},
        {"soil_type": "Sandy", "crop_type": "Watermelon", "N": 60, "P": 10, "K": 30, "fertilizer": "NPK 19:19:19", "dosage_kg_ha": 50},
        {"soil_type": "Clayey", "crop_type": "Pigeonpeas", "N": 15, "P": 40, "K": 15, "fertilizer": "DAP", "dosage_kg_ha": 50},
        {"soil_type": "Alluvial", "crop_type": "Jute", "N": 45, "P": 30, "K": 25, "fertilizer": "Urea", "dosage_kg_ha": 50},
        {"soil_type": "Loamy", "crop_type": "Apple", "N": 15, "P": 90, "K": 130, "fertilizer": "MOP", "dosage_kg_ha": 80},
        {"soil_type": "Sandy", "crop_type": "Papaya", "N": 30, "P": 35, "K": 30, "fertilizer": "NPK 19:19:19", "dosage_kg_ha": 60},
    ]
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated fertilizer reference dataset -> {output_path}")
    return df

if __name__ == "__main__":
    os.makedirs("crop_expert_system/data", exist_ok=True)
    generate_crop_dataset("crop_expert_system/data/crop.csv")
    generate_fertilizer_dataset("crop_expert_system/data/fertilizer.csv")
