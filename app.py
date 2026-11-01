"""
Smart Crop and Fertilizer Advisor - AI Expert System
Flask Web Server integrating Machine Learning Crop Prediction with Rule-Based Fertilizer Advising.
Styled with AgriCulture Theme System (Bootstrap 5).
"""

import os
import sys
import io
import csv
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, Response, redirect, url_for

try:
    from flask_cors import CORS
except ImportError:
    def CORS(a):
        return a

# Ensure current directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from crop_expert_system.knowledge_base import KnowledgeBase
from crop_expert_system.predictor import CropPredictor, SoilInput
from crop_expert_system.inference_engine import InferenceEngine
from crop_expert_system.database import DatabaseManager
from crop_expert_system.train_model import ModelTrainer

# Initialize Flask Application with absolute template and static paths for Vercel/serverless support
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),
    template_folder=os.path.join(BASE_DIR, 'templates')
)
CORS(app)

# Initialize Core Expert System Engines
kb = KnowledgeBase()
predictor = CropPredictor()
engine = InferenceEngine(kb)
db = DatabaseManager()

# --- WEB PAGE ROUTES ---

@app.route('/')
def home():
    """Serves main AgriCulture themed dashboard and interactive advisor form."""
    stats = db.get_statistics()
    all_crops = kb.get_all_crops()
    return render_template('index.html', stats=stats, all_crops=all_crops)

@app.route('/rotation')
def rotation():
    """Serves Crop Recommendation on the basis of Soil Condition, Time/Season, Temperature, and Harvest Gap."""
    return render_template('rotation.html')

@app.route('/about')
def about():
    """Redirects to /rotation as System Architecture was replaced with Crop Rotation & Scheduling."""
    return redirect(url_for('rotation'))

@app.route('/knowledge')
def knowledge():
    """Serves knowledge base browser (22 crops, production rules, fertilizer chemistry)."""
    return render_template(
        'knowledge.html',
        crops=kb.crop_requirements,
        rules=kb.rules,
        fertilizers=kb.fertilizers
    )

@app.route('/history')
def history():
    """Serves historical consultation records and audit log stored in SQLite."""
    records = db.fetch_history(limit=100)
    stats = db.get_statistics()
    return render_template('history.html', history=records, stats=stats)

@app.route('/report/<int:rec_id>')
def report(rec_id):
    """Serves printable official farm advisory report for a specific consultation."""
    record = db.fetch_by_id(rec_id)
    if not record:
        return "<h3>Consultation record not found</h3><a href='/history'>Return to History</a>", 404
    crop_info = kb.get_crop_requirements(record.get('predicted_crop', ''))
    return render_template('report.html', record=record, crop_info=crop_info)

