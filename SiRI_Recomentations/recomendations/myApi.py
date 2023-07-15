from rest_framework import status
from .models import Students, Candidates
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers, CandidatesSerializers
from .funcinalities import vacancyToVector, studentToVector, compareSkills, verifyExperience, updateStudent, getVacantes,loweCase,getStudents
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.status import HTTP_401_UNAUTHORIZED


@api_view(['POST'])
#@permission_classes([handleAuthToken])
def generarRanking(req):
    sub_key = handleAuthToken(req)
    #print(sub_key)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        res = {'status': 0, 'result': {}, 'msg': ""}
        candidates = Candidates.objects.filter(idVacancy=req.data['id'])
        ranking = []
        for c in candidates:
            s = Students.objects.get(code=c.idStudent)
            obj = {}
            obj['Similitud'] = c.score
            obj['Nombre'] = s.name
            obj['Correo'] = s.mail
            obj['Telefono'] = s.phone
            ranking.append(obj)
        ranking = sorted(ranking, key=lambda i: i['Similitud'], reverse=True)
        count = 1
        for obj in ranking:
            obj['Posicion']= str(count)
            count += 1
        #print(ranking)
        res['status']=1
        res['result'] = ranking

        return Response(ranking)

@api_view(['POST'])
#@permission_classes([handleAuthToken])
def apply(req):
    sub_key = handleAuthToken(req)
    #print(sub_key)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        res = {'status': 0, 'result': {}, 'msg': ""}
        # Vacante
        vacancy = req.data['vacancy']
        student_Info = req.data['student']
        justString = vacancy['description'] + " " + vacancy['additionalInfo'] + " " + vacancy["name"]
        for s in vacancy['skills']:
            justString += " " + s

        vacancy_S = vacancyToVector(vacancy['id'],False,justString)
        #print(sum(vacancy_S))

        student_S = studentToVector(req.data['code'],student_Info['profile'],student_Info['experiences'],student_Info['certifications'],student_Info['skills'])
        #print(sum(student_S))
        print('---- Calculando Similitud ----')
        similitud =  cosine_similarity([vacancy_S],[student_S])[0][0]
        print('---- Comprobar habilidades ----')
        skills = compareSkills(vacancy['skills'],student_Info['skills'])
        print('---- Comprobar Experiencia ----')
        verExp = verifyExperience(vacancy['experience'],student_Info['experiences'])

        if verExp['req'] == "N/A":
            score = (0.4*similitud + 0.6*skills)*100
        else:
            if verExp['std'] >= verExp['req']:
                exp = 1
            else:
                exp = verExp['std']/verExp['req']
            score = (0.4*similitud + 0.2*exp + 0.4*skills)*100


        res['result']['similitud'] = similitud
        res['result']['skills'] = skills
        res['result']['exp'] = exp 
        res['result']['score'] = score 

        try:
            student = Students.objects.get(code=req.data['code'])

            res['msg'] = "Apicacion realizada exitosamente"
            res['status'] = 1

            c = Candidates.objects.create(idStudent=student,
                                        idVacancy=vacancy['id'],
                                        score=score)

            return Response(res)
        
        except Students.DoesNotExist:
            res['msg'] = "Estudiante AGREGADO y apicacion realizada exitosamente"
            res['status'] = 1

            sSkl = loweCase(student_Info['skills'])
            saveExp = str(verExp['std'])+" meses"
            name = student_Info['profile']['name']
            mail = student_Info['profile']['mail']
            phone = student_Info['profile']['phone']
            student = Students.objects.create(code=req.data['code'],skills=sSkl,experience=saveExp,name=name,mail=mail,phone=phone)

            c = Candidates.objects.create(idStudent=student,
                                        idVacancy=vacancy['id'],
                                        score=score)
            c.save()
            return Response(res)
    
