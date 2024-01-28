from django import forms
from .models import StrategyParameters,StrategyParameters2

class StrategyParametersForm(forms.ModelForm):
    class Meta:
        model = StrategyParameters
        fields = ['valorTK', 'startHour', 'endHour', 'fechaDesde', 'fechaHasta', 'tipoTK']
        widgets = {
            'fechaDesde': forms.DateInput(attrs={'type': 'date'}),
            'fechaHasta': forms.DateInput(attrs={'type': 'date'}),
        }
      

class StrategyParameters2Form(forms.ModelForm):
    class Meta:
        model = StrategyParameters2
        fields = ['valorTK', 'startHour', 'endHour', 'fechaDesde', 'fechaHasta', 'tipoTK', 'stopLoss']
        widgets = {
                'fechaDesde': forms.DateInput(attrs={'type': 'date'}),
                'fechaHasta': forms.DateInput(attrs={'type': 'date'}),
        }

