from django.db import models
from django.core.validators import MinValueValidator, ValidationError

def no_negativo(value):
    if value < 0:
        raise ValidationError("El valor no puede ser negativo")

class StrategyParameters(models.Model):
    valorTK = models.FloatField(
        validators=[MinValueValidator(0), no_negativo]
    )
    startHour = models.TimeField()
    endHour = models.TimeField()
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    tipoTK = models.CharField(max_length=1, choices=[('P', 'Puntos'), ('R', 'Ratio')])
    # Agrega campos para otras variables de la estrategia

class StrategyParameters2(models.Model):
    valorTK = models.FloatField(
        validators=[MinValueValidator(0), no_negativo]
    )
    startHour = models.TimeField()
    endHour = models.TimeField()
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    stopLoss = models.FloatField(validators=[MinValueValidator(0), no_negativo])
    tipoTK = models.CharField(max_length=1, choices=[('P', 'Puntos'), ('R', 'Ratio')])
    # Agrega campos para otras variables de la estrategia
