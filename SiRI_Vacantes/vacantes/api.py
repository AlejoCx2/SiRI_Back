from .models import Vacancy, Companies, Contracts, Requirements
from .serializers import CompaniesSerializers, ContractsSerializers, VacancySerializers, RequirementsSerializers
from rest_framework import viewsets, permissions
from .permissions import handleAuthToken

class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    permission_classes = [handleAuthToken]
    serializer_class = CompaniesSerializers

class ContractsViewSet(viewsets.ModelViewSet):
    queryset = Contracts.objects.all()
    permission_classes = [handleAuthToken]
    serializer_class = ContractsSerializers

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    permission_classes = [handleAuthToken]
    serializer_class = VacancySerializers

class RequirementsViewSet(viewsets.ModelViewSet):
    queryset = Requirements.objects.all()
    permission_classes = [handleAuthToken]
    serializer_class = RequirementsSerializers