# --- STATIC ASSET COMPATIBILITY ROUTE ---

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Direct route alias for /assets/ to support AgriCulture template paths."""
    static_assets = os.path.join(app.root_path, 'static', 'assets')
    if os.path.exists(os.path.join(static_assets, filename)):
        return send_from_directory(static_assets, filename)
    fallback_assets = os.path.join(app.root_path, 'assets')
    return send_from_directory(fallback_assets, filename)

# --- REST API ENDPOINTS ---

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Main Expert System Inference Endpoint:
    1. Validates soil & climate inputs.
    2. Runs Machine Learning model to predict highest-yielding crop and confidence.
    3. Runs forward-chaining Inference Engine against Knowledge Base rules.
    4. Computes exact fertilizer dosage in kg/ha and kg/acre.
    5. Formulates natural language explanation facility reasoning.
    6. Persists consultation to SQLite database history.
    """
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        if not data:
            return jsonify({"error": "No input payload provided."}), 400

        # Construct and validate SoilInput
        soil = SoilInput(
            N=float(data.get('N', 0)),
            P=float(data.get('P', 0)),
            K=float(data.get('K', 0)),
            ph=float(data.get('ph', 6.5)),
            rainfall=float(data.get('rainfall', 100)),
            temperature=float(data.get('temperature', 25)),
            humidity=float(data.get('humidity', 70))
        )

        valid, err = soil.validate()
        if not valid:
            return jsonify({"error": err}), 400

        # 1. ML Crop Prediction
        best_crop = predictor.predict_crop(soil)
        top_crops = predictor.top_n_crops(soil, n=3)
        conf = predictor.confidence(soil)

        # 2. Rule-Based Fertilizer Inference & Explanation Facility
        rec = engine.fire_rules(soil, best_crop, top_crops)
        rec_report = rec.to_report()

        # Enrich with temporal / harvest gap context
        harvest_gap_days = int(data.get('harvest_gap_days', 90))
        season_time = data.get('season_time', 'Kharif')
        prev_crop = data.get('prev_crop', 'Rice (Paddy)')
        crop_reqs = kb.get_crop_requirements(best_crop)
        if crop_reqs:
            min_days = crop_reqs.get('duration_min_days', 90)
            max_days = crop_reqs.get('duration_max_days', 120)
            fits_gap = max_days <= harvest_gap_days
            buffer_days = harvest_gap_days - max_days
            rec_report['temporal_context'] = {
                'season_time': season_time,
                'prev_crop': prev_crop,
                'harvest_gap_days': harvest_gap_days,
                'crop_duration': crop_reqs.get('growth_duration_days', f"{min_days}-{max_days} days"),
                'fits_harvest_gap': fits_gap,
                'buffer_days': buffer_days,
                'suitable_seasons': crop_reqs.get('suitable_seasons', []),
                'rotation_role': crop_reqs.get('rotation_role', 'Standard Crop'),
                'rotation_benefits': crop_reqs.get('rotation_benefits', '')
            }

        # 3. Save into SQLite database history
        farmer_name = data.get('farmer_name', 'Farmer')
        location = data.get('location', 'Farm Plot #1')
        soil_type = data.get('soil_type', 'Loamy')

        rec_id = db.save_history(
            farmer_name=farmer_name,
            location=location,
            soil_type=soil_type,
            soil_dict=soil.to_dict(),
            recommendation_report=rec_report,
            confidence=conf
        )

        return jsonify({
            "status": "success",
            "consultation_id": rec_id,
            "soil": soil.to_dict(),
            "confidence": conf,
            "recommendation": rec_report
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommend-rotation', methods=['POST'])
def api_recommend_rotation():
    """
    Recommends optimal crop based on:
    - Soil Condition (Type, texture, pH)
    - Time of year / Sowing Season
    - Ambient Temperature
    - Time between two crop harvesting (harvest gap days)
    - Crop rotation synergy (preceding crop)
    """
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        soil_condition = data.get('soil_condition', 'Loamy')
        time_of_year = data.get('time_of_year', 'Zaid (Summer: March - June)')
        temperature = float(data.get('temperature', 28.0))
        harvest_gap_days = int(data.get('harvest_gap_days', 75))
        previous_crop = data.get('previous_crop', 'Rice (Paddy)')
        ph = float(data.get('ph', 6.5))

        result = engine.recommend_crop_rotation(
            soil_condition=soil_condition,
            time_of_year=time_of_year,
            temperature=temperature,
            harvest_gap_days=harvest_gap_days,
            previous_crop=previous_crop,
            ph=ph
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def api_history():
    """Fetches consultation records or exports to CSV."""
    records = db.fetch_history(limit=200)
    export_format = request.args.get('format', '').lower()

    if export_format == 'csv':
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow([
            'ID', 'Timestamp', 'Farmer Name', 'Location', 'Soil Type',
            'N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall',
            'Predicted Crop', 'Confidence (%)', 'Recommended Fertilizer',
            'Dosage (kg/ha)', 'Dosage (kg/acre)', 'Explanation'
        ])
        for r in records:
            writer.writerow([
                r['id'], r['timestamp'], r['farmer_name'], r['location'], r['soil_type'],
                r['N'], r['P'], r['K'], r['ph'], r['temperature'], r['humidity'], r['rainfall'],
                r['predicted_crop'], r['confidence'], r['recommended_fertilizer'],
                r['dosage_kg_ha'], r['dosage_kg_acre'], r['explanation']
            ])
        output = si.getvalue()
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=agritech_consultations.csv"}
        )

    return jsonify({"history": records}), 200

@app.route('/api/history/<int:rec_id>', methods=['GET'])
def api_get_record(rec_id):
    """Fetches single consultation record by ID."""
    rec = db.fetch_by_id(rec_id)
    if not rec:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({"record": rec}), 200

@app.route('/api/history/<int:rec_id>', methods=['DELETE'])
def api_delete_record(rec_id):
    """Deletes consultation record by ID."""
    success = db.delete_history(rec_id)
    return jsonify({"success": success}), 200

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Returns database summary statistics for dashboard metrics."""
    return jsonify(db.get_statistics()), 200

@app.route('/api/knowledge', methods=['GET'])
def api_knowledge():
    """Returns complete knowledge base in JSON format."""
    return Response(kb.to_json(), mimetype='application/json')

@app.route('/api/retrain', methods=['POST'])
def api_retrain():
    """Retrains models and updates saved crop_model.pkl."""
    try:
        trainer = ModelTrainer()
        trainer.load_dataset()
        trainer.preprocess()
        results = trainer.train()
        save_path = trainer.save_model()
        global predictor
        predictor = CropPredictor()  # Reload active model in memory
        return jsonify({
            "status": "success",
            "saved_model": save_path,
            "best_model": trainer.best_model_name,
            "comparison": {k: round(v['accuracy'] * 100, 2) for k, v in results.items()}
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import sys
    import socket
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    port = int(os.environ.get('PORT', 5000))
    local_ip = get_local_ip()

    print("\n=======================================================")
    print(" [AgriCulture] Smart Crop & Fertilizer Advisor Expert System")
    print(f" * Local PC Browser:   http://127.0.0.1:{port}")
    print(f" * Mobile Phone Link:  http://{local_ip}:{port}")
    print(" (Open Mobile Phone Link in your phone's Chrome/Safari on same Wi-Fi)")
    print("=======================================================\n")
    app.run(host='0.0.0.0', port=port, debug=False)

