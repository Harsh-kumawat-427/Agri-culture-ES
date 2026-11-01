"""
Smart Crop and Fertilizer Advisor - Expert System UI
Supports both Streamlit UI and Tkinter GUI Form with Report View
as specified in the project architecture notes.
"""

import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Ensure package root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

try:
    from crop_expert_system.knowledge_base import KnowledgeBase
    from crop_expert_system.predictor import CropPredictor, SoilInput
    from crop_expert_system.inference_engine import InferenceEngine
    from crop_expert_system.database import DatabaseManager
except ImportError:
    from knowledge_base import KnowledgeBase
    from predictor import CropPredictor, SoilInput
    from inference_engine import InferenceEngine
    from database import DatabaseManager


def run_streamlit_app():
    """Streamlit Application matching Section 8 of project notes."""
    import streamlit as st
    import pandas as pd

    st.set_page_config(
        page_title="Smart Crop & Fertilizer Advisor",
        page_icon="🌱",
        layout="wide"
    )

    st.title("🌱 Smart Crop and Fertilizer Advisor")
    st.subheader("AI Expert System: ML Crop Prediction + Rule-Based Fertilizer Advice")

    # Initialize engines
    @st.cache_resource
    def load_resources():
        kb = KnowledgeBase()
        predictor = CropPredictor()
        engine = InferenceEngine(kb)
        db = DatabaseManager()
        return kb, predictor, engine, db

    kb, predictor, engine, db = load_resources()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📋 Enter Soil & Weather Parameters")
        farmer_name = st.text_input("Farmer Name", value="Ramesh Kumar")
        location = st.text_input("Farm Location", value="North Field Plot #4")
        soil_type = st.selectbox(
            "Soil Type",
            ["Loamy", "Clayey", "Sandy", "Black", "Alluvial", "Red"]
        )

        n_val = st.slider("Nitrogen (N) kg/ha", 0, 250, 80)
        p_val = st.slider("Phosphorus (P) kg/ha", 0, 200, 45)
        k_val = st.slider("Potassium (K) kg/ha", 0, 250, 40)
        ph_val = st.slider("Soil pH", 3.5, 10.0, 6.5, step=0.1)
        temp_val = st.slider("Temperature (°C)", 5.0, 50.0, 24.0, step=0.5)
        hum_val = st.slider("Humidity (%)", 10.0, 100.0, 82.0, step=1.0)
        rain_val = st.slider("Rainfall (mm)", 10.0, 400.0, 220.0, step=1.0)

        submit = st.button("🚀 Run Expert System Inference", type="primary", use_container_width=True)

    with col2:
        st.markdown("### 📊 Expert System Report View")
        if submit:
            soil = SoilInput(
                N=n_val, P=p_val, K=k_val, ph=ph_val,
                temperature=temp_val, humidity=hum_val, rainfall=rain_val
            )
            valid, err = soil.validate()
            if not valid:
                st.error(err)
            else:
                best_crop = predictor.predict_crop(soil)
                top_crops = predictor.top_n_crops(soil, n=3)
                conf = predictor.confidence(soil)
                rec = engine.fire_rules(soil, best_crop, top_crops)
                report = rec.to_report()

                # Save history
                rec_id = db.save_history(
                    farmer_name=farmer_name,
                    location=location,
                    soil_type=soil_type,
                    soil_dict=soil.to_dict(),
                    recommendation_report=report,
                    confidence=conf
                )

                st.success(f"Consultation Saved in Database (ID: #{rec_id})")

                # Predicted crop card
                st.metric(
                    label="Optimal Predicted Crop (ML)",
                    value=report["crop_display"],
                    delta=f"{conf:.1f}% Match"
                )

                # Fertilizer recommendation
                st.info(
                    f"**Recommended Fertilizer:** {report['recommended_fertilizer']}\n\n"
                    f"**Prescribed Dosage:** {report['dosage']['kg_per_hectare']} kg/ha "
                    f"({report['dosage']['kg_per_acre']} kg/acre)"
                )

                # Explanation Facility
                st.markdown("#### 💡 Explanation Facility Reasoning")
                st.write(report["explanation"])

                # Fired Rules
                st.markdown("#### ⚙️ Fired Knowledge Base Rules")
                for r in report["fired_rules"]:
                    st.code(f"Rule {r['rule_id']}: {r['condition']} -> {r['suggested_fertilizer']}")

                # Benchmark Chart
                st.markdown("#### 📈 Soil Nutrients vs Ideal Benchmark")
                benchmarks = report["ideal_benchmarks"]
                chart_data = pd.DataFrame({
                    "Nutrient": ["N", "P", "K"],
                    "Your Soil": [n_val, p_val, k_val],
                    "Ideal Crop Benchmark": [
                        benchmarks.get("ideal_N", 0),
                        benchmarks.get("ideal_P", 0),
                        benchmarks.get("ideal_K", 0)
                    ]
                }).set_index("Nutrient")
                st.bar_chart(chart_data)
        else:
            st.info("👈 Enter soil test values on the left and click **Run Expert System Inference**.")


