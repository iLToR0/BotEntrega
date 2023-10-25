# En myapp/forms.py

from django import forms
from .models import StrategyParameters
from django.forms.widgets import DateInput



   

class StrategyParametersForm(forms.ModelForm):


    class Meta:
        model = StrategyParameters
        fields = ['valorTK', 'startHour', 'endHour','fechaDesde','fechaHasta','tipoTK']
