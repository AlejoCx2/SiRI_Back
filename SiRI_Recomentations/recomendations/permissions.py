import jwt
import os
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from datetime import datetime

def handleAuthToken(request):
        
        xd = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtMZjCP8/jqIHPR9GMgMi
UYW5uQCA0iJE1m4ZY521Lmheh0Noroin4eJKE/XO71wHLT8eDTSOb219ricA0LMJ
P+KVvsLQsYa0VzKLJMd8OlD5pnnHPXdNhjYoqtxPE2j5/bj8glsxn6jvF9lXOp97
vhcekJh4HgY/foKj0hKBD5WpVtZM9Xiuh1nB2q3JUR65hIw5DmDKtxd/A1VBjlUd
3+1F96BORJAeeupzJLtTa6C9yVE50Ru0l5O0gNXmPjrWYgicfFtyImhuaZnf5g6E
vNtTq02nmnRFkjQMRbACQZSZQDpF4tkim9u4GOplEZ3KRYT8o3V+Kz8TNdL2MXFY
PwIDAQAB
-----END PUBLIC KEY-----"""

        method = request.method
        authToken = request.headers.get('Authorization') 
        #print(authToken)
        if authToken == None:
            print("No se envio el token")
            return  "Unauthorized"
            #return  Response({'error': 'Unauthorized'}, status=HTTP_401_UNAUTHORIZED)
        try:
            authToken = authToken[7:]
            decodedToken = jwt.decode(authToken, xd, algorithms=["RS256"])
            if method == 'POST':
                if decodedToken['role'] == 'company':  
                    print("Es una compañia")
                    print(datetime.now().strftime("%H:%M:%S"))
                    return decodedToken['sub_key']
                else:
                    print("Es un Estudiante")
                    return "invalid token"
            if method == 'GET':
                print("Paso por el Get")
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
            print("Fallo el decode")
            print(datetime.now())
            print(authToken)
            return  "invalid token"

class ClasshandleAuthToken(permissions.BasePermission):
    def has_permission(self, request, view):
        xd = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtMZjCP8/jqIHPR9GMgMi
UYW5uQCA0iJE1m4ZY521Lmheh0Noroin4eJKE/XO71wHLT8eDTSOb219ricA0LMJ
P+KVvsLQsYa0VzKLJMd8OlD5pnnHPXdNhjYoqtxPE2j5/bj8glsxn6jvF9lXOp97
vhcekJh4HgY/foKj0hKBD5WpVtZM9Xiuh1nB2q3JUR65hIw5DmDKtxd/A1VBjlUd
3+1F96BORJAeeupzJLtTa6C9yVE50Ru0l5O0gNXmPjrWYgicfFtyImhuaZnf5g6E
vNtTq02nmnRFkjQMRbACQZSZQDpF4tkim9u4GOplEZ3KRYT8o3V+Kz8TNdL2MXFY
PwIDAQAB
-----END PUBLIC KEY-----"""
        #secret = "xd"
        authToken = request.headers.get('Authorization')
        try: 
            authToken = authToken[7:]
            print(authToken)
            #print("Aqui 1 XD")
            decodedToken = jwt.decode(authToken, xd, algorithms=["RS256"])
            #decodedToken = jwt.decode(authToken, os.getenv("AUTH_PUBLIC_KEY"), algorithms=["RS256"])
            #print("Aqui 2 XD")
            print("Si paso los basicos")
            return True
        except:
            return False