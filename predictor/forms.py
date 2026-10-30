from django import forms


class MedicalInsuranceForm(forms.Form):
    SEX_CHOICES = [('male', 'Male'), ('female', 'Female')]
    SMOKER_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    REGION_CHOICES = [
        ('northeast', 'Northeast'),
        ('northwest', 'Northwest'),
        ('southeast', 'Southeast'),
        ('southwest', 'Southwest')
    ]

    age = forms.IntegerField(min_value = 18, max_value = 64, initial = 30, label = "Age")
    sex = forms.ChoiceField(choices = SEX_CHOICES, initial = 'male', label = "Sex")
    bmi = forms.FloatField(min_value = 15.0, max_value = 55.0, initial = 26.0, label = "BMI")
    children = forms.IntegerField(min_value = 0, max_value = 5, initial = 0, label = "Children")
    smoker = forms.ChoiceField(choices = SMOKER_CHOICES, initial = 'no', label = "Smoker")
    region = forms.ChoiceField(choices = REGION_CHOICES, initial = 'northeast', label = "Region")
