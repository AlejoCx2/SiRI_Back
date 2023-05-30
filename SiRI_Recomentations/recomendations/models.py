from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Students(models.Model):
    code = models.CharField(max_length=300,null=False,unique=True)
    skills = ArrayField(models.CharField(max_length=100),blank=False, null=False)
    experience = models.CharField(max_length=100,null=False)
    name = models.CharField(max_length=100,null=False)
    mail = models.CharField(max_length=100,null=False)
    phone = models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.code + " - " + self.name
    
class Candidates(models.Model):
    idStudent = models.ForeignKey(Students, on_delete=models.CASCADE, null=False)
    idVacancy = models.IntegerField(null=False)
    score = models.DecimalField(null=False, decimal_places=2, max_digits=5)
    applyed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('idStudent', 'idVacancy'),)

    def __str__(self):
        return str(self.idStudent.code) + " - " + str(self.idVacancy)