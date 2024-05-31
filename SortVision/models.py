from django.db import models
from django.utils import timezone
import uuid
from django.db import models

# Create your models here.

class Main(models.Model):
    Opis = models.TextField(max_length=1024, blank=True, null=True)

class Kraj(models.Model):
    nazwa = models.CharField(max_length=100)
    w_finale = models.BooleanField(default=False)

    def __str__(self):
        return self.nazwa

class Polfinal(models.Model):
    numer = models.PositiveIntegerField()
    kraje = models.ManyToManyField(Kraj, related_name='polfinaly')

class Final(models.Model):
    nazwa = models.CharField(max_length=100, default="Finał")
    kraje = models.ManyToManyField(Kraj, related_name='finaly')

class PunktacjaJury(models.Model):
    kraj = models.ForeignKey(Kraj, related_name='otrzymane_punkty_jury', on_delete=models.CASCADE)
    przyznajacy_kraj = models.ForeignKey(Kraj, related_name='przyznane_punkty_jury', on_delete=models.CASCADE)
    polfinal = models.ForeignKey(Polfinal, related_name='punkty_jury', on_delete=models.CASCADE, null=True, blank=True)
    final = models.ForeignKey(Final, related_name='punkty_jury', on_delete=models.CASCADE, null=True, blank=True)
    punkty = models.PositiveIntegerField()

class PunktacjaWidzowie(models.Model):
    kraj = models.ForeignKey(Kraj, related_name='otrzymane_punkty_widzowie', on_delete=models.CASCADE)
    polfinal = models.ForeignKey(Polfinal, related_name='punkty_widzowie', on_delete=models.CASCADE, null=True, blank=True)
    final = models.ForeignKey(Final, related_name='punkty_widzowie', on_delete=models.CASCADE, null=True, blank=True)
    punkty = models.PositiveIntegerField()

