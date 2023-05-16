from rest_framework import status
from .models import Students
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import handleAuthToken
from .serializers import StudentsSerializers

import os
import nltk
import ssl


@api_view(['POST'])
@permission_classes([handleAuthToken])
def generarRanking(req):

    res = {'status': 0, 'result': {}, 'msg': ""}
    vacancy = req.data['vacancy']

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
    stop_words = set(stopwords.words('english'))
    
    vacancy_V = [word.lower() for word in nltk.word_tokenize(vacancy) if word.isalpha()]
    vacancy_V = [word for word in vacancy_V if word not in stop_words]
    res['status'] = 1

    return Response(res)
