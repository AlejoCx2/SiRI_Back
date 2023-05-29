from rest_framework import routers
from rest_framework.urls import path
from .api import StudentsViewSet, CandidatesViewSet
from .myApi import generarRanking, apply, updateStudentVector,updateVacancyVector

router = routers.DefaultRouter()

router.register('api/students', StudentsViewSet, 'students')
router.register('api/candidates', CandidatesViewSet, 'candidates')

urlpatterns = router.urls
urlpatterns.append(path('api/generar_ranking/', generarRanking, name='generar_ranking'))
urlpatterns.append(path('api/apply/', apply, name='apply'))
urlpatterns.append(path('api/update/student/', updateStudentVector, name='updateStudent'))
urlpatterns.append(path('api/update/vacancy/', updateVacancyVector, name='updateVacancy'))