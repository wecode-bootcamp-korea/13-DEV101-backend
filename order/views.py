import json
import random
from twilio.rest import Client

from django.views import View
from django.http import JsonResponse

from .models import Order, SmsAuth
from product.models import Product
from user.models import User
from my_settings import SMS_ACCESS_KEY_ID, SMS_ACCESS_SECRET_KEY, SMS_SEND_PHONE_NUMBER

class OrderView(View):
    def get(self,request, product_id):
        try:
            # 데코레이터 머지되면 씌울 예정
            user_id = 1
            product = Product.objects.get(id=product_id)
            user    = User.objects.get(id=user_id)
            
            info = {
                'creator'     : product.creator.nickname,
                'class_image' : product.image_set.first().image_url,
                'username'    : user.name,
                'phone_number': user.phone_number,
                'price'       : product.price,
                'discount'    : int(product.price*product.discount),
                'total'       : int(product.price-int((product.price*product.discount)))
            }
            return JsonResponse(info, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message':'NO_PRODUCT'}, status=400)

    def post(self,request, product_id):
        try:
            # 데코레이터 머지되면 씌울 예정
            user_id      = 1
            data         = json.loads(request.body)
            product      = Product.objects.get(id=product_id)
            username     = data['username']
            phone_number = data['phone_number']
            price        = data['price']

            order=Order.objects.create(
                product_id      = product_id,
                user_id         = user_id,
                name            = username,
                phone_number    = phone_number,
                total_price     = price,
                status_id       = 1,
                payment_type_id = 1
            )
            return JsonResponse({'order_info':order.id}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message':'NO_PRODUCT'}, status=404)

class SmsAuthView(View):
    def send_sms(self, phone_number, auth_number):
        account_sid = SMS_ACCESS_KEY_ID
        auth_token  = SMS_ACCESS_SECRET_KEY
        from_number = SMS_SEND_PHONE_NUMBER
        to_number   = phone_number
        message     = f"인증번호는 {auth_number}입니다."
        client      = Client(account_sid, auth_token)
        message     = client.messages.create(to=to_number,
                                            from_=from_number,
                                            body=message)

    def post(self, request):
        try:
            data         = json.loads(request.body)
            # 데코레이터 머지되면 씌울 예정
            user_id      = 1
            phone_number = data['phone_number']
            phone_number = '+82'+phone_number[1:]
            auth_number  = random.randint(1000,9999)
            user, created=SmsAuth.objects.update_or_create(phone_number=phone_number, user_id=user_id, defaults={'auth_number':auth_number})
            
            self.send_sms(phone_number=phone_number, auth_number=auth_number)

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)


class SmsAuthCheckView(View):
    def post(self, request):
        try:
            data               = json.loads(request.body)
            # 데코레이터 머지되면 씌울 예정
            user_id            = 1
            input_auth_number  = data['auth_number']
            phone_number       = data['phone_number']
            phone_number       = '+82'+phone_number[1:]
            stored_auth_number = SmsAuth.objects.get(user_id=user_id, phone_number=phone_number).auth_number
            if int(input_auth_number) == stored_auth_number:
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'CHECK_VERIFICATION_NUMBER'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)