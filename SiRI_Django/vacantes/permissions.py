import os
import jwt
from rest_framework import permissions


class handleAuthToken(permissions.BasePermission):
    def has_permission(self, request, view):
        secret = "xd";
        method = request.method
        authToken = request.headers.get('Authorization')
        try: 
            authToken = authToken[7:]
            #print("Aqui 1 XD")
            #decodedToken = jwt.decode(authToken, os.getenv("AUTH_PUBLIC_KEY"), algorithms=["RS256"])
            #print("Aqui 2 XD")
            #return True
            if authToken  == secret:
                return True
            else:
                return False
            
        except:
            return False
