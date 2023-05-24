from rest_framework import status
from .models import Students, Candidates
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers, CandidatesSerializers
from .funcinalities import vacancyToVector


@api_view(['POST'])
@permission_classes([handleAuthToken])
def generarRanking(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    vacancy = req.data['vacancy']
    justString = vacancy['description'] + " " + vacancy['additionalInfo']

    

    res['status']=1
    res['result']=sum(vacancy_S)

    return Response(res)

@api_view(['POST'])
@permission_classes([handleAuthToken])
def apply(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    try:
        student = Students.objects.get_or_create(code=req.data['code'])

        if student[1]:
            res['msg'] = "Estudiante AGREGADO y apicacion realizada exitosamente"
        else:
            res['msg'] = "Apicacion realizada exitosamente"
        res['status'] = 1
        # Vacante
        vacancy = req.data['vacancy']
        justString = vacancy['description'] + " " + vacancy['additionalInfo'] + " " + vacancy["name"]

        vacancy_S = vacancyToVector(justString)
        

        c = Candidates.objects.create(idStudent=student[0],
                                      idVacancy=req.data['idVacancy'],
                                      score=0)
        res['result']['candidate'] = CandidatesSerializers(c).data

        return Response(res)
    
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)