from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Companies(models.Model):
    nit = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.nit

class Contracts(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    idCompany = models.ForeignKey(Companies, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False) # max=1500 testiar
    additionalInfo = models.TextField(null=True, blank=True) # max=1500 testiar
    salary = models.IntegerField(validators=[MinValueValidator(1200000)])
    modality = models.CharField(max_length=100, null=False)
    skills = ArrayField(models.CharField(max_length=100),blank=False, null=False)
    idContract = models.ForeignKey(Contracts, on_delete=models.RESTRICT, null=False)
    experience = models.CharField(max_length=100, null=False)
    place = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.idCompany.nit

class Requirements(models.Model):
    idVacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name + ' - ' + self.idVacancy.name