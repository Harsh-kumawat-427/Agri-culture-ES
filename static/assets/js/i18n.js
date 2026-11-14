/**
 * AgriCulture AI Expert System - Internationalization (i18n) Engine
 * Provides dual-language support: English (en) and Hindi (hi - हिन्दी).
 */

const AGRI_TRANSLATIONS = {
  en: {
    "nav_home": "Home",
    "nav_advisor": "AI Soil & Crop Advisor",
    "nav_rotation": "Seasonal & Crop Rotation",
    "nav_knowledge": "Knowledge Base",
    "nav_records": "Consultation Records",
    "nav_new_test": "New Consultation",
    "btn_lang": "हिन्दी",
    "project_by": "Project By",
    "brand_tagline": "AI Expert System",
    
    // Advisor Form Labels
    "form_title": "Soil Testing & Weather Input Form",
    "form_subtitle": "Validated against agronomical feasibility bounds",
    "farmer_name_label": "Farmer Name",
    "location_label": "Farm Location / Plot",
    "soil_type_label": "Soil Classification",
    "season_label": "Sowing Season / Time",
    "prev_crop_label": "Previous Crop Harvested",
    "gap_label": "Gap Before Next Crop",
    "days_unit": "Days",
    "macronutrients_title": "1. Primary Macronutrients (N-P-K in kg/ha)",
    "n_label": "Nitrogen (N)",
    "p_label": "Phosphorus (P)",
    "k_label": "Potassium (K)",
    "env_title": "2. Soil Reaction & Environmental Parameters",
    "ph_label": "Soil Reaction (pH)",
    "temp_label": "Average Temperature (°C)",
    "humidity_label": "Relative Humidity (%)",
    "rainfall_label": "Rainfall (mm)",
    "btn_run_advisory": "Run Expert Advisory Inference",
    "quick_presets": "Quick Field Presets:",
    "swipe_hint": "Swipe horizontally",
    "shc_guide_btn": "How to Read Soil Health Card",

    // Advisor Results Display
    "optimal_crop": "Optimal Crop Recommendation",
    "ml_confidence": "ML Posterior Probability",
    "rec_fertilizer_title": "Formulated Fertilizer Dosage",
    "field_fallow_status": "Fallow Window Compatibility",
    "reasoning_title": "Agronomic Explanation & Decision Reasoning",
    "calculation_steps_title": "Step-by-Step Dosage Formulation Arithmetic",
    "rules_fired_title": "Triggered Production Rules",
    "field_tips_title": "Field Management Recommendations",
    "runner_up_title": "Alternative Crop Candidates Evaluated by ML",
    "btn_print_report": "Print / Download PDF Report",
    "btn_view_report": "View Full Report Page",
    
    // Rotation Form
    "rot_title": "Crop Recommendation by Soil, Time, Temp & Harvest Gap",
    "rot_subtitle": "Smart Crop Rotation & Harvest Window Engine",
    "rot_form_title": "Cropping Parameters",
    "rot_irrigation_label": "Irrigation Availability & Water Source",
    "rot_disease_label": "Previous Crop Disease / Pest History",
    "btn_rot_submit": "Recommend Optimal Crop & Rotation Plan",
    "disclaimer_text": "Disclaimer: Academic project demonstration for Medi-Caps University. Verify recommendations with an agricultural extension officer or certified soil testing laboratory."
  },
  hi: {
    "nav_home": "होम",
    "nav_advisor": "मृदा व फसल सलाहकार",
    "nav_rotation": "मौसमी व फसल चक्र",
    "nav_knowledge": "ज्ञान भंडार (Knowledge Base)",
    "nav_records": "परामर्श रिकॉर्ड",
    "nav_new_test": "नया परीक्षण",
    "btn_lang": "English",
    "project_by": "परियोजना निर्माता",
    "brand_tagline": "एआई विशेषज्ञ प्रणाली",

    // Advisor Form Labels
    "form_title": "मिट्टी परीक्षण एवं मौसम इनपुट फॉर्म",
    "form_subtitle": "कृषि विज्ञान व्यवहार्यता मानकों द्वारा सत्यापित",
    "farmer_name_label": "किसान का नाम",
    "location_label": "खेत का स्थान / ब्लॉक",
    "soil_type_label": "मिट्टी का वर्गीकरण",
    "season_label": "बुवाई का मौसम / समय",
    "prev_crop_label": "पिछली काटी गई फसल",
    "gap_label": "अगली बुवाई से पहले खाली दिन (अंतराल)",
    "days_unit": "दिन",
    "macronutrients_title": "1. प्राथमिक मुख्य पोषक तत्व (N-P-K किग्रा/हेक्टेयर)",
    "n_label": "नाइट्रोजन (N)",
    "p_label": "फास्फोरस (P)",
    "k_label": "पोटाश (K)",
    "env_title": "2. मिट्टी का पीएच और पर्यावरणीय कारक",
    "ph_label": "मिट्टी का पीएच (pH मान)",
    "temp_label": "औसत तापमान (°C)",
    "humidity_label": "सापेक्ष आर्द्रता (%)",
    "rainfall_label": "वर्षा (मिमी)",
    "btn_run_advisory": "विशेषज्ञ कृषि सलाह प्राप्त करें",
    "quick_presets": "त्वरित खेत प्रीसेट:",
    "swipe_hint": "दाएं-बाएं स्वाइप करें",
    "shc_guide_btn": "मृदा स्वास्थ्य कार्ड कैसे समझें?",

    // Advisor Results Display
    "optimal_crop": "सर्वोत्तम अनुशंसित फसल",
    "ml_confidence": "एमएल मॉडल प्रायिकता",
    "rec_fertilizer_title": "उर्वरक की सटीक मात्रा व खुराक",
    "field_fallow_status": "बुवाई अंतराल अनुकूलता",
    "reasoning_title": "कृषि वैज्ञानिक कारण व व्याख्या (Explainable AI)",
    "calculation_steps_title": "उर्वरक मात्रा गणना के चरण",
    "rules_fired_title": "सक्रिय हुए कृषि नियम (Fired Rules)",
    "field_tips_title": "खेत प्रबंधन और सावधानियां",
    "runner_up_title": "एमएल मॉडल द्वारा मूल्यांकित अन्य वैकल्पिक फसलें",
    "btn_print_report": "प्रिंट करें / पीडीएफ डाउनलोड करें",
    "btn_view_report": "पूर्ण रिपोर्ट देखें",

    // Rotation Form
    "rot_title": "मिट्टी, मौसम, तापमान और कटाई अंतराल अनुसार फसल चक्र",
    "rot_subtitle": "स्मार्ट फसल चक्र व कटाई अंतराल प्रणाली",
    "rot_form_title": "फसल व खेत मापदंड",
    "rot_irrigation_label": "सिंचाई की उपलब्धता व जल स्रोत",
    "rot_disease_label": "पिछली फसल में कीट या फंगल रोग का इतिहास",
    "btn_rot_submit": "इष्टतम फसल चक्र योजना प्राप्त करें",
    "disclaimer_text": "चेतावनी: मेडी-कैप्स विश्वविद्यालय के लिए शैक्षणिक प्रोजेक्ट प्रदर्शन। वास्तविक उपयोग से पहले कृषि अधिकारी या अधिकृत मृदा प्रयोगशाला से पुष्टि करें।"
  }
};

function getActiveLanguage() {
  return localStorage.getItem('agri_lang') || 'en';
}

function setActiveLanguage(lang) {
  if (lang !== 'en' && lang !== 'hi') lang = 'en';
  localStorage.setItem('agri_lang', lang);
  applyTranslations(lang);
}

function toggleLanguage() {
  const current = getActiveLanguage();
  const next = current === 'en' ? 'hi' : 'en';
  setActiveLanguage(next);
}

function applyTranslations(lang) {
  const dict = AGRI_TRANSLATIONS[lang] || AGRI_TRANSLATIONS['en'];
  
  // Update elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.innerText = dict[key];
    }
  });

  // Update elements with data-i18n-placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) {
      el.setAttribute('placeholder', dict[key]);
    }
  });

  // Update language switcher button label
  const btn = document.getElementById('lang-label');
  if (btn) {
    btn.innerText = dict['btn_lang'] || (lang === 'en' ? 'हिन्दी' : 'English');
  }

  // Update HTML lang attribute
  document.documentElement.lang = lang;
}

document.addEventListener('DOMContentLoaded', () => {
  const lang = getActiveLanguage();
  applyTranslations(lang);
});
