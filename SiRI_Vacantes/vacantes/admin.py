from django.contrib import admin
from .models import Companies, Contracts, Requirements, Vacancy

# Register your models here.
admin.site.register(Companies)
admin.site.register(Contracts)
admin.site.register(Requirements)
admin.site.register(Vacancy)

