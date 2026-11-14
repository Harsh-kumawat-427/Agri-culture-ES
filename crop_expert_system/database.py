"""
DatabaseManager Module for Smart Crop & Fertilizer Advisor Expert System.
Uses SQLite to persistently record past consultations, soil parameters,
model predictions, rule inferences, and explanations.
"""

import sqlite3
import json
import os
import shutil
import tempfile
import secrets
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Manages SQLite persistence for expert system recommendation histories."""
    def __init__(self, db_path=None):
        if db_path is None:
            # Check for Vercel/AWS Lambda serverless environments where only /tmp is writable
            base_dir = os.path.dirname(os.path.abspath(__file__))
            seed_db = os.path.join(base_dir, "data", "expert_system_history.db")

            if os.environ.get('VERCEL') or not self._is_writable(os.path.join(base_dir, "data")):
                tmp_dir = tempfile.gettempdir()
                self.db_path = os.path.join(tmp_dir, "expert_system_history.db")
                if os.path.exists(seed_db) and not os.path.exists(self.db_path):
                    try:
                        shutil.copy2(seed_db, self.db_path)
                    except Exception:
                        pass
            else:
                candidates = [
                    seed_db,
                    os.path.join(os.getcwd(), "crop_expert_system", "data", "expert_system_history.db"),
                    os.path.join(os.getcwd(), "data", "expert_system_history.db")
                ]
                self.db_path = next((p for p in candidates if os.path.exists(p)), candidates[0])
        else:
            self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    @staticmethod
    def _is_writable(dir_path: str) -> bool:
        """Checks if a directory has active write permissions."""
        try:
            os.makedirs(dir_path, exist_ok=True)
            test_file = os.path.join(dir_path, ".write_check")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            return True
        except Exception:
            return False

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Creates recommendations history table and ensures report_id column exists."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recommendations_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id TEXT UNIQUE,
                    timestamp TEXT NOT NULL,
                    farmer_name TEXT DEFAULT 'Farmer',
                    location TEXT DEFAULT 'Farm Field #1',
                    soil_type TEXT DEFAULT 'Alluvial/Loamy',
                    N REAL NOT NULL,
                    P REAL NOT NULL,
                    K REAL NOT NULL,
                    ph REAL NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    rainfall REAL NOT NULL,
                    predicted_crop TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    recommended_fertilizer TEXT NOT NULL,
                    dosage_kg_ha REAL NOT NULL,
                    dosage_kg_acre REAL NOT NULL,
                    explanation TEXT NOT NULL,
                    fired_rules_json TEXT,
                    nutrient_gaps_json TEXT
                )
            """)
            conn.commit()

            # Check if report_id column exists in existing database
            cursor.execute("PRAGMA table_info(recommendations_history)")
            cols = [info[1] for info in cursor.fetchall()]
            if "report_id" not in cols:
                cursor.execute("ALTER TABLE recommendations_history ADD COLUMN report_id TEXT")
                conn.commit()

            # Populate missing report_ids for existing rows
            cursor.execute("SELECT id FROM recommendations_history WHERE report_id IS NULL OR report_id = ''")
            missing_rows = cursor.fetchall()
            for r in missing_rows:
                token = f"agr_{secrets.token_hex(4)}"
                cursor.execute("UPDATE recommendations_history SET report_id = ? WHERE id = ?", (token, r["id"]))
            conn.commit()

            try:
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_rec_report_id ON recommendations_history(report_id)")
                conn.commit()
            except Exception:
                pass

    def generate_report_token(self) -> str:
        """Generates random secure unguessable report token."""
        return f"agr_{secrets.token_hex(4)}"

    def cleanup_test_data(self):
        """Removes 'Test Farmer' test rows and deduplicates rows in the live database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recommendations_history WHERE farmer_name LIKE '%Test Farmer%' OR location LIKE '%Unit Test%'")
            cursor.execute("""
                DELETE FROM recommendations_history
                WHERE id NOT IN (
                    SELECT MIN(id)
                    FROM recommendations_history
                    GROUP BY farmer_name, location, predicted_crop, recommended_fertilizer, N, P, K
                )
            """)
            conn.commit()

    def save_history(
        self,
        farmer_name: str,
        location: str,
        soil_type: str,
        soil_dict: Dict[str, float],
        recommendation_report: Dict[str, Any],
        confidence: float
    ) -> int:
        """Saves a completed expert consultation into SQLite with random unguessable report_id."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_id = self.generate_report_token()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO recommendations_history (
                    report_id, timestamp, farmer_name, location, soil_type,
                    N, P, K, ph, temperature, humidity, rainfall,
                    predicted_crop, confidence, recommended_fertilizer,
                    dosage_kg_ha, dosage_kg_acre, explanation,
                    fired_rules_json, nutrient_gaps_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                report_id,
                ts,
                farmer_name or "Farmer",
                location or "Farm Field #1",
                soil_type or "Loamy",
                soil_dict.get("N", 0.0),
                soil_dict.get("P", 0.0),
                soil_dict.get("K", 0.0),
                soil_dict.get("ph", 6.5),
                soil_dict.get("temperature", 25.0),
                soil_dict.get("humidity", 70.0),
                soil_dict.get("rainfall", 100.0),
                recommendation_report.get("crop_display", recommendation_report.get("crop", "Unknown")),
                confidence,
                recommendation_report.get("recommended_fertilizer", "None"),
                recommendation_report.get("dosage", {}).get("kg_per_hectare", 0.0),
                recommendation_report.get("dosage", {}).get("kg_per_acre", 0.0),
                recommendation_report.get("explanation", ""),
                json.dumps(recommendation_report.get("fired_rules", [])),
                json.dumps(recommendation_report.get("nutrient_gaps", {}))
            ))
            conn.commit()
            return cursor.lastrowid

    def fetch_history(self, limit: int = 50, anonymize: bool = False) -> List[Dict[str, Any]]:
        """Retrieves most recent consultations in descending order, with optional anonymization."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM recommendations_history
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                r = dict(row)
                if not r.get("report_id"):
                    r["report_id"] = f"agr_{r['id']:04d}"
                if anonymize:
                    r["farmer_name"] = f"Farmer #{r['id']:03d}"
                    r["location"] = f"Field Plot #{r['id']:02d} [Protected]"
                results.append(r)
            return results

    def fetch_by_id(self, rec_id_or_token: Any) -> Optional[Dict[str, Any]]:
        """Fetches individual consultation record by random report_id or legacy integer ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Try matching random report_id token first
            cursor.execute("SELECT * FROM recommendations_history WHERE report_id = ?", (str(rec_id_or_token),))
            row = cursor.fetchone()
            if row:
                r = dict(row)
                if not r.get("report_id"):
                    r["report_id"] = str(rec_id_or_token)
                return r

            # Fall back to matching numeric integer ID
            if str(rec_id_or_token).isdigit():
                cursor.execute("SELECT * FROM recommendations_history WHERE id = ?", (int(rec_id_or_token),))
                row = cursor.fetchone()
                if row:
                    r = dict(row)
                    if not r.get("report_id"):
                        r["report_id"] = f"agr_{r['id']:04d}"
                    return r
            return None

    def delete_history(self, rec_id: int) -> bool:
        """Deletes a recommendation record."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recommendations_history WHERE id = ?", (rec_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_statistics(self) -> Dict[str, Any]:
        """Calculates dashboard summary metrics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM recommendations_history")
            total = cursor.fetchone()[0]

            cursor.execute("""
                SELECT predicted_crop, COUNT(*) as count
                FROM recommendations_history
                GROUP BY predicted_crop
                ORDER BY count DESC
                LIMIT 5
            """)
            top_crops = [{"crop": r[0], "count": r[1]} for r in cursor.fetchall()]

            cursor.execute("""
                SELECT recommended_fertilizer, COUNT(*) as count
                FROM recommendations_history
                GROUP BY recommended_fertilizer
                ORDER BY count DESC
                LIMIT 5
            """)
            top_fertilizers = [{"fertilizer": r[0], "count": r[1]} for r in cursor.fetchall()]

            return {
                "total_recommendations": total,
                "top_crops": top_crops,
                "top_fertilizers": top_fertilizers
            }

if __name__ == "__main__":
    db = DatabaseManager()
    print("DatabaseManager initialized. Total records:", db.get_statistics()["total_recommendations"])
