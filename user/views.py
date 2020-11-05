import json
import bcrypt
import jwt
import re
import requests

from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse,HttpResponse

from user.models      import User
from product.models   import Product,Image,Watched,ProductLike
from my_settings      import SECRET_KEY,ALGORITHM

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

class KakaoLoginView(View):
    def get(self,request):
        access_token = request.headers['Authorization']
        kakao_header = ({'Authorization':f'Bearer {access_token}'})
        url          = 'https://kapi.kakao.com/v1/user/access_token_info'

        response     = requests.request("GET", url, headers=kakao_header)
        user         = response.json()

#MY_PAGE
class MyPageView(View):
    def get(self,request):
        try:
            user_id   = request.GET.get('user')
#USER
            user      = User.objects.get(id=user_id)
            post_like = User.objects.prefetch_related('postlike_set').get(id=user_id)
            post_like = post_like.postlike_set.all()
            my_info   = {
                "user_name"    : user.name,
                "profile_image": user.image_url,
                "coupon_num"   : user.coupon.all().count(),
                "user_email"   : user.email,
                "point"        : user.cheer_point,
                "liked_num"    : post_like.count(),
                "order_count"  : 2
            }

#Wached
            watched_list = Watched.objects.select_related('product').prefetch_related('product__image_set','product__productlike_set').filter(user_id=user_id)

            seen_class = [{
                "id" : watch.product.id,
                "class_image" : watch.product.image_set.all()[0].image_url,
                "isOpening" : watch.product.is_open,
                "category" : watch.product.sub_category.name,
                "mentor"  : watch.product.creator.nickname,
                "description" : watch.product.name,
                "likeCount" : watch.product.productlike_set.all().count(),
                "cheeredRate" : watch.product.cheered_set.all().count(),
               "thumpsup"  : watch.product.review_set.filter(good_bad=True).count() / watch.product.review_set.all().count(),
                "originPrice" : watch.product.price,
                "discount" : watch.product.discount,
                "month" : 5
            } if watch.product.review_set.all().count() != 0 else {
                "id" : watch.product.id,
                "class_image" : watch.product.image_set.all()[0].image_url,
                "isOpening" : watch.product.is_open,
                "category" : watch.product.sub_category.name,
                "mentor"  : watch.product.creator.nickname,
                "description" : watch.product.name,
                "likeCount" : watch.product.productlike_set.all().count(),
                "cheeredRate" : watch.product.cheered_set.all().count(),
                "thumpsup"  : 0,
                "originPrice" : watch.product.price,
                "discount" : watch.product.discount,
                "month" : 5
            } for watch in watched_list]

    #Liked
            products_like = ProductLike.objects.select_related('user','product').filter(user_id=user_id)

            liked_class = [{
                "id"           : likeproduct.product.id,
                "class_image"  : likeproduct.product.image_set.first().image_url,
                "isOpening"    : likeproduct.product.is_open,
                "category"     : likeproduct.product.sub_category.name,
                "mentor"       : likeproduct.product.creator.nickname,
                "description"  : likeproduct.product.name,
                "likeCount"    : likeproduct.product.productlike_set.all().count(),
                "cheeredRate"  : likeproduct.product.cheered_set.all().count(),
                "thumpsup"     : likeproduct.product.review_set.filter(good_bad=True).count() / likeproduct.product.review_set.all().count(),
                "originPrice"  : likeproduct.product.price,
                "discount"     : likeproduct.product.discount,
                "month"        : 5
            } if likeproduct.product.review_set.all().count() != 0 else {
                "id"           : likeproduct.product.id,
                "class_image"  : likeproduct.product.image_set.first().image_url,
                "isOpening"    : likeproduct.product.is_open,
                "category"     : likeproduct.product.sub_category.name,
                "mentor"       : likeproduct.product.creator.nickname,
                "description"  : likeproduct.product.name,
                "likeCount"    : likeproduct.product.productlike_set.all().count(),
                "cheeredRate"  : likeproduct.product.cheered_set.all().count(),
                "thumpsup"     : 0,
                "originPrice"  : likeproduct.product.price,
                "discount"     : likeproduct.product.discount,
                "month"        : 5
           } for likeproduct in products_like]

#Class_made
            user = User.objects.select_related('creator').get(id=user_id)
            creator = user.creator

            if creator:
                creator_products = creator.product_set.all()

                class_made = [{
                    'id'          : product.id,
                    'class_image' : product.image_set.first().image_url,
                    'title'       : product.name,
                    'category'    : product.sub_category.name,
                    'mentor'      : creator.nickname,
                }for product in creator_products]
            else:
                class_made = []

            return JsonResponse({'message':'Success','mypage':[{'my_info':my_info, 'seen_class':seen_class,'class_made':class_made,'liked_class':liked_class}]},status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'USER DOES NOT EXIST'}, status=400)