@api_view(['PUT'])
#@permission_classes([handleAuthToken])
def updateStudentVector(req):
    sub_key = handleAuthToken(req)
    #print(sub_key)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        res = {'status': 0, 'result': {}, 'msg': ""}
        vacancies = req.data['vacancies']
        updt = updateStudent(req.data['code'],req.data['profile'],req.data['experiences'],req.data['certifications'],req.data['skills'])
        
        if updt['msg'] == 'Actualizado':
            res['status'] = 1
            res['msg'] = updt['msg']
            student_S = updt['vector']
            try:
                std = 0
                for v in vacancies:
                    vacancy_S = getVacantes()[v['id']]
                    print('---- Calculando Similitud ----')
                    similitud =  cosine_similarity([vacancy_S],[student_S])[0][0]
                    #print(similitud)
                    print('---- Comprobar habilidades ----')
                    skills = compareSkills(v['skills'],req.data['skills'])
                    #print(skills)
                    print('---- Comprobar Experiencia ----')
                    verExp = verifyExperience(v['experience'],req.data['experiences'])
                    if verExp['std'] >= verExp['req']:
                        exp = 1
                        std = verExp['std']
                    else:
                        exp = verExp['std']/verExp['req']
                        std = verExp['std']
                    #print(exp)
                    score = (0.3*similitud + 0.2*exp + 0.5*skills)*100
                    #print(score)
                    student = Students.objects.get(code=req.data['code'])
                    student.skills = loweCase(req.data['skills'])
                    student.experience = str(std)+" meses"
                    student.name = req.data['profile']['name']
                    student.mail = req.data['profile']['mail']
                    student.phone = req.data['profile']['phone']
                    student.save()
                    c = Candidates.objects.get(idStudent=student.id,idVacancy=v['id'])
                    c.score=score
                    c.save()
                res['result']['aplicaciones'] = len(vacancies)
            except Candidates.DoesNotExist:
                res['result']['aplicaciones'] = 0
        else:
            res['status'] = 1
            res['msg'] = updt['msg']

        return Response(res)

@api_view(['PUT'])
#@permission_classes([handleAuthToken])
def updateVacancyVector(req):
    sub_key = handleAuthToken(req)
    #print(sub_key)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        res = {'status': 0, 'result': {}, 'msg': ""}
        justString = req.data['description'] + " " + req.data['additionalInfo'] + " " + req.data["name"]
        for s in req.data['skills']:
            justString += " " + s
            print(s)

        vacancy_S = vacancyToVector(req.data['id'],True,justString)
        res['status']=1
        res['msg']="Vacante Actualizada"
        try:
            candidates = Candidates.objects.filter(idVacancy=req.data['id'])
            count = 0
            for c in candidates:
                s = Students.objects.get(code=c.idStudent)
                student_S = getStudents()[str(c.idStudent)]
                print('---- Calculando Similitud ----')
                similitud =  cosine_similarity([vacancy_S],[student_S])[0][0]
                #print(similitud)
                print('---- Comprobar habilidades ----')
                skills = compareSkills(req.data['skills'],s.skills)
                #print(skills)
                print('---- Comprobar Experiencia ----')
                verExp = verifyExperience(req.data['experience'],s.experience)
                if verExp['std'] >= verExp['req']:
                    exp = 1
                else:
                    exp = verExp['std']/verExp['req']
                #print(exp)
                score = (0.3*similitud + 0.2*exp + 0.5*skills)*100
                #print(score)
                c = Candidates.objects.get(idStudent=s.id,idVacancy=req.data['id'])
                c.score=score
                c.save()
                count += 1
            res['result']['candidates']= count
            return Response(res)
        except Candidates.DoesNotExist:
            res['result']['candidates']= 0
            return Response(res)


@api_view(['GET'])
def getCandidateVacancies(req):
    sub_key = handleAuthToken(req)
    if sub_key == 'invalid token':
        return  Response({"error": sub_key}, status=status.HTTP_400_BAD_REQUEST)
    elif sub_key == 'Unauthorized':
        return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        print("Entro")
        res = {'status': 0, 'result': {}, 'msg': ""}
        studentVacancies = []
        try:
            student = Students.objects.get(code=sub_key)
            studentId = student.id
            vacancies = Candidates.objects.filter(idStudent=studentId)
            studentVacancies = []
            for v in vacancies:
                studentVacancies.append(v.idVacancy)
            
            res['status']=1
            res['result'] = studentVacancies
            
        except Students.DoesNotExist:
            print("El estudiante no esta en la DB")
            res['status']=1
            res['result'] = studentVacancies

        return Response(studentVacancies)
