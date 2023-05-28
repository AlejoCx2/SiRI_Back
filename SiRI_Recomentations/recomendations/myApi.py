from rest_framework import status
from .models import Students, Candidates
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers, CandidatesSerializers
from .funcinalities import vacancyToVector, studentToVector,compareSkills
from sklearn.metrics.pairwise import cosine_similarity


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
        student_Info = req.data['student']
        justString = vacancy['description'] + " " + vacancy['additionalInfo'] + " " + vacancy["name"]
        for s in vacancy['skills']:
            justString += " " + s

        vacancy_S = vacancyToVector(vacancy['id'],vacancy['updated_at'],justString)
        print(sum(vacancy_S))
        student_S = studentToVector(req.data['code'],student_Info['profile'],student_Info['experiences'],student_Info['certifications'],student_Info['skills'])
        print(sum(student_S))

        print('---- Calculando Similitud ----')
        similitud =  cosine_similarity([vacancy_S],[student_S])[0][0]
        #print('---- Comprobar habilidades ----')
        #skills = compareSkills(vacancy['skills'],student_Info['skills'])
        
        #c = Candidates.objects.create(idStudent=student[0],
        #                              idVacancy=req.data['idVacancy'],
        #                              score=0)
        res['result']['similitud'] = similitud
        #res['result']['skills'] = skills

        return Response(res)
    
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)