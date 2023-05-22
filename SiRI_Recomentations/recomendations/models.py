from django.db import models

# Create your models here.
class Students(models.Model):
    code = models.CharField(max_length=100,null=False,unique=True)

    def __str__(self):
        return self.code
    
class Candidates(models.Model):
    idStudent = models.ForeignKey(Students, on_delete=models.CASCADE, null=False)
    idVacancy = models.IntegerField(null=False)
    score = models.DecimalField(null=False, decimal_places=2, max_digits=5)
    applyed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.idStudent.code + " - " + self.idVacancy