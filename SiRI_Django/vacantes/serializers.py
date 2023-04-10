from rest_framework import serializers
from .models import Companies, Contracts, Vacancy, Requirements

class CompaniesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = '__all__' #('atrubute','')
        read_only_fields = ('id',)

class ContractsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__' #('atrubute','')
        read_only_fields = ('id',)

class VacancySerializers(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__' #('atrubute','')
        read_only_fields = ('created_at','id',)

class RequirementsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = '__all__' #('atrubute','')
        read_only_fields = ('id',)