import json
import bcrypt
import jwt
import re
import requests
import boto3
import datetime
import uuid

from django.db.models  import Q
from django.views      import View

# TODO : merge후 수정예정   
# from django.core.cache import cache

from django.http       import JsonResponse,HttpResponse

from user.utils       import user_validator
from user.models      import User,Creator,UserCoupon
from product.models   import Category,SubCategory,Coupon,Level,Product,Introduction,TitleCover,BasicInfo,Watched,ProductLike

from my_settings      import SECRET_KEY,ALGORITHM,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

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
                user        = User.objects.get(email=data['email'])
                password    = data['password']
                db_password = user.password.encode()

                if bcrypt.checkpw(password.encode(),db_password):
                    access_token  = jwt.encode({'id':user.id},SECRET_KEY,algorithm=ALGORITHM)
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
        try:
            access_token = request.headers['Authorization']
            kakao_header = {'Authorization':f'Bearer {access_token}'}

            url          = 'https://kapi.kakao.com/v2/user/me'
            response     = requests.get(url, headers=kakao_header)
            user         = response.json()

            if user['kakao_account']['profile'].get('profile_image_url'):
                image = user['kakao_account']['profile']['profile_image_url']
            else:
                image = None

            if user.get('id'):
                user = User.objects.get_or_create(
                    social_login_id = user.get('id'),
                    name            = user['kakao_account']['profile']['nickname'],
                    social          = SocialPlatform.objects.get(platform='kakao'),
                    image_url       = image
                    )[0]
                access_token = jwt.encode({'id': user.id},SECRET_KEY,algorithm= ALGORITHM).decode('utf-8')

                return JsonResponse({"access_token": access_token}, status=200)

            return JsonResponse({"Message": "INVALID_TOKEN"}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class MyPageView(View):
    @user_validator
    def get(self,request):
        try:
            user_id = request.user.id
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

            watched_list = Watched.objects.select_related('product').prefetch_related('product__image_set','product__productlike_set').filter(user_id=user_id)

            seen_class = [{
                "id"          : watch.product.id,
                "class_image" : watch.product.image_set.all()[0].image_url,
                "isOpening"   : watch.product.is_open,
                "category"    : watch.product.sub_category.name,
                "mentor"      : watch.product.creator.nickname,
                "description" : watch.product.name,
                "likeCount"   : watch.product.productlike_set.all().count(),
                "cheeredRate" : watch.product.cheered_set.all().count(),
               "thumpsup"     : watch.product.review_set.filter(good_bad=True).count() / watch.product.review_set.all().count(),
                "originPrice" : watch.product.price,
                "discount"    : watch.product.discount,
                "month"       : 5
            } if watch.product.review_set.all().count() != 0 else {
                "id"          : watch.product.id,
                "class_image" : watch.product.image_set.all()[0].image_url,
                "isOpening"   : watch.product.is_open,
                "category"    : watch.product.sub_category.name,
                "mentor"      : watch.product.creator.nickname,
                "description" : watch.product.name,
                "likeCount"   : watch.product.productlike_set.all().count(),
                "cheeredRate" : watch.product.cheered_set.all().count(),
                "thumpsup"    : 0,
                "originPrice" : watch.product.price,
                "discount"    : watch.product.discount,
                "month"       : 5
            } for watch in watched_list]

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

        except Exception as e:
            return JsonResponse({'message':f"{e}"},status=400)



class KakaoLoginView(View):
    def get(self,request):
        try:
            access_token = request.headers['Authorization']
            kakao_header = {'Authorization':f'Bearer {access_token}'}

            url          = 'https://kapi.kakao.com/v2/user/me'
            response     = requests.get(url, headers=kakao_header)
            user         = response.json()

            if user['kakao_account']['profile'].get('profile_image_url'):
                image = user['kakao_account']['profile']['profile_image_url']
            else:
                image = None

            if user.get('id'):
                user = User.objects.get_or_create(
                    social_login_id = user.get('id'),
                    name            = user['kakao_account']['profile']['nickname'],
                    social          = SocialPlatform.objects.get(platform='kakao'),
                    image_url       = image
                    )[0]
                access_token = jwt.encode({'id': user.id},SECRET_KEY,algorithm= ALGORITHM).decode('utf-8')

                return JsonResponse({"access_token": access_token}, status=200)

            return JsonResponse({"Message": "INVALID_TOKEN"}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Exception as e:
            return JsonResponse({'message':f"{e}"},status=400)

class BasicInfoView(View):
    @user_validator
    def post(self,request):
        try:
            category        = request.POST['category']
            sub_category    = request.POST['sub_category']
            category_detail = request.POST['category_detail']
            level           = request.POST['level']
            nickname        = request.POST['nickname']

            user_id      = request.user.id
            user         = User.objects.select_related('creator').prefetch_related('creator__product_set').get(id=user_id)
            user_creator = user.creator

            if user_creator:
                product = user_creator.product_set.first()

                if TitleCover.objects.filter(product_id=product.id).exists():
                    image_url = TitleCover.objects.get(product_id=product.id).cover_image_url
                else:
                    image_url = ''

                basic_info = {
                    "category"        : product.basicinfo_set.first().category.name,
                    "sub_category"    : product.basicinfo_set.first().sub_category.name,
                    "category_detail" : product.basicinfo_set.first().category_detail,
                    "product_id"      : product.id,
                    "level"           : product.level.name,
                    "image_url"       : image_url
                }

                return JsonResponse({'message':'Success','basic_info':basic_info},status=200)

            else:
                if user.image_url:
                    image = user.image_url
                else:
                    image=''

                new_creator = Creator.objects.create(
                    image_url    = image,
                    nickname     = nickname,
                    introduction = "나를 소개하세요."
                )
                new_product = Product.objects.create(
                    category_id      = Category.objects.get(name=category).id,
                    sub_category_id  = SubCategory.objects.get(name=sub_category).id,
                    level_id         = Level.objects.get(name=level).id,
                    creator_id       = new_creator.id
                )
                BasicInfo.objects.create(
                    category_id     = new_product.category.id,
                    sub_category_id = new_product.sub_category.id,
                    category_detail = category_detail,
                    product_id      = new_product.id,
                    level_id        = Level.objects.get(name=level).id
                )
                user.creator_id = new_creator.id
                user.save()

# TODO : merge후 수정예정   
                #cache.delete('products')

                return JsonResponse({'message':'Success'},status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'},status=400)
        except Exception as e:
            return JsonResponse({'message':f'{e}'},status=400)


class CoverTitleView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    @user_validator
    def post(self,request,product_id):
        try:
            user_id = request.user.id
            title   = request.POST['title']
            if TitleCover.objects.filter(product_id=product_id).exists():
                if Introduction.objects.filter(product_id=product_id).exists():
                    introduction = Introduction.objects.get(product_id=product_id)
                    cover = TitleCover.objects.get(product_id=product_id)
                    product = Product.objects.get(id=product_id)
                    title_cover = {
                        "title"               : cover.title,
                        "cover_image_url"     : cover.cover_image_url,
                        "thumnail_image_url"  : cover.thumbnail_image_url,
                        'theme_image_url'     : introduction.theme_image_url,
                        'process_image_url'   : introduction.process_image_url,
                        'work_image_url'      : introduction.work_image_url,
                        'theme_description'   : introduction.theme_description,
                        'process_description' : introduction.process_description,
                        'work_description'    : introduction.work_description,
                        "category"            : product.category.name,
                        "sub_category"        : product.sub_category.name,
                        "category_detail"     : product.basicinfo_set.first().category_detail,
                        "product_id"          : product.id,
                        "level"               : product.level.name,
                        "image_url"           : TitleCover.objects.get(product_id=product_id).cover_image_url
                }

                    return JsonResponse({'message':'Success',"title_cover":title_cover},status=200)

                cover = TitleCover.objects.get(product_id=product_id)
                product = Product.objects.get(id=product_id)

                title_cover = {
                    "product_id"          : product_id,
                    "title"               : cover.title,
                    "cover_image_url"     : cover.cover_image_url,
                    "thumnail_image_url"  : cover.thumbnail_image_url,
                    'theme_image_url'     : '',
                    'process_image_url'   : '',
                    'work_image_url'      : '',
                    'theme_description'   : '',
                    'process_description' : '',
                    'work_description'    : '',
                    "category"            : product.category.name,
                    "sub_category"        : product.sub_category.name,
                    "category_detail"     : product.basicinfo_set.first().category_detail,
                    "product_id"          : product.id,
                    "level"               : product.level.name,
                    "image_url"           : TitleCover.objects.get(product_id=product_id).cover_image_url
                }

                return JsonResponse({'message':'Success',"title_cover":title_cover},status=200)

            files     = request.FILES.getlist('file')
            file_urls = []
            for file in files:
                filename = str(uuid.uuid1()).replace('-','')
                self.s3_client.upload_fileobj(
                        file,
                        "class-dev101",
                        filename,
                        ExtraArgs={
                            "ContentType": file.content_type
                        })
                file_urls.append(f"https://s3.ap-northeast-2.amazonaws.com/class-dev101/{filename}")

            cover_title = TitleCover.objects.create(
                product_id = product_id,
                title = title,
                cover_image_url = file_urls[0],
                thumbnail_image_url = file_urls[1]
            )

# TODO : merge후 수정예정   
            #cache.delete('products')

            return JsonResponse({'message':'Success'},status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'},status=400)

        except Exception as e:
            return JsonResponse({'message':f'{e}'},status=400)


class IntroductionView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    @user_validator
    def post(self,request,product_id):
        try:
            user_id = request.user.id
            if Introduction.objects.filter(product_id=product_id).exists():
                product      = Product.objects.get(id=product_id)
                basic_info   = BasicInfo.objects.get(product_id=product_id)
                cover        = TitleCover.objects.get(product_id=product_id)
                introduction = Introduction.objects.get(product_id=product_id)
                data = {
                    'theme_image_url'     : introduction.theme_image_url,
                    'process_image_url'   : introduction.process_image_url,
                    'work_image_url'      : introduction.work_image_url,
                    'theme_description'   : introduction.theme_description,
                    'process_description' : introduction.process_description,
                    'work_description'    : introduction.work_description,
                    "category"            : product.category.name,
                    "sub_category"        : product.sub_category.name,
                    "category_detail"     : product.basicinfo_set.first().category_detail,
                    "level"               : product.level.name,
                    "image_url"           : TitleCover.objects.get(product_id=product_id).cover_image_url,
                    "product_id"          : product_id,
                    "title"               : cover.title,
                    "cover_image_url"     : cover.cover_image_url,
                    "thumnail_image_url"  : cover.thumbnail_image_url,
                }

                return JsonResponse({'message':'Success','introduction':data},status=200)

            files     = request.FILES.getlist('file')
            file_urls = []
            for file in files:
                filename = str(uuid.uuid1()).replace('-','')
                self.s3_client.upload_fileobj(
                        file,
                        "class-dev101",
                        filename,
                        ExtraArgs={
                            "ContentType": file.content_type
                        })
                file_urls.append(f"https://s3.ap-northeast-2.amazonaws.com/class-dev101/{filename}")

            theme_desc   = request.POST['theme_desc']
            process_desc = request.POST['process_desc']
            work_desc    = request.POST['work_desc']

            Introduction.objects.create(
                product_id = product_id,
                theme_image_url       = file_urls[0],
                process_image_url     = file_urls[1],
                work_image_url        = file_urls[2],
                theme_description     = theme_desc,
                process_description   = process_desc,
                work_description      = work_desc
            )

# TODO : merge후 수정예정   
            #cache.delete('products')

            return JsonResponse({'message':'Success'},status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'},status=400)
        except Exception as e:
            return JsonResponse({'message':f'{e}'},status=400)
