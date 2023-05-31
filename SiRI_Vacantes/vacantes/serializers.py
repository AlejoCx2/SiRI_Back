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
    contract = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    companyNit = serializers.SerializerMethodField()
    class Meta:
        model = Vacancy
        fields = ('id','company','companyNit','name','description','additionalInfo','salary','modality','place','contract','experience','skills','created_at','updated_at') #('atrubute','')
        read_only_fields = ('created_at','id',)

    def get_contract(self,obj):
        return obj.idContract.name
    
    def get_company(self,obj):
        return obj.idCompany.name
    
    def get_companyNit(self,obj):
        return obj.idCompany.nit

class RequirementsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = '__all__' #('atrubute','')
        read_only_fields = ('id',)