# ─────────────────────────────────────────────
# Parameter-Calibrated Dietary & Lifestyle Engine
# ─────────────────────────────────────────────

DIET_RECOMMENDATIONS = {
    "Glucose": {
        "High": {
            "title": "🩸 Diabetes & Blood Sugar Guidance",
            "foods_to_eat": ["Non-starchy vegetables (spinach, broccoli)", "Legumes & lentils", "Chia & flax seeds", "Cinnamon tea"],
            "foods_to_avoid": ["Refined sugars & sodas", "White bread & pastries", "Processed fruit juices"],
            "lifestyle": "Engage in 30 minutes of brisk walking daily after meals to enhance insulin sensitivity."
        }
    },
    "HbA1c": {
        "High": {
            "title": "📊 Glycated Hemoglobin (HbA1c) Control",
            "foods_to_eat": ["Whole grains (quinoa, oats)", "High-fiber greens", "Avocados & almonds"],
            "foods_to_avoid": ["High-GI carbohydrates", "Confectionery & sweets"],
            "lifestyle": "Maintain consistent sleep schedules (7-8 hrs) and monitor fasting blood glucose daily."
        }
    },
    "Hemoglobin": {
        "Low": {
            "title": "🩸 Iron & Anemia Nutritional Protocol",
            "foods_to_eat": ["Spinach & kale", "Lentils & chickpeas", "Pomegranate & beets", "Vitamin C-rich fruits (oranges)"],
            "foods_to_avoid": ["Tea/Coffee immediately after meals (inhibits iron absorption)"],
            "lifestyle": "Combine iron sources with Vitamin C for 3x higher gastrointestinal absorption."
        }
    },
    "Cholesterol": {
        "High": {
            "title": "🫀 Lipid & Cardiovascular Health",
            "foods_to_eat": ["Oats & barley (soluble beta-glucan)", "Walnuts & almonds", "Extra virgin olive oil", "Fatty fish / Omega-3"],
            "foods_to_avoid": ["Trans fats & fried foods", "Full-fat dairy & processed meats"],
            "lifestyle": "Perform 150 minutes of moderate aerobic cardio exercise per week."
        }
    },
    "LDL": {
        "High": {
            "title": "🫀 LDL Lowering Protocol",
            "foods_to_eat": ["Plant sterols & stanols", "Psyllium husk", "Garlic & green tea"],
            "foods_to_avoid": ["Saturated animal fats", "Palm oil & coconut cream"],
            "lifestyle": "Increase daily soluble fiber intake to 25-30g."
        }
    },
    "Creatinine": {
        "High": {
            "title": "💧 Renal Care & Hydration Protocol",
            "foods_to_eat": ["Cranberries & blueberries", "Cauliflower & cabbage", "Olive oil & cucumber"],
            "foods_to_avoid": ["Excessive red meat consumption", "High-sodium processed snacks", "Creatine supplements"],
            "lifestyle": "Maintain optimal hydration (2.5 - 3 Liters of water daily unless fluid restricted)."
        }
    },
    "TSH": {
        "High": {
            "title": "🦋 Thyroid Support Protocol",
            "foods_to_eat": ["Brazil nuts (Selenium)", "Iodized salt & seafood", "Eggs & dairy"],
            "foods_to_avoid": ["Raw un-cooked cruciferous vegetables in large amounts", "Soy supplements"],
            "lifestyle": "Take prescribed levothyroxine on an empty stomach 30-60 minutes before breakfast."
        }
    }
}

def generate_dietary_guidance(analysis):
    recommendations = []

    for param, status in analysis.items():
        if param in DIET_RECOMMENDATIONS and status in DIET_RECOMMENDATIONS[param]:
            recommendations.append(DIET_RECOMMENDATIONS[param][status])

    return recommendations
