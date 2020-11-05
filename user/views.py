import json
import bcrypt
import jwt
import re

from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse,HttpResponse

from user.models      import User
from my_settings      import SECRET_KEY,ALGORITHM
#from user.utils       import user_validator

class SignUpView(View):
    def post(self,request):
        try:
            data         = json.loads(request.body)
            password     = data['password']
            re_password  = data['re_password']

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'Existing user'},status=409)

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
                return JsonResponse({'message':'Invalid Email'},status=400)

            if password != re_password:
                return JsonResponse({'message':'Password Error'},status=400)

            else:
                hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                decoded_password = hashed_password.decode('utf-8')

                User.objects.create(
                    name         = data['name'],
                    email        = data['email'],
                    phone_number = data['phone_number'],
                    password     = decoded_password
                )
                return JsonResponse({'message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'},status=400)
        except:
            return JsonResponse({'message':'Anoter_Error'},status=400)

class SignInView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                password = data['password']
                db_password = user.password.encode()

                if bcrypt.checkpw(password.encode(),db_password):
                    access_token = jwt.encode({'id':user.id},SECRET_KEY,algorithm=ALGORITHM)
                    decoded_token = access_token.decode()

                    return JsonResponse(
                    {'message':'SUCCESS','TOKEN':decoded_token}, status=201)

                else:
                    return JsonResponse({'message':'PASSWORD_ERROR'}, status=400)

            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
