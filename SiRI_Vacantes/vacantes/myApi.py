from rest_framework import status
from .models import Vacancy, Companies, Contracts, Requirements
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken, ClasshandleAuthToken
from .serializers import CompaniesSerializers, VacancySerializers
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED

@api_view(['POST'])
#@permission_classes([handleAuthToken])
def createVacante(req):

    sub_key = handleAuthToken(req)
    #print(sub_key)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        res = {'status': 0, 'result': {}, 'msg': ""}
        try:
            company = Companies.objects.get_or_create(nit=req.data['nit'],defaults={'name': req.data['companyName']})
            contrct = Contracts.objects.get(id=req.data['idContract'])

            if company[1]:
                res['msg'] = "Empresa AGREGADA y vacante creada exitosamente"
            else:
                res['msg'] = "Vacante creada exitosamente"
            res['status'] = 1
            # Crea la vacante
            v = Vacancy.objects.create(name=req.data['name'], 
                                    description=req.data['description'], 
                                    additionalInfo=req.data['additionalInfo'], 
                                    salary=req.data['salary'],
                                    modality=req.data['modality'],
                                    place=req.data['place'],
                                    idContract=contrct, 
                                    experience=req.data['experience'],
                                    skills=req.data['skills'],
                                    idCompany=company[0], 
                                    )
            res['result']['vacante'] = VacancySerializers(v).data

            return Response(res)
        
        except Companies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Contracts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class MyModelUpdateView(APIView):
    def put(self, request, pk):
        try:
            contrct = Contracts.objects.get(id=request.data['idContract'])

            vacancy = Vacancy.objects.get(id=pk)
            name = request.data.get('name')
            description = request.data.get('description')
            additionalInfo = request.data.get('additionalInfo')
            salary = request.data.get('salary')
            modality = request.data.get('modality')
            place = request.data.get('place')
            experience = request.data.get('experience')
            skills = request.data.get('skills')

                # Actualizar el atributo directamente
            vacancy.name = name
            vacancy.description = description
            vacancy.additionalInfo = additionalInfo
            vacancy.salary = salary
            vacancy.modality = modality
            vacancy.place = place
            vacancy.experience = experience
            vacancy.skills = skills
            vacancy.idContract = contrct
            vacancy.save()

            serializer = VacancySerializers(vacancy)
            return Response(serializer.data)
        
        except Contracts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) #Response({'msg': "ERROR: Contract Not Found"})#
        except Vacancy.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([ClasshandleAuthToken])
def getVacanciesCompany(req, nit):
    sub_key = handleAuthToken(req)
    #print(sub_key)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        res = {'status': 0, 'result': {}, 'msg': ""}
        vacantes = []
        try:
            c = Companies.objects.get(nit=nit)
            vacas = Vacancy.objects.filter(idCompany=c.id)
            for v in vacas:
                vacantes.append(VacancySerializers(v).data)
            res['result']=vacantes
            return Response(vacantes)
        except Companies.DoesNotExist:
            res['result']=[]
            return Response([])