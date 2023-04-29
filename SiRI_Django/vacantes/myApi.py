from rest_framework import status
from .models import Vacancy, Companies, Contracts, Requirements
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import CompaniesSerializers, VacancySerializers


@api_view(['POST'])
@permission_classes([handleAuthToken])
def createVacante(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    try:
        company = Companies.objects.get_or_create(nit=req.data['nit'])
        contrct = Contracts.objects.get(id=req.data['idContract'])
    except Companies.DoesNotExist or Contracts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if company[1]:
        res['msg'] = "Empresa AGREGADA y vacante creada exitosamente"
    else:
        res['msg'] = "Vacante creada exitosamente"
    res['status'] = 1
    # Crea la vacante
    v = Vacancy.objects.create(name=req.data['name'], description=req.data['description'], additionalInfo=req.data['additionalInfo'],
                               keyWords=req.data['keyWords'], salary=req.data['salary'], experience=req.data['experience'], idCompany=company[0], idContract=contrct)
    res['result']['vacante'] = VacancySerializers(v).data

    return Response(res)
