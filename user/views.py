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
            name         = data['name']
            email        = data['email']
            phone_number = data['phone_number']
            password     = data['password']
            re_password  = data['re_password']

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'Existing user'},status=409)

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message':'Invalid Email'},status=400)

            if password != re_password:
                return JsonResponse({'message':'Password Error'},status=400)

            else:
                hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                decoded_password = hashed_password.decode('utf-8')

                User.objects.create(
                    name         = name,
                    email        = email,
                    phone_number = phone_number,
                    password     = decoded_password
                )
                return JsonResponse({'message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'},status=400)
        except:
            return JsonResponse({'message':'Anoter_Error'},status=400)
