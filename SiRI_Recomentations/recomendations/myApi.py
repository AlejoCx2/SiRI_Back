from rest_framework import status
from .models import Students, Candidates
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers, CandidatesSerializers
from .funcinalities import vacancyToVector, studentToVector, compareSkills, verifyExperience, updateStudent
from sklearn.metrics.pairwise import cosine_similarity


@api_view(['POST'])
@permission_classes([handleAuthToken])
def generarRanking(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    vacancy = req.data['vacancy']
    justString = vacancy['description'] + " " + vacancy['additionalInfo']

    

    res['status']=1
    res['result']=sum(vacancy)

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
        #print(sum(vacancy_S))
        student_S = studentToVector(req.data['code'],student_Info['profile'],student_Info['experiences'],student_Info['certifications'],student_Info['skills'])
        #print(sum(student_S))

        print('---- Calculando Similitud ----')
        similitud =  cosine_similarity([vacancy_S],[student_S])[0][0]
        print('---- Comprobar habilidades ----')
        skills = compareSkills(vacancy['skills'],student_Info['skills'])
        print('---- Comprobar Experiencia ----')
        exp = verifyExperience(vacancy['experience'],student_Info['experiences'])
        #c = Candidates.objects.create(idStudent=student[0],
        #                              idVacancy=req.data['idVacancy'],
        #                              score=0)
        res['result']['similitud'] = similitud
        res['result']['skills'] = skills
        res['result']['exp'] = exp 

        return Response(res)
    
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes([handleAuthToken])
def updateStudentVector(req):
    res = {'status': 0, 'result': {}, 'msg': ""}
    msg = updateStudent(req.data['code'],req.data['profile'],req.data['experiences'],req.data['certifications'],req.data['skills'])
    res['status'] = 1
    res['msg'] = msg

    return Response(res)
