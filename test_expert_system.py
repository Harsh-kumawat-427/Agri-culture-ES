"""
Automated Comprehensive Test Suite for AgriTech AI Expert System.
Verifies ML Predictor, KnowledgeBase, InferenceEngine, DatabaseManager, and Flask API endpoints.
"""

import unittest
import json
import os
import sys

from crop_expert_system.knowledge_base import KnowledgeBase
from crop_expert_system.predictor import CropPredictor, SoilInput
from crop_expert_system.inference_engine import InferenceEngine, Recommendation
from crop_expert_system.database import DatabaseManager
from app import app


class TestAgriTechExpertSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase()
        cls.predictor = CropPredictor()
        cls.engine = InferenceEngine(cls.kb)
        cls.db = DatabaseManager()
        cls.client = app.test_client()

    def test_01_knowledge_base_integrity(self):
        """Checks that all 22 crops, fertilizers, and rules exist in the KnowledgeBase."""
        crops = self.kb.get_all_crops()
        self.assertEqual(len(crops), 22, f"Expected 22 crops, found {len(crops)}")
        self.assertIn("rice", crops)
        self.assertIn("maize", crops)
        self.assertIn("grapes", crops)
        self.assertIn("cotton", crops)

        rules = self.kb.get_rules()
        self.assertGreaterEqual(len(rules), 6, "Knowledge base rules should have at least 6 production rules.")
        rule_ids = [r.rule_id for r in rules]
        self.assertIn("R01_ALL_DEFICIENT", rule_ids)
        self.assertIn("R02_N_LOW", rule_ids)
        self.assertIn("R03_P_LOW", rule_ids)
        self.assertIn("R04_K_LOW", rule_ids)
        self.assertIn("R05_PH_ACIDIC", rule_ids)

        urea = self.kb.get_fertilizer("Urea")
        self.assertIsNotNone(urea)
        self.assertEqual(urea["n_percent"], 46.0)

    def test_02_crop_predictor(self):
        """Tests ML classification and confidence scoring."""
        # High rainfall + high humidity -> Rice profile
        soil_rice = SoilInput(N=80, P=45, K=40, ph=6.5, rainfall=230, temperature=24, humidity=82)
        pred_rice = self.predictor.predict_crop(soil_rice)
        self.assertEqual(pred_rice, "rice", f"Expected rice, got {pred_rice}")

        top_3 = self.predictor.top_n_crops(soil_rice, n=3)
        self.assertEqual(len(top_3), 3)
        self.assertEqual(top_3[0]["crop"], "rice")
        self.assertGreater(top_3[0]["confidence"], 70.0)

    def test_03_inference_engine_fertilizer_rules(self):
        """Tests forward-chaining rules and dosage calculation."""
        # Nitrogen deficient soil for rice (N=40 vs ideal 80 -> gap=40)
        soil_low_n = SoilInput(N=40, P=45, K=40, ph=6.5, rainfall=230, temperature=24, humidity=82)
        top_crops = self.predictor.top_n_crops(soil_low_n, n=3)
        rec = self.engine.fire_rules(soil_low_n, "rice", top_crops)

        self.assertEqual(rec.crop, "rice")
        self.assertEqual(rec.fertilizer, "Urea")
        # 40 gap / 0.46 = ~86.96 kg/ha
        self.assertAlmostEqual(rec.dosage_kg_ha, 86.96, delta=1.0)
        self.assertIn("Urea", rec.explanation)
        self.assertIn("Nitrogen", rec.explanation)

    def test_04_acidic_soil_rule(self):
        """Tests pH acidic rule firing Lime."""
        soil_acidic = SoilInput(N=80, P=45, K=40, ph=4.8, rainfall=200, temperature=24, humidity=80)
        top_crops = self.predictor.top_n_crops(soil_acidic, n=3)
        rec = self.engine.fire_rules(soil_acidic, "rice", top_crops)

        rule_ids = [r["rule_id"] for r in rec.fired_rules]
        self.assertIn("R05_PH_ACIDIC", rule_ids)
        self.assertIn("Lime", rec.fertilizer)

    def test_05_database_manager(self):
        """Tests SQLite saving, fetching, and stats."""
        soil_dict = {"N": 80, "P": 45, "K": 40, "ph": 6.5, "rainfall": 220, "temperature": 24, "humidity": 82}
        report_dict = {
            "crop": "rice",
            "crop_display": "Rice (Paddy)",
            "recommended_fertilizer": "Urea",
            "dosage": {"kg_per_hectare": 50.0, "kg_per_acre": 20.2},
            "explanation": "Test explanation facility narrative.",
            "fired_rules": [{"rule_id": "R02_N_LOW"}],
            "nutrient_gaps": {"N": 20.0}
        }

        rec_id = self.db.save_history(
            farmer_name="Test Farmer",
            location="Unit Test Field",
            soil_type="Loamy",
            soil_dict=soil_dict,
            recommendation_report=report_dict,
            confidence=99.2
        )
        self.assertIsInstance(rec_id, int)
        self.assertGreater(rec_id, 0)

        record = self.db.fetch_by_id(rec_id)
        self.assertIsNotNone(record)
        self.assertEqual(record["farmer_name"], "Test Farmer")
        self.assertEqual(record["predicted_crop"], "Rice (Paddy)")

        stats = self.db.get_statistics()
        self.assertGreaterEqual(stats["total_recommendations"], 1)

    def test_06_crop_rotation_recommendation(self):
        """Tests crop recommendation by soil condition, time/season, temp, and harvest gap."""
        # Test 75-day summer window after Rice -> Should strongly favor short-duration catch legume (Mung bean)
        result = self.engine.recommend_crop_rotation(
            soil_condition="Loamy",
            time_of_year="Zaid (Summer: March - June)",
            temperature=30.0,
            harvest_gap_days=75,
            previous_crop="Rice (Paddy)",
            ph=6.5
        )
        self.assertIsNotNone(result)
        top = result["primary_recommendation"]
        self.assertIn("Mung", top["display_name"])
        self.assertGreaterEqual(top["suitability_score"], 90.0)
        self.assertIn("Time Between Two Harvests", result["explanation"])

    def test_07_flask_routes(self):
        """Tests Flask web pages and API responses."""
        res_home = self.client.get('/')
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b"AgriCulture", res_home.data)

        # /rotation page
        res_rot = self.client.get('/rotation')
        self.assertEqual(res_rot.status_code, 200)
        self.assertIn(b"Crop Recommendation by Soil", res_rot.data)

        # /about redirects to /rotation
        res_about = self.client.get('/about')
        self.assertEqual(res_about.status_code, 302)

        res_knowledge = self.client.get('/knowledge')
        self.assertEqual(res_knowledge.status_code, 200)
        self.assertIn(b"Knowledge Base", res_knowledge.data)

        res_history = self.client.get('/history')
        self.assertEqual(res_history.status_code, 200)
        self.assertIn(b"Consultation Records", res_history.data)

        # Test POST /api/recommend-rotation
        rot_payload = {
            "soil_condition": "Loamy",
            "time_of_year": "Zaid (Summer: March - June)",
            "temperature": 28.0,
            "harvest_gap_days": 75,
            "previous_crop": "Rice (Paddy)",
            "ph": 6.5
        }
        res_rot_api = self.client.post('/api/recommend-rotation', data=json.dumps(rot_payload), content_type='application/json')
        self.assertEqual(res_rot_api.status_code, 200)
        rot_data = res_rot_api.get_json()
        self.assertIn("primary_recommendation", rot_data)
        self.assertIn("explanation", rot_data)

        # Test POST /api/predict
        payload = {
            "farmer_name": "Suresh Patel",
            "location": "Gujarat Plot #2",
            "soil_type": "Black",
            "N": 115,
            "P": 45,
            "K": 20,
            "ph": 6.8,
            "temperature": 24,
            "humidity": 80,
            "rainfall": 80
        }
        res_pred = self.client.post('/api/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res_pred.status_code, 200)
        data = res_pred.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("recommendation", data)
        self.assertIn("crop", data["recommendation"])

        # Test report view for created consultation
        rec_id = data["consultation_id"]
        res_report = self.client.get(f'/report/{rec_id}')
        self.assertEqual(res_report.status_code, 200)
        self.assertIn(b"Advisory Report", res_report.data)

        # Test CSV export
        res_csv = self.client.get('/api/history?format=csv')
        self.assertEqual(res_csv.status_code, 200)
        self.assertEqual(res_csv.mimetype, 'text/csv')


if __name__ == "__main__":
    unittest.main()

