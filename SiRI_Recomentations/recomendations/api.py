from .models import Students
from .serializers import StudentsSerializers
from rest_framework import viewsets, permissions
from .permissions import handleAuthToken

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    permission_classes = [handleAuthToken]#permissions.AllowAny
    serializer_class = StudentsSerializers