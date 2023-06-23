from .models import Students, Candidates
from .serializers import StudentsSerializers, CandidatesSerializers
from rest_framework import viewsets, permissions
from .permissions import ClasshandleAuthToken

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    permission_classes = [ClasshandleAuthToken]#permissions.AllowAny
    serializer_class = StudentsSerializers

class CandidatesViewSet(viewsets.ModelViewSet):
    queryset = Candidates.objects.all()
    permission_classes = [ClasshandleAuthToken]#permissions.AllowAny
    serializer_class = CandidatesSerializers