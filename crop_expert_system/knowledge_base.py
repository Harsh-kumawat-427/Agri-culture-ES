"""
KnowledgeBase Module for Smart Crop & Fertilizer Advisor Expert System.
Stores:
1. Ideal N, P, K, pH ranges, seasonal windows, duration days, and environmental preferences for 22 crops.
2. Standard fertilizer nutrient concentrations (% composition).
3. Production IF-THEN rules for soil nutrient amendments, acidity/alkalinity buffering,
   and combined deficiency resolutions.
4. Agronomic Crop Rotation and Harvest-Gap Compatibility Benchmarks.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import json

@dataclass
class Rule:
    rule_id: str
    condition_desc: str
    target_nutrient: str
    suggested_fertilizer: str
    advice: str
    priority: int
    rule_type: str = "deficiency"  # deficiency, soil_ph, balanced

class KnowledgeBase:
    """Holds agronomic rules and nutrient benchmark requirements for crops."""

    def __init__(self):
        self.crop_requirements: Dict[str, Dict[str, Any]] = self._init_crop_requirements()
        self.fertilizers: Dict[str, Dict[str, Any]] = self._init_fertilizers()
        self.rules: List[Rule] = self._init_rules()

    def _init_crop_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Ideal benchmark ranges for N, P, K (kg/ha), pH, duration, seasons, and soils for 22 crops."""
        return {
            "mungbean": {
                "display_name": "Mung Bean (Green Gram)",
                "category": "Pulses / Short-Duration Catch Crop",
                "ideal_N": 21, "N_min": 10, "N_max": 40,
                "ideal_P": 47, "P_min": 35, "P_max": 60,
                "ideal_K": 20, "K_min": 15, "K_max": 25,
                "ideal_ph": 6.7, "ph_min": 6.0, "ph_max": 7.5,
                "ideal_rainfall_mm": 48,
                "ideal_temp_c": 28, "temp_min": 22, "temp_max": 38,
                "growth_duration_days": "60 - 75 days",
                "duration_min_days": 60, "duration_max_days": 75,
                "season": "Zaid (Summer) / Kharif (Monsoon)",
                "suitable_seasons": ["Zaid", "Kharif", "Spring", "Catch Crop"],
                "suitable_soils": ["Loamy", "Sandy", "Alluvial", "Clayey"],
                "rotation_role": "Nitrogen Fixer (Rhizobium)",
                "rotation_benefits": "Excellent short catch crop that fits tightly between two cereal crops, fixing 30-40 kg N/ha into the soil.",
                "notes": "Shortest duration legume, ideal catch crop to fill short harvest gaps."
            },
            "mothbeans": {
                "display_name": "Moth Beans (Matki)",
                "category": "Pulses / Arid Catch Crop",
                "ideal_N": 21, "N_min": 10, "N_max": 40,
                "ideal_P": 48, "P_min": 35, "P_max": 60,
                "ideal_K": 20, "K_min": 15, "K_max": 25,
                "ideal_ph": 6.8, "ph_min": 5.5, "ph_max": 8.0,
                "ideal_rainfall_mm": 50,
                "ideal_temp_c": 28, "temp_min": 24, "temp_max": 38,
                "growth_duration_days": "65 - 80 days",
                "duration_min_days": 65, "duration_max_days": 80,
                "season": "Kharif (Monsoon) / Summer",
                "suitable_seasons": ["Kharif", "Zaid", "Summer"],
                "suitable_soils": ["Sandy", "Loamy", "Red"],
                "rotation_role": "Nitrogen Fixer & Soil Cover",
                "rotation_benefits": "Prevents soil erosion in arid soils, restores nitrogen, thrives in dry windows.",
                "notes": "Highly drought resistant crop suitable for arid and sandy desert belts."
            },
            "muskmelon": {
                "display_name": "Muskmelon (Cantaloupe)",
                "category": "Cucurbit / Summer Cash Crop",
                "ideal_N": 100, "N_min": 80, "N_max": 120,
                "ideal_P": 18, "P_min": 10, "P_max": 30,
                "ideal_K": 50, "K_min": 45, "K_max": 55,
                "ideal_ph": 6.4, "ph_min": 6.0, "ph_max": 7.5,
                "ideal_rainfall_mm": 25,
                "ideal_temp_c": 28, "temp_min": 24, "temp_max": 36,
                "growth_duration_days": "70 - 85 days",
                "duration_min_days": 70, "duration_max_days": 85,
                "season": "Zaid (Summer)",
                "suitable_seasons": ["Zaid", "Spring", "Summer"],
                "suitable_soils": ["Sandy", "Loamy", "Alluvial"],
                "rotation_role": "Short-Cycle Commercial Fruit",
                "rotation_benefits": "High market value cash crop fitting between Rabi harvest and Kharif sowing.",
                "notes": "Thrives under hot dry summer conditions; requires high nitrogen in early stages."
            },
            "watermelon": {
                "display_name": "Watermelon",
                "category": "Cucurbit / Summer Fruit",
                "ideal_N": 99, "N_min": 80, "N_max": 120,
                "ideal_P": 17, "P_min": 10, "P_max": 30,
                "ideal_K": 50, "K_min": 45, "K_max": 55,
                "ideal_ph": 6.5, "ph_min": 6.0, "ph_max": 7.2,
                "ideal_rainfall_mm": 50,
                "ideal_temp_c": 26, "temp_min": 22, "temp_max": 36,
                "growth_duration_days": "75 - 90 days",
                "duration_min_days": 75, "duration_max_days": 90,
                "season": "Zaid (Summer)",
                "suitable_seasons": ["Zaid", "Summer", "Spring"],
                "suitable_soils": ["Sandy", "Loamy", "Alluvial"],
                "rotation_role": "Short-Cycle Cash Crop",
                "rotation_benefits": "Quick return summer crop utilizing sandy riverbeds and post-harvest fields.",
                "notes": "Prefers warm sandy loam with good drainage. Needs moderate moisture."
            },
            "blackgram": {
                "display_name": "Black Gram (Urad)",
                "category": "Pulses / Soil Restorer",
                "ideal_N": 40, "N_min": 20, "N_max": 60,
                "ideal_P": 67, "P_min": 55, "P_max": 80,
                "ideal_K": 19, "K_min": 15, "K_max": 25,
                "ideal_ph": 7.1, "ph_min": 6.5, "ph_max": 7.8,
                "ideal_rainfall_mm": 68,
                "ideal_temp_c": 30, "temp_min": 25, "temp_max": 38,
                "growth_duration_days": "70 - 90 days",
                "duration_min_days": 70, "duration_max_days": 90,
                "season": "Kharif (Monsoon) / Summer",
                "suitable_seasons": ["Kharif", "Zaid", "Spring"],
                "suitable_soils": ["Loamy", "Clayey", "Black"],
                "rotation_role": "Nitrogen Fixer (Rhizobium)",
                "rotation_benefits": "Improves soil physical structure and enriches residual soil nitrogen for next cereals.",
                "notes": "Prefers well-drained loam and warm humid climates."
            },
            "maize": {
                "display_name": "Maize (Corn)",
                "category": "Cereal / Versatile Grain",
                "ideal_N": 78, "N_min": 60, "N_max": 100,
                "ideal_P": 48, "P_min": 35, "P_max": 60,
                "ideal_K": 20, "K_min": 15, "K_max": 25,
                "ideal_ph": 6.2, "ph_min": 5.5, "ph_max": 7.5,
                "ideal_rainfall_mm": 85,
                "ideal_temp_c": 23, "temp_min": 18, "temp_max": 32,
                "growth_duration_days": "80 - 110 days",
                "duration_min_days": 80, "duration_max_days": 110,
                "season": "Kharif / Rabi / Zaid (All Seasons)",
                "suitable_seasons": ["Kharif", "Rabi", "Zaid", "All Year"],
                "suitable_soils": ["Loamy", "Alluvial", "Black", "Red"],
                "rotation_role": "High-Yield Cereal Feed",
                "rotation_benefits": "Produces high biomass; breaks pulse pest cycles when rotated with legumes.",
                "notes": "Fast growing, heavy feeder of nitrogen and phosphorus for cob formation."
            },
            "chickpea": {
                "display_name": "Chickpea (Gram)",
                "category": "Pulses / Winter Legume",
                "ideal_N": 40, "N_min": 20, "N_max": 60,
                "ideal_P": 68, "P_min": 55, "P_max": 80,
                "ideal_K": 80, "K_min": 70, "K_max": 90,
                "ideal_ph": 7.3, "ph_min": 6.0, "ph_max": 8.5,
                "ideal_rainfall_mm": 80,
                "ideal_temp_c": 19, "temp_min": 12, "temp_max": 26,
                "growth_duration_days": "90 - 120 days",
                "duration_min_days": 90, "duration_max_days": 120,
                "season": "Rabi (Winter)",
                "suitable_seasons": ["Rabi", "Winter"],
                "suitable_soils": ["Loamy", "Black", "Clayey"],
                "rotation_role": "Soil Rejuvenator (High N-Fixation)",
                "rotation_benefits": "Premier winter pulse to rotate after Kharif Rice or Maize; replenishes soil nitrogen naturally.",
                "notes": "Fixes atmospheric nitrogen via Rhizobium root nodules. Needs cool winter weather."
            },
            "kidneybeans": {
                "display_name": "Kidney Beans (Rajma)",
                "category": "Pulses",
                "ideal_N": 21, "N_min": 10, "N_max": 40,
                "ideal_P": 67, "P_min": 55, "P_max": 80,
                "ideal_K": 20, "K_min": 15, "K_max": 25,
                "ideal_ph": 5.8, "ph_min": 5.3, "ph_max": 6.5,
                "ideal_rainfall_mm": 105,
                "ideal_temp_c": 20, "temp_min": 14, "temp_max": 26,
                "growth_duration_days": "100 - 130 days",
                "duration_min_days": 100, "duration_max_days": 130,
                "season": "Rabi / Spring",
                "suitable_seasons": ["Rabi", "Spring"],
                "suitable_soils": ["Loamy", "Alluvial"],
                "rotation_role": "High-Value Pulse",
                "rotation_benefits": "Excellent companion in cool season rotations.",
                "notes": "Responds well to early phosphorus fertilization."
            },
            "lentil": {
                "display_name": "Lentil (Masoor)",
                "category": "Pulses / Winter Legume",
                "ideal_N": 19, "N_min": 10, "N_max": 40,
                "ideal_P": 68, "P_min": 55, "P_max": 80,
                "ideal_K": 19, "K_min": 15, "K_max": 25,
                "ideal_ph": 6.9, "ph_min": 6.0, "ph_max": 7.8,
                "ideal_rainfall_mm": 45,
                "ideal_temp_c": 24, "temp_min": 14, "temp_max": 28,
                "growth_duration_days": "100 - 130 days",
                "duration_min_days": 100, "duration_max_days": 130,
                "season": "Rabi (Winter)",
                "suitable_seasons": ["Rabi", "Winter"],
                "suitable_soils": ["Loamy", "Alluvial", "Clayey"],
                "rotation_role": "Nitrogen Fixer",
                "rotation_benefits": "Thrives on residual moisture after paddy harvest; enriches organic nitrogen.",
                "notes": "Cool season legume; sensitive to waterlogging."
            },
            "rice": {
                "display_name": "Rice (Paddy)",
                "category": "Cereal / Main Kharif Staple",
                "ideal_N": 80, "N_min": 60, "N_max": 100,
                "ideal_P": 48, "P_min": 35, "P_max": 60,
                "ideal_K": 40, "K_min": 35, "K_max": 45,
                "ideal_ph": 6.5, "ph_min": 5.5, "ph_max": 7.2,
                "ideal_rainfall_mm": 230,
                "ideal_temp_c": 24, "temp_min": 20, "temp_max": 35,
                "growth_duration_days": "110 - 150 days",
                "duration_min_days": 110, "duration_max_days": 150,
                "season": "Kharif (Monsoon)",
                "suitable_seasons": ["Kharif", "Monsoon"],
                "suitable_soils": ["Clayey", "Alluvial", "Loamy"],
                "rotation_role": "Primary Cereal Crop",
                "rotation_benefits": "Foundation of Rice-Wheat and Rice-Pulse cropping systems.",
                "notes": "Requires standing water and high nitrogen during vegetative growth."
            },
            "jute": {
                "display_name": "Jute (Golden Fiber)",
                "category": "Fiber / Monsoon Cash Crop",
                "ideal_N": 78, "N_min": 60, "N_max": 100,
                "ideal_P": 47, "P_min": 35, "P_max": 60,
                "ideal_K": 40, "K_min": 35, "K_max": 45,
                "ideal_ph": 6.7, "ph_min": 6.0, "ph_max": 7.5,
                "ideal_rainfall_mm": 175,
                "ideal_temp_c": 25, "temp_min": 22, "temp_max": 35,
                "growth_duration_days": "120 - 150 days",
                "duration_min_days": 120, "duration_max_days": 150,
                "season": "Kharif (Monsoon)",
                "suitable_seasons": ["Kharif", "Monsoon"],
                "suitable_soils": ["Alluvial", "Clayey", "Loamy"],
                "rotation_role": "Cash Fiber Crop",
                "rotation_benefits": "Foliage leaf drop adds substantial organic humus to delta soils.",
                "notes": "Requires high humidity, standing water, and heavy monsoon rains."
            },
            "cotton": {
                "display_name": "Cotton",
                "category": "Fiber / Cash Crop",
                "ideal_N": 118, "N_min": 100, "N_max": 140,
                "ideal_P": 46, "P_min": 35, "P_max": 60,
                "ideal_K": 20, "K_min": 15, "K_max": 25,
                "ideal_ph": 6.9, "ph_min": 6.0, "ph_max": 8.0,
                "ideal_rainfall_mm": 80,
                "ideal_temp_c": 24, "temp_min": 21, "temp_max": 35,
                "growth_duration_days": "150 - 180 days",
                "duration_min_days": 150, "duration_max_days": 180,
                "season": "Kharif (Monsoon)",
                "suitable_seasons": ["Kharif"],
                "suitable_soils": ["Black", "Alluvial", "Loamy"],
                "rotation_role": "Long-Cycle Cash Crop",
                "rotation_benefits": "Deep root penetration aerates dense black soils; rotate with pulse crops.",
                "notes": "Highest nitrogen consumer; requires warm weather and dry boll maturity."
            },
            "pigeonpeas": {
                "display_name": "Pigeonpeas (Arhar / Tur)",
                "category": "Pulses / Semi-Arid Legume",
                "ideal_N": 21, "N_min": 10, "N_max": 40,
                "ideal_P": 68, "P_min": 55, "P_max": 80,
                "ideal_K": 20, "K_min": 15, "K_max": 25,
                "ideal_ph": 6.0, "ph_min": 5.0, "ph_max": 7.5,
                "ideal_rainfall_mm": 150,
                "ideal_temp_c": 28, "temp_min": 20, "temp_max": 36,
                "growth_duration_days": "150 - 200 days",
                "duration_min_days": 150, "duration_max_days": 200,
                "season": "Kharif (Monsoon to Winter)",
                "suitable_seasons": ["Kharif"],
                "suitable_soils": ["Loamy", "Black", "Clayey", "Red"],
                "rotation_role": "Deep-Rooted Nitrogen Fixer",
                "rotation_benefits": "Extensive taproot system mines subsoil phosphorus and fixes massive nitrogen.",
                "notes": "Deep taproot, drought tolerant, thrives in semi-arid conditions."
            },
            "banana": {
                "display_name": "Banana",
                "category": "Fruit / Plantation",
                "ideal_N": 100, "N_min": 80, "N_max": 120,
                "ideal_P": 82, "P_min": 70, "P_max": 95,
                "ideal_K": 50, "K_min": 45, "K_max": 55,
                "ideal_ph": 6.0, "ph_min": 5.5, "ph_max": 6.8,
                "ideal_rainfall_mm": 105,
                "ideal_temp_c": 27, "temp_min": 20, "temp_max": 35,
                "growth_duration_days": "10 - 12 months",
                "duration_min_days": 300, "duration_max_days": 365,
                "season": "Year-Round / Perennial",
                "suitable_seasons": ["All Year", "Perennial"],
                "suitable_soils": ["Alluvial", "Loamy", "Clayey"],
                "rotation_role": "Annual Plantation",
                "rotation_benefits": "High income annual crop requiring dedicated field for full calendar year.",
                "notes": "Heavy consumer of potassium and nitrogen. Requires constant moisture."
            },
            "papaya": {
                "display_name": "Papaya",
                "category": "Tropical Fruit",
                "ideal_N": 50, "N_min": 30, "N_max": 70,
                "ideal_P": 59, "P_min": 45, "P_max": 75,
                "ideal_K": 50, "K_min": 45, "K_max": 55,
                "ideal_ph": 6.7, "ph_min": 6.0, "ph_max": 7.2,
                "ideal_rainfall_mm": 142,
                "ideal_temp_c": 33, "temp_min": 22, "temp_max": 38,
                "growth_duration_days": "9 - 12 months",
                "duration_min_days": 270, "duration_max_days": 365,
                "season": "Tropical Year-Round",
                "suitable_seasons": ["All Year", "Perennial"],
                "suitable_soils": ["Loamy", "Sandy", "Alluvial"],
                "rotation_role": "Short Perennial Fruit",
                "rotation_benefits": "Continuous commercial yield; susceptible to waterlogging.",
                "notes": "Fast growing herbaceous plant; susceptible to frost."
            },
            "grapes": {
                "display_name": "Grapes (Vineyard)",
                "category": "Viticulture / Perennial",
                "ideal_N": 23, "N_min": 10, "N_max": 40,
                "ideal_P": 132, "P_min": 120, "P_max": 145,
                "ideal_K": 200, "K_min": 180, "K_max": 220,
                "ideal_ph": 6.0, "ph_min": 5.5, "ph_max": 6.8,
                "ideal_rainfall_mm": 70,
                "ideal_temp_c": 24, "temp_min": 15, "temp_max": 35,
                "growth_duration_days": "Perennial vine",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Loamy", "Sandy", "Red"],
                "rotation_role": "Permanent Vineyard",
                "rotation_benefits": "High long-term capital crop.",
                "notes": "High potassium and phosphorus demand for berry sugar content."
            },
            "apple": {
                "display_name": "Apple",
                "category": "Temperate Fruit / Orchard",
                "ideal_N": 21, "N_min": 10, "N_max": 40,
                "ideal_P": 134, "P_min": 120, "P_max": 145,
                "ideal_K": 200, "K_min": 180, "K_max": 220,
                "ideal_ph": 5.9, "ph_min": 5.5, "ph_max": 6.5,
                "ideal_rainfall_mm": 112,
                "ideal_temp_c": 22, "temp_min": 5, "temp_max": 26,
                "growth_duration_days": "Perennial orchard",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Temperate Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Loamy", "Alluvial"],
                "rotation_role": "Permanent Orchard",
                "rotation_benefits": "Cool hilly terrain permanent establishment.",
                "notes": "Requires winter chilling hours for dormancy break."
            },
            "orange": {
                "display_name": "Orange (Citrus)",
                "category": "Citrus Fruit / Orchard",
                "ideal_N": 20, "N_min": 10, "N_max": 40,
                "ideal_P": 17, "P_min": 10, "P_max": 30,
                "ideal_K": 10, "K_min": 5, "K_max": 20,
                "ideal_ph": 7.0, "ph_min": 6.0, "ph_max": 8.0,
                "ideal_rainfall_mm": 110,
                "ideal_temp_c": 23, "temp_min": 15, "temp_max": 34,
                "growth_duration_days": "Perennial orchard",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Subtropical Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Loamy", "Black", "Alluvial"],
                "rotation_role": "Permanent Citrus Orchard",
                "rotation_benefits": "Deep root soil stabilization.",
                "notes": "Requires well-aerated soil and balanced micronutrients."
            },
            "pomegranate": {
                "display_name": "Pomegranate",
                "category": "Horticulture / Fruit",
                "ideal_N": 20, "N_min": 15, "N_max": 40,
                "ideal_P": 20, "P_min": 10, "P_max": 30,
                "ideal_K": 40, "K_min": 35, "K_max": 45,
                "ideal_ph": 6.4, "ph_min": 5.5, "ph_max": 7.2,
                "ideal_rainfall_mm": 107,
                "ideal_temp_c": 22, "temp_min": 16, "temp_max": 36,
                "growth_duration_days": "Perennial orchard",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Loamy", "Black", "Sandy", "Red"],
                "rotation_role": "Permanent Dryland Fruit",
                "rotation_benefits": "Tolerates salinity and drought.",
                "notes": "Sub-tropical fruit requiring dry climate during fruit ripening."
            },
            "mango": {
                "display_name": "Mango",
                "category": "Fruit / Orchard",
                "ideal_N": 20, "N_min": 10, "N_max": 40,
                "ideal_P": 27, "P_min": 15, "P_max": 40,
                "ideal_K": 30, "K_min": 25, "K_max": 35,
                "ideal_ph": 5.8, "ph_min": 5.0, "ph_max": 7.0,
                "ideal_rainfall_mm": 95,
                "ideal_temp_c": 31, "temp_min": 22, "temp_max": 40,
                "growth_duration_days": "Perennial tree",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Alluvial", "Loamy", "Red"],
                "rotation_role": "Permanent Tree Crop",
                "rotation_benefits": "Agro-forestry canopy stabilization.",
                "notes": "Deep rooted evergreen tree; prefers clear sunny weather during flowering."
            },
            "coconut": {
                "display_name": "Coconut Palm",
                "category": "Plantation",
                "ideal_N": 22, "N_min": 10, "N_max": 40,
                "ideal_P": 17, "P_min": 10, "P_max": 30,
                "ideal_K": 30, "K_min": 25, "K_max": 35,
                "ideal_ph": 6.0, "ph_min": 5.2, "ph_max": 7.5,
                "ideal_rainfall_mm": 175,
                "ideal_temp_c": 27, "temp_min": 22, "temp_max": 36,
                "growth_duration_days": "Perennial palm",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Coastal Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Sandy", "Alluvial", "Red"],
                "rotation_role": "Coastal Plantation",
                "rotation_benefits": "Allows multi-tier intercropping underneath palm canopy.",
                "notes": "Coastal palm thriving in sandy coastal plains with high humidity."
            },
            "coffee": {
                "display_name": "Coffee (Arabica / Robusta)",
                "category": "Beverage / Plantation",
                "ideal_N": 101, "N_min": 80, "N_max": 120,
                "ideal_P": 29, "P_min": 15, "P_max": 40,
                "ideal_K": 30, "K_min": 25, "K_max": 35,
                "ideal_ph": 6.8, "ph_min": 5.8, "ph_max": 7.2,
                "ideal_rainfall_mm": 158,
                "ideal_temp_c": 25, "temp_min": 16, "temp_max": 30,
                "growth_duration_days": "Perennial shrub",
                "duration_min_days": 365, "duration_max_days": 365,
                "season": "Hill Perennial",
                "suitable_seasons": ["Perennial"],
                "suitable_soils": ["Red", "Loamy", "Alluvial"],
                "rotation_role": "Shade Plantation",
                "rotation_benefits": "Integrated hill agro-ecosystem.",
                "notes": "Shade-tolerant sub-tropical shrub needing rich volcanic/loamy soils."
            }
        }

    def _init_fertilizers(self) -> Dict[str, Dict[str, Any]]:
        """Fertilizer composition details, nutrient percentage, and typical application forms."""
        return {
            "Urea": {
                "name": "Urea",
                "formula": "CO(NH2)2",
                "primary_nutrient": "N",
                "n_percent": 46.0,
                "p_percent": 0.0,
                "k_percent": 0.0,
                "description": "High-concentration nitrogenous granular fertilizer for vigorous vegetative and canopy growth."
            },
            "DAP": {
                "name": "DAP (Di-Ammonium Phosphate)",
                "formula": "(NH4)2HPO4",
                "primary_nutrient": "P",
                "n_percent": 18.0,
                "p_percent": 46.0,
                "k_percent": 0.0,
                "description": "Widely used phosphatic fertilizer providing immediate root stimulation and starter nitrogen."
            },
            "SSP": {
                "name": "SSP (Single Super Phosphate)",
                "formula": "Ca(H2PO4)2 + CaSO4",
                "primary_nutrient": "P",
                "n_percent": 0.0,
                "p_percent": 16.0,
                "k_percent": 0.0,
                "description": "Supplies water-soluble phosphate plus 11% sulphur and 19% calcium for root development."
            },
            "MOP": {
                "name": "MOP (Muriate of Potash / Potassium Chloride)",
                "formula": "KCl",
                "primary_nutrient": "K",
                "n_percent": 0.0,
                "p_percent": 0.0,
                "k_percent": 60.0,
                "description": "Standard potassic fertilizer enhancing drought resistance, disease tolerance, and crop yield quality."
            },
            "NPK 19:19:19": {
                "name": "NPK 19:19:19",
                "formula": "Complex 1:1:1",
                "primary_nutrient": "NPK",
                "n_percent": 19.0,
                "p_percent": 19.0,
                "k_percent": 19.0,
                "description": "Fully balanced multi-nutrient complex for simultaneous nitrogen, phosphorus, and potassium correction."
            },
            "Agricultural Lime": {
                "name": "Agricultural Lime (Calcium Carbonate)",
                "formula": "CaCO3",
                "primary_nutrient": "pH Buffer",
                "n_percent": 0.0,
                "p_percent": 0.0,
                "k_percent": 0.0,
                "description": "Reduces soil acidity, raises pH, and improves microbial activity in soils below pH 5.5."
            },
            "Agricultural Gypsum": {
                "name": "Agricultural Gypsum (Calcium Sulfate)",
                "formula": "CaSO4·2H2O",
                "primary_nutrient": "pH Buffer / Sulphur",
                "n_percent": 0.0,
                "p_percent": 0.0,
                "k_percent": 0.0,
                "description": "Reclaims sodic/alkaline soils above pH 8.0 by displacing excess sodium with calcium."
            }
        }

    def _init_rules(self) -> List[Rule]:
        """Loads canonical production rules as designated in project specification."""
        return [
            Rule(
                rule_id="R01_ALL_DEFICIENT",
                condition_desc="Nitrogen, Phosphorus, and Potassium are all significantly below crop benchmarks",
                target_nutrient="NPK",
                suggested_fertilizer="NPK 19:19:19",
                advice="Soil shows concurrent multi-nutrient deficiency. Apply balanced NPK 19:19:19 as basal dressing.",
                priority=100,
                rule_type="balanced"
            ),
            Rule(
                rule_id="R02_N_LOW",
                condition_desc="Soil Nitrogen (N) is below the recommended minimum threshold for the crop",
                target_nutrient="N",
                suggested_fertilizer="Urea",
                advice="Nitrogen deficiency detected. Apply Urea in split doses to accelerate leaf chlorophyll and vegetative biomass.",
                priority=80,
                rule_type="deficiency"
            ),
            Rule(
                rule_id="R03_P_LOW",
                condition_desc="Soil Phosphorus (P) is below the crop's minimum root establishment requirement",
                target_nutrient="P",
                suggested_fertilizer="DAP",
                advice="Phosphorus deficiency detected. Apply DAP or SSP close to root zone to spur deep rooting and early flower initiation.",
                priority=75,
                rule_type="deficiency"
            ),
            Rule(
                rule_id="R04_K_LOW",
                condition_desc="Soil Potassium (K) is below the crop's physiological resilience threshold",
                target_nutrient="K",
                suggested_fertilizer="MOP",
                advice="Potassium deficit found. Apply MOP (Muriate of Potash) to reinforce stalk strength, fruit filling, and osmotic drought resistance.",
                priority=70,
                rule_type="deficiency"
            ),
            Rule(
                rule_id="R05_PH_ACIDIC",
                condition_desc="Soil pH is below 5.5 (strongly acidic)",
                target_nutrient="pH",
                suggested_fertilizer="Agricultural Lime",
                advice="Acidic soil condition (pH < 5.5) inhibits phosphorus and cation uptake. Broadcast agricultural lime (CaCO3) 2-3 weeks prior to sowing.",
                priority=90,
                rule_type="soil_ph"
            ),
            Rule(
                rule_id="R06_PH_ALKALINE",
                condition_desc="Soil pH is above 8.0 (strongly alkaline / sodic)",
                target_nutrient="pH",
                suggested_fertilizer="Agricultural Gypsum",
                advice="Alkaline/saline condition (pH > 8.0) locks iron and zinc. Incorporate Gypsum or elemental sulphur to lower soil pH and leach sodium.",
                priority=90,
                rule_type="soil_ph"
            ),
            Rule(
                rule_id="R07_BALANCED_SOIL",
                condition_desc="All nutrients (N, P, K) and pH meet or exceed crop requirements",
                target_nutrient="None",
                suggested_fertilizer="No Chemical Fertilizer Required",
                advice="Soil nutrient profile is optimal for this crop. Maintain soil organic matter with farmyard compost (FYM) or green manuring.",
                priority=50,
                rule_type="balanced"
            ),
            Rule(
                rule_id="R08_NP_DEFICIENT",
                condition_desc="Nitrogen and Phosphorus are both deficient while Potassium is adequate",
                target_nutrient="NP",
                suggested_fertilizer="DAP (18-46-0) + Topdress Urea",
                advice="Dual N & P deficiency detected. Apply Diammonium Phosphate (DAP) at basal sowing to stimulate early root vigor, followed by topdressed Urea.",
                priority=85,
                rule_type="deficiency"
            ),
            Rule(
                rule_id="R09_NK_DEFICIENT",
                condition_desc="Nitrogen and Potassium are both deficient while Phosphorus is adequate",
                target_nutrient="NK",
                suggested_fertilizer="Potassium Nitrate (13-0-45) or Urea + MOP blend",
                advice="Dual N & K deficiency detected. Apply split Urea for vegetative chlorophyll and MOP to strengthen stem lodging resistance.",
                priority=85,
                rule_type="deficiency"
            ),
            Rule(
                rule_id="R10_PK_DEFICIENT",
                condition_desc="Phosphorus and Potassium are both deficient while Nitrogen is adequate (common in legumes)",
                target_nutrient="PK",
                suggested_fertilizer="Monopotassium Phosphate (MKP 00:52:34) / SSP + MOP",
                advice="Dual P & K deficit found. Apply Single Super Phosphate (SSP) with MOP prior to flowering to spur root nodulation and flower retention.",
                priority=85,
                rule_type="deficiency"
            ),
            Rule(
                rule_id="R11_N_EXCESS",
                condition_desc="Soil Nitrogen exceeds maximum safe benchmark by > 25% (Nitrogen luxury consumption)",
                target_nutrient="N_Toxicity",
                suggested_fertilizer="Withhold Nitrogen Fertilizers / Leach with Water",
                advice="Excessive soil nitrogen leads to succulent weak stems, pest/aphid vulnerability, and delayed maturity. Withhold nitrogen fertilizers immediately.",
                priority=78,
                rule_type="toxicity"
            ),
            Rule(
                rule_id="R12_P_EXCESS",
                condition_desc="Soil Phosphorus is excessively high (> 30% above maximum benchmark)",
                target_nutrient="P_Toxicity",
                suggested_fertilizer="Chelated Zinc (Zn-EDTA) Foliar Spray",
                advice="Excess phosphorus induces iron and zinc ion lockout, causing interveinal leaf chlorosis. Avoid phosphatic fertilizers and spray Chelated Zinc.",
                priority=74,
                rule_type="toxicity"
            ),
            Rule(
                rule_id="R13_DROUGHT_HEAT_STRESS",
                condition_desc="Precipitation < 60 mm and Ambient Temperature > 30°C (Moisture Deficit & Thermal Stress)",
                target_nutrient="Climate_Stress",
                suggested_fertilizer="Foliar Potassium (1% KNO3) & Organic Straw Mulch",
                advice="High heat and low rainfall trigger rapid moisture loss. Spray 1% Potassium Nitrate or MOP to close stomata and spread organic crop mulch.",
                priority=92,
                rule_type="climate"
            ),
            Rule(
                rule_id="R14_WATERLOGGING_EXCESS_RAIN",
                condition_desc="Precipitation > 220 mm with heavy soil (Waterlogging & Leaching Risk)",
                target_nutrient="Drainage_Nitrogen",
                suggested_fertilizer="Ridge & Furrow Drainage + Post-Drainage Urea",
                advice="Excess rainfall risks root asphyxiation and nitrogen denitrification. Create field drainage trenches and apply foliar Urea post-drainage.",
                priority=91,
                rule_type="climate"
            ),
            Rule(
                rule_id="R15_COLD_CHILLING_STRESS",
                condition_desc="Ambient Temperature < 15°C during critical growth stages (Frost & Chilling Risk)",
                target_nutrient="Thermal_Stress",
                suggested_fertilizer="Potassium Silicate Foliar Spray & Light Evening Irrigation",
                advice="Low temperature (< 15°C) slows root cation uptake. Provide light evening irrigation and spray potassium silicate to protect cell membranes.",
                priority=88,
                rule_type="climate"
            ),
            Rule(
                rule_id="R16_SULPHUR_DEFICIT_OILSEEDS",
                condition_desc="Oilseed or pulse crop planted with low fertility (Sulphur requirement for oil/protein)",
                target_nutrient="Sulphur",
                suggested_fertilizer="Agricultural Gypsum or Bentonite Sulphur (25 kg/ha)",
                advice="Oilseed and pulse crops require high sulphur for oil synthesis and nodule protein. Apply 25 kg/ha agricultural gypsum or elemental sulphur.",
                priority=76,
                rule_type="micronutrient"
            ),
            Rule(
                rule_id="R17_ZINC_DEFICIENCY_CALCAREOUS",
                condition_desc="Alkaline / Calcareous soil (pH > 7.8) with high phosphorus (Zinc fixation)",
                target_nutrient="Zinc",
                suggested_fertilizer="Zinc Sulphate Heptahydrate (ZnSO4 21%)",
                advice="High soil pH immobilizes zinc, triggering Khaira disease in paddy or white bud in maize. Broadcast 25 kg/ha Zinc Sulphate or spray 0.5% ZnSO4.",
                priority=82,
                rule_type="micronutrient"
            ),
            Rule(
                rule_id="R18_PULSE_ROTATION_SYNERGY",
                condition_desc="Rotation following high-nitrogen cereal crop (Rice, Wheat, Maize)",
                target_nutrient="Soil_Regeneration",
                suggested_fertilizer="Rhizobium Bio-fertilizer Seed Inoculation",
                advice="Continuous cereal farming exhausts soil nitrogen. Inoculate legume seeds with Rhizobium culture to fix 35-50 kg/ha atmospheric nitrogen.",
                priority=86,
                rule_type="rotation"
            ),
            Rule(
                rule_id="R19_SHORT_GAP_CATCH_CROP",
                condition_desc="Fallow harvest gap between two main crops is short (60 - 85 days)",
                target_nutrient="Harvest_Window",
                suggested_fertilizer="Starter DAP (18-46-0) for Fast Catch Crop",
                advice="Short fallow gap requires quick-maturing catch crops (Mungbean, Cowpea, Mothbeans). Apply starter DAP to accelerate early flowering.",
                priority=89,
                rule_type="rotation"
            ),
            Rule(
                rule_id="R20_ORGANIC_CARBON_RESTORATION",
                condition_desc="Soil Nitrogen is critically depleted (< 35 kg/ha) indicating low soil organic matter",
                target_nutrient="Soil_Carbon",
                suggested_fertilizer="Well-Decomposed Farmyard Manure (FYM 8-10 t/ha)",
                advice="Critically low nitrogen indicates depleted soil organic carbon (< 0.4%). Incorporate 8-10 tonnes/ha FYM or compost to rebuild microbial life.",
                priority=84,
                rule_type="organic"
            ),
            Rule(
                rule_id="R21_MICRONUTRIENT_BORON_DEFICIT",
                condition_desc="Fruit and horticultural crops in light/leached soils (Boron deficit risk)",
                target_nutrient="Boron",
                suggested_fertilizer="Borax (10 kg/ha) or Solubor Foliar Spray (0.1%)",
                advice="Horticultural crops require boron for pollen viability and fruit setting. Apply 10 kg/ha Borax or spray 0.1% Solubor at flower bud initiation.",
                priority=72,
                rule_type="micronutrient"
            ),
            Rule(
                rule_id="R22_SALINE_SOIL_REMEDY",
                condition_desc="Saline or sodic soil condition (pH 7.5 - 8.3 with low rainfall / poor drainage)",
                target_nutrient="Salinity",
                suggested_fertilizer="Green Manuring with Dhaincha (Sesbania) + Leaching",
                advice="High salinity inhibits root water absorption. Sow Sesbania (Dhaincha) green manure at 20 kg/ha seed rate and incorporate into soil at 45 days.",
                priority=79,
                rule_type="soil_ph"
            )
        ]

    def add_rule(self, rule: Rule):
        """Allows dynamic rule expansion to the knowledge base."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def get_rules(self) -> List[Rule]:
        return self.rules

    def get_crop_requirements(self, crop: str) -> Optional[Dict[str, Any]]:
        if not crop:
            return None
        c = crop.lower().strip()
        if c in self.crop_requirements:
            return self.crop_requirements[c]
        # Match by display name or partial name
        for k, v in self.crop_requirements.items():
            disp = v.get("display_name", "").lower().strip()
            if c == disp or c in disp or disp in c:
                return v
            if k in c or c in k:
                return v
        return None

    def get_fertilizer(self, name: str) -> Optional[Dict[str, Any]]:
        return self.fertilizers.get(name)

    def get_all_crops(self) -> List[str]:
        return sorted(list(self.crop_requirements.keys()))

    def to_json(self) -> str:
        data = {
            "crops": self.crop_requirements,
            "fertilizers": self.fertilizers,
            "rules": [
                {
                    "rule_id": r.rule_id,
                    "condition": r.condition_desc,
                    "target_nutrient": r.target_nutrient,
                    "fertilizer": r.suggested_fertilizer,
                    "advice": r.advice,
                    "priority": r.priority,
                    "type": r.rule_type
                }
                for r in self.rules
            ]
        }
        return json.dumps(data, indent=2)

if __name__ == "__main__":
    kb = KnowledgeBase()
    print(f"Loaded Knowledge Base with {len(kb.get_all_crops())} crops and {len(kb.get_rules())} rules.")
    mung = kb.get_crop_requirements("mungbean")
    print(f"Mung Bean Duration: {mung['growth_duration_days']}, Season: {mung['season']}")
