import jwt
import os
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

def handleAuthToken(request):
        method = request.method
        authToken = request.headers.get('Authorization') 
        #print(authToken)
        if authToken == None:
            return  "Unauthorized"
            #return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
        try:
            authToken = authToken[7:]   
            decodedToken = jwt.decode(authToken, os.getenv("AUTH_PUBLIC_KEY"), algorithms=["RS256"])
            if method == 'POST':
                if decodedToken['role'] == 'company':  
                    return decodedToken['sub_key']
                else:
                    return "invalid token"
            if method == 'GET':
                
                return decodedToken['sub_key']
            if method == 'PUT':
                if decodedToken['role'] == 'company':  
                    return decodedToken['sub_key']
                else:
                    return "invalid token"
            if method == 'DELETE':
                if decodedToken['role'] == 'company':  
                    return decodedToken['sub_key']
                else:
                    return "invalid token"
        except:
            return  "invalid token"

class ClasshandleAuthToken(permissions.BasePermission):
    def has_permission(self, request, view):
        #secret = "xd"
        authToken = request.headers.get('Authorization')
        try: 
            authToken = authToken[7:]
            #print("Aqui 1 XD")
            decodedToken = jwt.decode(authToken, os.getenv("AUTH_PUBLIC_KEY"), algorithms=["RS256"])
            #print("Aqui 2 XD")
            return True
        except:
            return False