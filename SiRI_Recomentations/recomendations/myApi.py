from rest_framework import status
from .models import Students, Candidates
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers, CandidatesSerializers

import os
import nltk
import ssl
import csv


@api_view(['POST'])
@permission_classes([handleAuthToken])
def generarRanking(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    vacancy = req.data['vacancy']
    justString = vacancy['description'] + " " + vacancy['additionalInfo']

    try:
        _create_unverified_https_context = ssl._create_unverified_context
        print('---- Try ssl ----')
    except AttributeError:
        print('---- Except ssl ----')
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    print('---- Descargando recursos ----')
    nltk.download('punkt')
    nltk.download('stopwords')

    print('---- Let`s Go ----')

    from nltk.corpus import stopwords
    stop_words_es = set(stopwords.words('spanish'))
    stop_words_en = set(stopwords.words('english'))
    stop_words = stop_words_es.union(stop_words_en)

    print('---- Vectorizando Vacante ----')
    vacancy_V = [word.lower() for word in nltk.word_tokenize(justString) if word.isalpha()]
    vacancy_V = [word for word in vacancy_V if word not in stop_words]
    
    with open('features.csv', 'r') as fr:
        reader = csv.reader(fr)
        for i, fila in enumerate(reader, start=1):
            if i == 1:
                words = set(fila)  # Guarda los valores de la fila en un conjunto
                break

    vacancy_S = [1 if word in vacancy_V else 0 for word in words]

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
        # Aplicar
        c = Candidates.objects.create(idStudent=student[0],
                                      idVacancy=req.data['idVacancy'],
                                      score=0)
        res['result']['candidate'] = CandidatesSerializers(c).data

        return Response(res)
    
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)