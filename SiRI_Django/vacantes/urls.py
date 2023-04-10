from rest_framework import routers
from .api import CompaniesViewSet, ContractsViewSet, VacancyViewSet, RequirementsViewSet

router = routers.DefaultRouter()

router.register('api/companies', CompaniesViewSet, 'companies')
router.register('api/contracts', ContractsViewSet, 'contracts')
router.register('api/vacancy', VacancyViewSet, 'vacancy')
router.register('api/requirements', RequirementsViewSet, 'requirements')

urlpatterns = router.urls