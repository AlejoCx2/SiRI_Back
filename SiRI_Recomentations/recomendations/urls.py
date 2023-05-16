from rest_framework import routers
from rest_framework.urls import path
from .api import StudentsViewSet
from .myApi import generarRanking

router = routers.DefaultRouter()

router.register('api/students', StudentsViewSet, 'students')

urlpatterns = router.urls
urlpatterns.append(path('api/generar_ranking/', generarRanking, name='generar_ranking'))