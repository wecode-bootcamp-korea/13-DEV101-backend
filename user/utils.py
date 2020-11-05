import jwt
import json

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET_KEY,ALGORITHM
from user.models import User

def user_validator(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
            user = User.objects.get(id=payload["id"])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