def run_tkinter_app():
    """Tkinter Desktop Form with a Report View matching Section 2 of project notes."""
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext

    kb = KnowledgeBase()
    predictor = CropPredictor()
    engine = InferenceEngine(kb)
    db = DatabaseManager()

    root = tk.Tk()
    root.title("AgriCulture - Smart Crop & Fertilizer Advisor Expert System")
    root.geometry("1000x720")
    root.configure(bg="#f8faf7")

    # Header Banner
    header = tk.Frame(root, bg="#2c5f2d", pady=15)
    header.pack(fill="x")
    title_lbl = tk.Label(
        header,
        text="🌱 Smart Crop & Fertilizer Advisor (AI Expert System)",
        font=("Georgia", 16, "bold"),
        fg="#ffffff",
        bg="#2c5f2d"
    )
    title_lbl.pack()
    subtitle_lbl = tk.Label(
        header,
        text="College Subject Project • Machine Learning Crop Prediction + Rule-Based Fertilizer Advice",
        font=("Arial", 10),
        fg="#eaf3df",
        bg="#2c5f2d"
    )
    subtitle_lbl.pack()

    # Main split container
    main_frame = tk.Frame(root, bg="#f8faf7", padx=20, pady=15)
    main_frame.pack(fill="both", expand=True)

    # Left frame: Inputs
    left_frame = tk.LabelFrame(
        main_frame,
        text=" Enter Soil Nutrients & Weather Data ",
        font=("Arial", 11, "bold"),
        fg="#1e451f",
        bg="#ffffff",
        padx=15,
        pady=10
    )
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Form Fields
    entries = {}
    fields = [
        ("Farmer Name:", "farmer_name", "Ramesh Kumar"),
        ("Farm Location:", "location", "North Field Plot #4"),
        ("Nitrogen (N) kg/ha:", "N", "80"),
        ("Phosphorus (P) kg/ha:", "P", "45"),
        ("Potassium (K) kg/ha:", "K", "40"),
        ("Soil pH (0-14):", "ph", "6.5"),
        ("Temperature (°C):", "temperature", "24.0"),
        ("Humidity (%):", "humidity", "82.0"),
        ("Rainfall (mm):", "rainfall", "220.0"),
    ]

    for label_text, key, default_val in fields:
        row = tk.Frame(left_frame, bg="#ffffff", pady=3)
        row.pack(fill="x")
        lbl = tk.Label(row, text=label_text, width=20, anchor="w", bg="#ffffff", font=("Arial", 9, "bold"))
        lbl.pack(side="left")
        ent = tk.Entry(row, font=("Arial", 9))
        ent.insert(0, default_val)
        ent.pack(side="right", fill="x", expand=True)
        entries[key] = ent

    # Soil type dropdown
    row_st = tk.Frame(left_frame, bg="#ffffff", pady=3)
    row_st.pack(fill="x")
    lbl_st = tk.Label(row_st, text="Soil Type:", width=20, anchor="w", bg="#ffffff", font=("Arial", 9, "bold"))
    lbl_st.pack(side="left")
    soil_combo = ttk.Combobox(row_st, values=["Loamy", "Clayey", "Sandy", "Black", "Alluvial", "Red"], state="readonly")
    soil_combo.current(0)
    soil_combo.pack(side="right", fill="x", expand=True)

    # Right frame: Report View
    right_frame = tk.LabelFrame(
        main_frame,
        text=" Expert Recommendation & Explanation Facility ",
        font=("Arial", 11, "bold"),
        fg="#1e451f",
        bg="#ffffff",
        padx=15,
        pady=10
    )
    right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

    report_text = scrolledtext.ScrolledText(right_frame, wrap="word", font=("Arial", 10), bg="#fdfdfc")
    report_text.pack(fill="both", expand=True)
    report_text.insert(
        "1.0",
        "=== READY FOR INFERENCE ===\n\n"
        "Enter soil data on the left panel and click 'Run Expert System Inference' below.\n\n"
        "The system will execute:\n"
        "1. Machine Learning crop classification.\n"
        "2. Forward-chaining production rule matching.\n"
        "3. Deficit dosage calculation in kg/ha and kg/acre.\n"
        "4. Transparent explanation facility reasoning.\n"
        "5. SQLite database history persistence.\n"
    )

    def on_run_inference():
        try:
            soil = SoilInput(
                N=float(entries["N"].get()),
                P=float(entries["P"].get()),
                K=float(entries["K"].get()),
                ph=float(entries["ph"].get()),
                temperature=float(entries["temperature"].get()),
                humidity=float(entries["humidity"].get()),
                rainfall=float(entries["rainfall"].get()),
            )

            valid, err = soil.validate()
            if not valid:
                messagebox.showerror("Validation Error", err)
                return

            best_crop = predictor.predict_crop(soil)
            top_crops = predictor.top_n_crops(soil, n=3)
            conf = predictor.confidence(soil)
            rec = engine.fire_rules(soil, best_crop, top_crops)
            report = rec.to_report()

            # Save in SQLite
            rec_id = db.save_history(
                farmer_name=entries["farmer_name"].get(),
                location=entries["location"].get(),
                soil_type=soil_combo.get(),
                soil_dict=soil.to_dict(),
                recommendation_report=report,
                confidence=conf
            )

            # Build report string
            out = []
            out.append(f"===========================================================")
            out.append(f"      SMART CROP & FERTILIZER ADVISORY REPORT #{rec_id}")
            out.append(f"===========================================================\n")
            out.append(f"Farmer: {entries['farmer_name'].get()}  |  Location: {entries['location'].get()}")
            out.append(f"Soil Type: {soil_combo.get()}  |  Model: {predictor.model_name}\n")
            out.append(f"-----------------------------------------------------------")
            out.append(f"1. OPTIMAL CROP PREDICTION (MACHINE LEARNING)")
            out.append(f"-----------------------------------------------------------")
            out.append(f"Predicted Crop: {report['crop_display'].upper()}")
            out.append(f"Prediction Confidence: {conf:.2f}%\n")
            out.append(f"Top 3 Crop Ranking:")
            for idx, c in enumerate(top_crops, 1):
                out.append(f"   {idx}. {c['crop'].capitalize():<15} ({c['confidence']}%)")

            out.append(f"\n-----------------------------------------------------------")
            out.append(f"2. FERTILIZER PRESCRIPTION (RULE-BASED INFERENCE)")
            out.append(f"-----------------------------------------------------------")
            out.append(f"Prescribed Fertilizer: {report['recommended_fertilizer']}")
            out.append(f"Dosage Rate:          {report['dosage']['kg_per_hectare']} kg/hectare")
            out.append(f"                      {report['dosage']['kg_per_acre']} kg/acre\n")

            out.append(f"-----------------------------------------------------------")
            out.append(f"3. EXPLANATION FACILITY (WHY THIS WAS RECOMMENDED)")
            out.append(f"-----------------------------------------------------------")
            out.append(f"{report['explanation']}\n")

            out.append(f"-----------------------------------------------------------")
            out.append(f"4. ACTIVE KNOWLEDGE BASE RULES TRIGGERED")
            out.append(f"-----------------------------------------------------------")
            for r in report["fired_rules"]:
                out.append(f"• Rule {r['rule_id']}: {r['condition']}")
                out.append(f"  Advice: {r['advice']}")

            out.append(f"\n[Saved to SQLite: expert_system_history.db]")

            report_text.delete("1.0", tk.END)
            report_text.insert("1.0", "\n".join(out))
            messagebox.showinfo("Success", f"Inference complete! Recommended Crop: {report['crop_display']}")

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    # Button Bar
    btn_frame = tk.Frame(left_frame, bg="#ffffff", pady=15)
    btn_frame.pack(fill="x")
    run_btn = tk.Button(
        btn_frame,
        text="🚀 Run Expert System Inference",
        font=("Arial", 11, "bold"),
        bg="#2c5f2d",
        fg="#ffffff",
        padx=10,
        pady=8,
        cursor="hand2",
        command=on_run_inference
    )
    run_btn.pack(fill="x")

    root.mainloop()


if __name__ == "__main__":
    # If invoked via streamlit CLI: streamlit run crop_expert_system/app.py
    if "streamlit" in sys.modules or (len(sys.argv) > 1 and "run" in sys.argv):
        try:
            run_streamlit_app()
        except ImportError:
            print("Streamlit not installed. Launching Desktop GUI form instead...")
            run_tkinter_app()
    else:
        # Check if user specified --gui or standard execution
        if "--gui" in sys.argv or os.environ.get("AGRI_UI") == "tkinter":
            run_tkinter_app()
        else:
            # Try streamlit if available, otherwise launch desktop form
            try:
                import streamlit
                run_streamlit_app()
            except ImportError:
                print("\n[AgriTech] Streamlit not in environment. Launching Tkinter form with report view...")
                run_tkinter_app()

