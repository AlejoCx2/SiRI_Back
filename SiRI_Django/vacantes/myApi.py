from rest_framework import status
from .models import Vacancy, Companies, Contracts, Requirements
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken

@api_view(['POST'])
@permission_classes([handleAuthToken])
def createVacante(req):

    res = {'status': 0, 'company':{}, 'msg':""}
    try:
        company = list(Companies.objects.filter(nit=req.data['nit']).values())
    except Companies.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if req.method == 'POST':
        if len(company)>0:
            res['status'] = 1
            res['company'] = company[0]
            res['msg'] = "Empresa encontrada exitosamente"
            return Response(res)
        else:
            res['msg'] = "Usuario no Registrado"
            return Response(res)
