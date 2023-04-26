from rest_framework import status
from .models import Vacancy, Companies, Contracts, Requirements
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def createVacante(req):
    res = {'status': 0, 'elements': ""}

    return Response(res)
