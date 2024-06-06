from django.db import models
from django.utils import timezone
import uuid
from django.db import models
from PIL import Image

# Create your models here.
from django.db import models
from PIL import Image

class Main(models.Model):
    Opis = models.TextField(max_length=1024, blank=True, null=True)

class Kraj(models.Model):
    nazwa = models.CharField(max_length=100)
    zdjecie = models.ImageField(blank=True, null=True, upload_to='images/')
    zdjecie_height = models.PositiveIntegerField(blank=True, null=True)
    zdjecie_width = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.zdjecie:
            img = Image.open(self.zdjecie.path)
            img = img.resize((60, 40), Image.Resampling.LANCZOS)
            img.save(self.zdjecie.path)
            self.zdjecie_width = img.width
            self.zdjecie_height = img.height
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nazwa

class Polfinal(models.Model):
    POLFINAL_CHOICES = [
        ('1', 'Półfinał 1'),
        ('2', 'Półfinał 2'),
    ]

    kraj = models.ForeignKey(Kraj, on_delete=models.CASCADE, blank=True, null=True)
    polfinal = models.CharField(max_length=1, choices=POLFINAL_CHOICES, blank=True, null=True)
    punkty = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.kraj.nazwa} - Półfinał {self.polfinal}"

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

