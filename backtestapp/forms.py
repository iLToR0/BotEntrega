from django import forms
from .models import StrategyParameters

class StrategyParametersForm(forms.ModelForm):
    class Meta:
        model = StrategyParameters
        fields = ['valorTK', 'startHour', 'endHour', 'fechaDesde', 'fechaHasta', 'tipoTK']
        widgets = {
            'fechaDesde': forms.DateInput(attrs={'type': 'date'}),
            'fechaHasta': forms.DateInput(attrs={'type': 'date'}),
        }
