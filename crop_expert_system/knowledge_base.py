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
    rule_type: str = "deficiency"  # deficiency, soil_ph, balanced, toxicity, climate, micronutrient, rotation, organic
    rule_name: str = ""
    agronomic_source: str = "ICAR & State Agricultural Universities"
    safety_precaution: str = ""

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
                "suitable_seasons": ["Zaid", "Kharif", "Catch Crop"],
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
                "suitable_seasons": ["Zaid", "Summer"],
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
                "suitable_seasons": ["Zaid", "Summer"],
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
                "season": "Kharif (Monsoon) / Zaid (Summer)",
                "suitable_seasons": ["Kharif", "Zaid"],
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
                "season": "Rabi (Winter)",
                "suitable_seasons": ["Rabi", "Winter"],
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
        """Fertilizer composition details, nutrient percentages, oxide/elemental fractions, and typical application forms."""
        return {
            "Urea": {
                "name": "Urea",
                "formula": "CO(NH2)2",
                "primary_nutrient": "N",
                "n_percent": 46.0,
                "p_percent": 0.0,
                "k_percent": 0.0,
                "p2o5_percent": 0.0,
                "k2o_percent": 0.0,
                "elemental_p_percent": 0.0,
                "elemental_k_percent": 0.0,
                "description": "High-concentration nitrogenous granular fertilizer (46% N). Supplies 46 kg Nitrogen per 100 kg product.",
                "split_schedule": "Apply 50% basal at sowing, 25% at tillering, and 25% at panicle/flowering initiation."
            },
            "DAP": {
                "name": "DAP (Di-Ammonium Phosphate 18-46-0)",
                "formula": "(NH4)2HPO4",
                "primary_nutrient": "P",
                "n_percent": 18.0,
                "p_percent": 46.0,
                "k_percent": 0.0,
                "p2o5_percent": 46.0,
                "k2o_percent": 0.0,
                "elemental_p_percent": 20.07,  # P2O5 * 0.4364
                "elemental_k_percent": 0.0,
                "description": "Commercial grade 18-46-0: Supplies 46% P₂O₅ (equivalent to 20.1% elemental P) plus 18% starter Nitrogen.",
                "starter_n_credit": 0.18,
                "split_schedule": "Apply 100% as basal dressing placed 3-5 cm below and beside the seed zone at sowing."
            },
            "SSP": {
                "name": "SSP (Single Super Phosphate)",
                "formula": "Ca(H2PO4)2 + CaSO4",
                "primary_nutrient": "P",
                "n_percent": 0.0,
                "p_percent": 16.0,
                "k_percent": 0.0,
                "p2o5_percent": 16.0,
                "k2o_percent": 0.0,
                "elemental_p_percent": 6.98,  # 16 * 0.4364
                "elemental_k_percent": 0.0,
                "description": "Supplies 16% water-soluble P₂O₅ plus 11-12% Sulphur and 19-21% Calcium for root and nodule development.",
                "split_schedule": "Full basal application incorporated into the soil during final tillage."
            },
            "MOP": {
                "name": "MOP (Muriate of Potash 0-0-60)",
                "formula": "KCl",
                "primary_nutrient": "K",
                "n_percent": 0.0,
                "p_percent": 0.0,
                "k_percent": 60.0,
                "p2o5_percent": 0.0,
                "k2o_percent": 60.0,
                "elemental_p_percent": 0.0,
                "elemental_k_percent": 49.8,  # K2O * 0.8301
                "description": "Commercial grade 0-0-60: Supplies 60% K₂O (equivalent to 49.8% elemental K) for osmotic regulation and disease resistance.",
                "split_schedule": "Apply 50% basal and 50% at flowering/grain-fill stage in light soils, or 100% basal in heavy clay soils."
            },
            "NPK 19:19:19": {
                "name": "NPK 19:19:19 (Complex 1:1:1)",
                "formula": "Complex 1:1:1",
                "primary_nutrient": "NPK",
                "n_percent": 19.0,
                "p_percent": 19.0,
                "k_percent": 19.0,
                "p2o5_percent": 19.0,
                "k2o_percent": 19.0,
                "elemental_p_percent": 8.29,
                "elemental_k_percent": 15.77,
                "description": "Balanced multi-nutrient complex delivering 19% N, 19% P₂O₅, and 19% K₂O for multi-nutrient deficient soils.",
                "split_schedule": "Apply as basal starter fertilizer, followed by crop-specific topdressings."
            },
            "Agricultural Lime": {
                "name": "Agricultural Lime (Calcium Carbonate)",
                "formula": "CaCO3",
                "primary_nutrient": "pH Buffer",
                "n_percent": 0.0,
                "p_percent": 0.0,
                "k_percent": 0.0,
                "p2o5_percent": 0.0,
                "k2o_percent": 0.0,
                "elemental_p_percent": 0.0,
                "elemental_k_percent": 0.0,
                "description": "Ground limestone (CaCO₃) used exclusively for acid soils (pH < 5.5). Neutralizes toxic Al³⁺ and Fe²⁺ ions.",
                "split_schedule": "Broadcast and incorporate 2-3 weeks prior to sowing with adequate moisture."
            },
            "Agricultural Gypsum": {
                "name": "Agricultural Gypsum (Calcium Sulfate Dihydrate)",
                "formula": "CaSO4·2H2O",
                "primary_nutrient": "pH Buffer / Sulphur",
                "n_percent": 0.0,
                "p_percent": 0.0,
                "k_percent": 0.0,
                "p2o5_percent": 0.0,
                "k2o_percent": 0.0,
                "elemental_p_percent": 0.0,
                "elemental_k_percent": 0.0,
                "description": "Agricultural gypsum (23% Ca, 18% S). Specifically amends sodic / alkali soils (pH > 8.0, high ESP) by displacing exchangeable Na⁺ with Ca²⁺.",
                "split_schedule": "Broadcast in dry soil, disc-plough to 10 cm, followed by heavy ponding/leaching with good quality irrigation water."
            }
        }

    def _init_rules(self) -> List[Rule]:
        """Loads canonical production rules as designated in project specification with agronomic citations."""
        return [
            Rule(
                rule_id="R01_ALL_DEFICIENT",
                rule_name="Compound NPK Basal Correction",
                condition_desc="Nitrogen, Phosphorus, and Potassium are all significantly below crop benchmarks",
                target_nutrient="NPK",
                suggested_fertilizer="NPK 19:19:19",
                advice="Soil shows concurrent multi-nutrient deficiency. Apply balanced NPK 19:19:19 as basal dressing placed 4-5 cm below seed depth.",
                priority=100,
                rule_type="balanced",
                agronomic_source="ICAR Integrated Plant Nutrient Supply System (IPNS)",
                safety_precaution="Incorporate thoroughly into topsoil; do not broadcast on dry soil without irrigation."
            ),
            Rule(
                rule_id="R02_N_LOW",
                rule_name="Split Nitrogen Vegetative Topdressing",
                condition_desc="Soil Nitrogen (N) is below the recommended minimum threshold for the crop",
                target_nutrient="N",
                suggested_fertilizer="Urea",
                advice="Nitrogen deficiency detected. Apply prilled Urea (46% N) in 2-3 split applications: 50% basal at sowing, 25% at active tillering (3-4 weeks), and 25% at panicle/flowering initiation.",
                priority=80,
                rule_type="deficiency",
                agronomic_source="IISS (Indian Institute of Soil Science) Bhopal",
                safety_precaution="Never apply entire nitrogen dose at once; avoid urea broadcasting in waterlogged fields to minimize volatilization and leaching."
            ),
            Rule(
                rule_id="R03_P_LOW",
                rule_name="Starter Phosphate Root Establishment (P₂O₅ & Starter N)",
                condition_desc="Soil Phosphorus (P) is below the crop's minimum root establishment requirement",
                target_nutrient="P",
                suggested_fertilizer="DAP",
                advice="Phosphorus deficiency detected. Apply DAP (18-46-0: 46% P₂O₅ equivalent, 20.1% elemental P) banded 3-5 cm below seed zone. DAP also contributes 18 kg starter N per 100 kg product applied.",
                priority=75,
                rule_type="deficiency",
                agronomic_source="TNAU Agritech Nutrient Portal / ICAR Guidelines",
                safety_precaution="Apply at sowing near roots; phosphorus has low mobility in soil and does not move downward with irrigation."
            ),
            Rule(
                rule_id="R04_K_LOW",
                rule_name="Potash Osmotic & Stalk Reinforcement (K₂O Equivalent)",
                condition_desc="Soil Potassium (K) is below the crop's physiological resilience threshold",
                target_nutrient="K",
                suggested_fertilizer="MOP",
                advice="Potassium deficit found. Apply MOP (Muriate of Potash 0-0-60: 60% K₂O equivalent, 49.8% elemental K) to reinforce stalk strength, regulate stomatal closure, and enhance osmotic drought tolerance.",
                priority=70,
                rule_type="deficiency",
                agronomic_source="International Potash Institute (IPI) & ICAR Agronomy",
                safety_precaution="In light sandy soils, split into 50% basal and 50% flowering to prevent leaching losses."
            ),
            Rule(
                rule_id="R05_PH_ACIDIC",
                rule_name="Acid Soil Neutralization & Liming",
                condition_desc="Soil pH is below 5.5 (strongly acidic with toxic Al³⁺ / Fe²⁺ activity)",
                target_nutrient="pH",
                suggested_fertilizer="Agricultural Lime",
                advice="Acidic soil condition (pH < 5.5) locks phosphorus into insoluble iron/aluminum phosphates. Broadcast Agricultural Lime (CaCO₃) at 200-500 kg/ha and incorporate into soil 2-3 weeks prior to sowing.",
                priority=90,
                rule_type="soil_ph",
                agronomic_source="ICAR Research Complex for NEH Region / Acid Soil Bulletin",
                safety_precaution="Lime should be finely powdered and worked into top 15 cm soil with adequate soil moisture."
            ),
            Rule(
                rule_id="R06_PH_ALKALINE",
                rule_name="Sodic / Alkaline Soil Gypsum Reclamation",
                condition_desc="Soil pH is above 8.0 with sodic condition (High Exchangeable Sodium Percentage / ESP)",
                target_nutrient="pH",
                suggested_fertilizer="Agricultural Gypsum",
                advice="Alkali/sodic condition (pH > 8.0, high ESP) disperses soil aggregates and limits root respiration. Incorporate Agricultural Gypsum (CaSO₄·2H₂O: 18% S, 23% Ca) to displace exchangeable Na⁺ with Ca²⁺, followed by deep flushing/leaching with good water.",
                priority=90,
                rule_type="soil_ph",
                agronomic_source="CSSRI (Central Soil Salinity Research Institute) Karnal",
                safety_precaution="Ensure adequate subsurface drainage before ponding water; do not confuse saline soil (high EC) with sodic soil (high ESP/pH)."
            ),
            Rule(
                rule_id="R07_BALANCED_SOIL",
                rule_name="Balanced Maintenance & Soil Health Sustenance",
                condition_desc="All nutrients (N, P, K) and pH meet or exceed crop requirements",
                target_nutrient="None",
                suggested_fertilizer="No Chemical Fertilizer Required",
                advice="Soil nutrient profile is optimal for this crop. Avoid unnecessary chemical applications. Maintain soil organic matter with well-rotted farmyard manure (FYM 5 t/ha) or bio-compost.",
                priority=50,
                rule_type="balanced",
                agronomic_source="National Project on Management of Soil Health & Fertility",
                safety_precaution="Continue regular annual soil health testing to detect nutrient drawdowns early."
            ),
            Rule(
                rule_id="R08_NP_DEFICIENT",
                rule_name="Dual Nitrogen & Phosphorus Starter Balancing",
                condition_desc="Nitrogen and Phosphorus are both deficient while Potassium is adequate",
                target_nutrient="NP",
                suggested_fertilizer="DAP (18-46-0) + Topdress Urea",
                advice="Dual N & P deficiency detected. Apply DAP at basal sowing (supplies both P₂O₅ and starter N), followed by a scheduled Urea topdressing at 30 days after germination.",
                priority=85,
                rule_type="deficiency",
                agronomic_source="ICAR Cereal Agronomy Protocols",
                safety_precaution="Account for DAP's 18% N content when calculating topdress Urea dose to prevent excessive vegetative growth."
            ),
            Rule(
                rule_id="R09_NK_DEFICIENT",
                rule_name="Dual Nitrogen & Potassium Vegetative Reinforcement",
                condition_desc="Nitrogen and Potassium are both deficient while Phosphorus is adequate",
                target_nutrient="NK",
                suggested_fertilizer="Potassium Nitrate (13-0-45) or Urea + MOP blend",
                advice="Dual N & K deficiency detected. Apply split Urea for vegetative chlorophyll synthesis and MOP (60% K₂O) to ensure strong vascular stalk development and drought resistance.",
                priority=85,
                rule_type="deficiency",
                agronomic_source="Fertiliser Association of India (FAI) Technical Bulletin",
                safety_precaution="Do not mix urea and MOP too far in advance in humid weather as the blend is hygroscopic."
            ),
            Rule(
                rule_id="R10_PK_DEFICIENT",
                rule_name="Legume Root Nodulation & Pod Filling (P & K)",
                condition_desc="Phosphorus and Potassium are both deficient while Nitrogen is adequate (common in legumes)",
                target_nutrient="PK",
                suggested_fertilizer="Monopotassium Phosphate (MKP 00:52:34) / SSP + MOP",
                advice="Dual P & K deficit found. Apply Single Super Phosphate (SSP) with MOP prior to flowering to spur root nodulation and flower retention. SSP also provides 11% crucial Sulphur.",
                priority=85,
                rule_type="deficiency",
                agronomic_source="Indian Society of Soil Science & Pulses Research (IIPR) Kanpur",
                safety_precaution="In pulses, ensure adequate soil moisture at flowering when phosphorus demand peaks."
            ),
            Rule(
                rule_id="R11_N_EXCESS",
                rule_name="Nitrogen Luxury Consumption & Toxicity Mitigation",
                condition_desc="Soil Nitrogen exceeds maximum safe benchmark by > 25% (Nitrogen luxury consumption)",
                target_nutrient="N_Toxicity",
                suggested_fertilizer="Withhold Nitrogen Fertilizers / Leach with Water",
                advice="Excessive soil nitrogen leads to succulent weak stems, severe lodging, delayed maturity, and heavy pest/aphid infestation. Withhold all nitrogenous fertilizers immediately and irrigate to dilute nitrate concentration.",
                priority=78,
                rule_type="toxicity",
                agronomic_source="Directorate of Plant Protection, Quarantine & Storage (DPPQS)",
                safety_precaution="Monitor closely for blast in rice or rust in wheat, which proliferate rapidly under excess nitrogen."
            ),
            Rule(
                rule_id="R12_P_EXCESS",
                rule_name="Phosphate-Induced Zinc Lockout & Antagonism Management",
                condition_desc="Soil Phosphorus is excessively high (> 30% above maximum benchmark), inducing Zinc uptake lockout",
                target_nutrient="P_Toxicity",
                suggested_fertilizer="Chelated Zinc (Zn-EDTA) Foliar Spray",
                advice="High available phosphorus inhibits ionic zinc absorption by roots through phosphate-zinc antagonism, causing interveinal leaf chlorosis. Withhold all phosphatic fertilizers and apply Chelated Zinc (Zn-EDTA @ 0.5–1.0 g/L water) as a foliar rescue spray.",
                priority=74,
                rule_type="toxicity",
                agronomic_source="IISS Bhopal Micronutrient Antagonism Advisory",
                safety_precaution="Do not soil-apply inorganic zinc with phosphate fertilizers together as insoluble zinc phosphate forms."
            ),
            Rule(
                rule_id="R13_DROUGHT_HEAT_STRESS",
                rule_name="Thermal & Moisture Stress Osmoregulation (Foliar KNO₃)",
                condition_desc="Precipitation < 60 mm and Ambient Temperature > 30°C (Moisture Deficit & Thermal Stress)",
                target_nutrient="Climate_Stress",
                suggested_fertilizer="Foliar Potassium (1% KNO3) & Organic Straw Mulch",
                advice="High temperature and moisture deficit trigger stomatal conductance loss and leaf scorching. Spray 1.0% to 1.5% Potassium Nitrate (KNO₃: 10-15 g/L water) in early morning or late afternoon to regulate stomatal transpiration, and spread crop residue mulch (4-5 t/ha).",
                priority=92,
                rule_type="climate",
                agronomic_source="CRIDA (Central Research Institute for Dryland Agriculture) Hyderabad",
                safety_precaution="Never spray foliar salts during hot midday sun (> 35°C) to prevent osmotic leaf burn."
            ),
            Rule(
                rule_id="R14_WATERLOGGING_EXCESS_RAIN",
                rule_name="Waterlogging Aeration & Post-Drainage Nitrate Recovery",
                condition_desc="Precipitation > 220 mm with heavy soil (Waterlogging & Leaching Risk)",
                target_nutrient="Drainage_Nitrogen",
                suggested_fertilizer="Ridge & Furrow Drainage + Post-Drainage Urea",
                advice="Excessive rainfall causes root zone waterlogging, oxygen starvation (hypoxia), and nitrogen leaching/denitrification. Create field drainage trenches immediately. Do not fertilize standing water; apply a light split of Urea (20-25 kg/ha) or 2% foliar urea only after excess water recedes.",
                priority=91,
                rule_type="climate",
                agronomic_source="Directorate of Water Management / ICAR Rainfed Agriculture",
                safety_precaution="Prioritize surface drainage before any fertilizer application; roots cannot absorb nutrients without soil oxygen."
            ),
            Rule(
                rule_id="R15_COLD_CHILLING_STRESS",
                rule_name="Frost Protection & Latent Heat Management",
                condition_desc="Ambient Temperature < 15°C during critical growth stages (Frost & Chilling Risk)",
                target_nutrient="Thermal_Stress",
                suggested_fertilizer="Potassium Silicate Foliar Spray & Light Evening Irrigation",
                advice="Low ambient temperature (< 15°C) slows root cation uptake and threatens frost injury in sensitive crops (Mustard, Potato, Gram). Provide light evening irrigation to raise soil thermal mass and release latent heat during freezing hours, and spray 0.15% potassium silicate.",
                priority=88,
                rule_type="climate",
                agronomic_source="IMD Agro-Meteorological Advisory Service & ICAR",
                safety_precaution="Irrigation must be light; avoid water stagnation in fields during cold spells."
            ),
            Rule(
                rule_id="R16_SULPHUR_DEFICIT_OILSEEDS",
                rule_name="Oilseed & Pulse Sulphur Nutrition (Glucosinolates & Protein)",
                condition_desc="Oilseed or pulse crop planted with low fertility (Sulphur requirement for oil/protein)",
                target_nutrient="Sulphur",
                suggested_fertilizer="Agricultural Gypsum or Bentonite Sulphur (25 kg/ha)",
                advice="Oilseed crops (Mustard, Groundnut, Soybean) and pulses require high sulphur for oil synthesis and protein amino acids. Apply 20-30 kg S/ha via Bentonite Sulphur (90% S @ 25 kg/ha) or Agricultural Gypsum (18% S @ 150 kg/ha) as basal dressing.",
                priority=76,
                rule_type="micronutrient",
                agronomic_source="DRMR (Directorate of Rapeseed-Mustard Research) Bharatpur",
                safety_precaution="Bentonite sulphur requires 1-2 weeks in moist soil to convert to plant-available sulfate (SO₄²⁻)."
            ),
            Rule(
                rule_id="R17_ZINC_DEFICIENCY_CALCAREOUS",
                rule_name="Calcareous Soil Zinc Fixation Correction (Khaira / White Bud)",
                condition_desc="Alkaline / Calcareous soil (pH > 7.8) with high phosphorus (Zinc fixation)",
                target_nutrient="Zinc",
                suggested_fertilizer="Zinc Sulphate Heptahydrate (ZnSO4 21%)",
                advice="High pH and calcium carbonate fix ionic zinc into insoluble precipitates, causing Khaira disease in paddy or white bud in maize. Broadcast 25 kg/ha Zinc Sulphate (21% Zn) as basal soil dressing, or spray 0.5% ZnSO₄ neutralized with 0.25% lime at 25 and 40 days.",
                priority=82,
                rule_type="micronutrient",
                agronomic_source="ICAR All India Coordinated Research Project on Micronutrients",
                safety_precaution="Always neutralize foliar zinc sulphate with slaked lime to prevent leaf scorching."
            ),
            Rule(
                rule_id="R18_PULSE_ROTATION_SYNERGY",
                rule_name="Symbiotic Rhizobium Inoculation & Nitrogen Recovery",
                condition_desc="Rotation following high-nitrogen cereal crop (Rice, Wheat, Maize)",
                target_nutrient="Soil_Regeneration",
                suggested_fertilizer="Rhizobium Bio-fertilizer Seed Inoculation",
                advice="Monoculture cereal farming rapidly depletes soil nitrogen and compacts structure. Treat legume seeds with Rhizobium biofertilizer culture (200 g/10 kg seed) to stimulate root nodules capable of fixing 35-50 kg/ha atmospheric nitrogen for following crops.",
                priority=86,
                rule_type="rotation",
                agronomic_source="Indian Institute of Pulses Research (IIPR) Kanpur",
                safety_precaution="Keep inoculated seeds in shade; do not mix biofertilizers directly with chemical fungicides or insecticides without a 24h gap."
            ),
            Rule(
                rule_id="R19_SHORT_GAP_CATCH_CROP",
                rule_name="Short Fallow Window Catch Crop Starter Formulation",
                condition_desc="Fallow harvest gap between two main crops is short (60 - 85 days)",
                target_nutrient="Harvest_Window",
                suggested_fertilizer="Starter DAP (18-46-0) for Fast Catch Crop",
                advice="Short fallow gap (60-85 days) mandates extra-early catch crops (Mungbean, Cowpea, Mothbeans). Apply starter DAP (50-60 kg/ha) at sowing to rapidly develop root architecture and trigger synchronized early flowering within 30 days.",
                priority=89,
                rule_type="rotation",
                agronomic_source="ICAR Catch-Crop Cropping Systems Research",
                safety_precaution="Select determinate, early-maturing cultivars (e.g. IPM 02-3 or PDM 139) to guarantee harvest before next season sowing."
            ),
            Rule(
                rule_id="R20_ORGANIC_CARBON_RESTORATION",
                rule_name="Soil Organic Carbon (SOC) Rebuilding & Biological Health",
                condition_desc="Soil Nitrogen is critically depleted (< 35 kg/ha) indicating low soil organic matter",
                target_nutrient="Soil_Carbon",
                suggested_fertilizer="Well-Decomposed Farmyard Manure (FYM 8-10 t/ha)",
                advice="Critically low soil nitrogen (< 35 kg/ha) indicates degraded soil organic carbon (< 0.4%). Incorporate 8-10 tonnes/ha well-decomposed Farmyard Manure (FYM) or vermicompost during final ploughing to rebuild microbial biomass and cation exchange capacity.",
                priority=84,
                rule_type="organic",
                agronomic_source="National Centre for Organic and Natural Farming (NCONF)",
                safety_precaution="Ensure FYM is fully decomposed to prevent weed seed germination and termite infestation."
            ),
            Rule(
                rule_id="R21_MICRONUTRIENT_BORON_DEFICIT",
                rule_name="Horticultural Boron Nutrition (Pollen Viability & Fruit Set)",
                condition_desc="Fruit and horticultural crops in light/leached soils (Boron deficit risk)",
                target_nutrient="Boron",
                suggested_fertilizer="Borax (10 kg/ha) or Solubor Foliar Spray (0.1%)",
                advice="Fruit crops (Apple, Pomegranate, Grapes, Papaya) require boron for cell wall pectin, pollen tube germination, and preventing fruit cracking. Apply 10 kg/ha Borax to soil, or spray 0.1% Solubor (1 g/L water) at pre-bloom and fruit set.",
                priority=72,
                rule_type="micronutrient",
                agronomic_source="ICAR-Central Institute for Arid Horticulture (CIAH) Bikaner",
                safety_precaution="The range between boron deficiency and toxicity is narrow; adhere strictly to recommended concentrations."
            ),
            Rule(
                rule_id="R22_SALINE_SOIL_REMEDY",
                rule_name="Saline Soil Leaching & Sesbania Green Manure Reclamation",
                condition_desc="Saline soil condition (High Electrical Conductivity EC > 4 dS/m, pH < 8.2, soluble salts)",
                target_nutrient="Salinity",
                suggested_fertilizer="Green Manuring with Dhaincha (Sesbania) + Leaching",
                advice="High soluble salt concentration (saline soil: EC > 4 dS/m, pH < 8.2) causes osmotic physiological drought. Provide subsurface drainage trenches and leach soluble salts with clean irrigation water. Sow Dhaincha (Sesbania aculeata @ 25 kg/ha) and incorporate into soil at 45 days to release organic acids and restore permeability. (If soil also has high exchangeable sodium pH > 8.5, gypsum is required).",
                priority=79,
                rule_type="soil_ph",
                agronomic_source="CSSRI Salinity Management Protocols & TNAU Soil Science",
                safety_precaution="Do not add gypsum to purely saline non-sodic soils as it increases unnecessary salt burden."
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
                    "rule_name": r.rule_name,
                    "condition": r.condition_desc,
                    "target_nutrient": r.target_nutrient,
                    "fertilizer": r.suggested_fertilizer,
                    "advice": r.advice,
                    "priority": r.priority,
                    "type": r.rule_type,
                    "source": r.agronomic_source,
                    "safety": r.safety_precaution
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
