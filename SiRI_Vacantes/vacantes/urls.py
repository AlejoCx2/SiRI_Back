from rest_framework import routers
from rest_framework.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api import CompaniesViewSet, ContractsViewSet, VacancyViewSet, RequirementsViewSet
from .myApi import createVacante, MyModelUpdateView, getVacanciesCompany

router = routers.DefaultRouter()

router.register('api/companies', CompaniesViewSet, 'companies')
router.register('api/contracts', ContractsViewSet, 'contracts')
router.register('api/vacancy', VacancyViewSet, 'vacancy')
router.register('api/requirements', RequirementsViewSet, 'requirements')

urlpatterns = router.urls
urlpatterns.append(path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'))
urlpatterns.append(path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'))
urlpatterns.append(path('api/create/vacancy/', createVacante, name='create_vacante'))
urlpatterns.append(path('api/update/vacancy/<int:pk>/', MyModelUpdateView.as_view(), name='update_vacante'))
urlpatterns.append(path('api/get/vacancies/<str:nit>/', getVacanciesCompany, name='get_vacancies'))