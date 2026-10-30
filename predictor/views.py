import os
import joblib
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.conf import settings
from .forms import MedicalInsuranceForm


BASE_DIR = settings.BASE_DIR
MODEL_PATH = os.path.join(BASE_DIR, 'predictor', 'ml_models', 'medical_insurance_model.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'predictor', 'ml_models', 'model_features.pkl')

try:
    model = joblib.load(MODEL_PATH)
    feature_cols = joblib.load(FEATURES_PATH)
except Exception as e:
    model = None
    feature_cols = None
    print(f"Error loading model or features: {e}")

REF_AVG_NON_SMOKER = 8400
REF_AVG_SMOKER = 32000

def bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 25:
        return "normal"
    elif 25 <= bmi < 30:
        return "overweight"
    else:
        return "obese"

def build_input_row(age, sex, bmi, children, smoker, region):
    category = bmi_category(bmi)
    row = {
        "age": age,
        "bmi": bmi,
        "children": children,
        "sex_male": 1 if sex == "male" else 0,
        "smoker_yes": 1 if smoker == "yes" else 0,
        "region_northwest": 1 if region == "northwest" else 0,
        "region_southest": 1 if region == "southeast" else 0,
        "region_southwest": 1 if region == "southwest" else 0,
        "bmi_category_obese": 1 if category == "obese" else 0,
        "bmi_category_overweight": 1 if category == "overweight" else 0,
        "bmi_category_underweight": 1 if category == "underweight" else 0
    }
    encoded = pd.DataFrame([row])
    return encoded.reindex(columns = feature_cols, fill_value = 0)

def predict_view(request):
    prediction = None
    context = {'form': MedicalInsuranceForm()}

    if model is None:
        context['error'] = "Model is not loaded. Please, ensure they are in the correct directory."
        return render(request, 'predictor/index.html', context)

    if request.method == 'POST':
        form = MedicalInsuranceForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            input_row = build_input_row(
                data['age'], data['sex'], data['bmi'], 
                data['children'], data['smoker'], data['region']
            )
            log_pred = model.predict(input_row)[0]
            prediction = np.expm1(log_pred)
            context.update({
                'form': form,
                'prediction': round(prediction, 2),
                'is_smoker': data['smoker'] == 'yes'
            })

    return render(request, 'predictor/index.html', context)