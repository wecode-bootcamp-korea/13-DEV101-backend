import json
import bcrypt
import jwt
import unittest

from io                             import BytesIO
from PIL                            import Image as img
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test                    import TestCase,Client
from unittest.mock                  import patch,MagicMock

from user.models    import User,Creator,SocialPlatform
from product.models import Product,ProductLike,Image,Category,SubCategory,Level,Coupon,Watched,BasicInfo,TitleCover,Introduction

from my_settings import SECRET_KEY,ALGORITHM

client = Client()

class UserSignupTest(TestCase):
    def setUp(self):
        client = Client()

    def tearDown(self):
            User.objects.all().delete()

    def test_post_user_view(self):
        user = {
            "name"         : "hn",
            "email"        : "hgggg@gmail.com",
            "phone_number" : "01084612249",
            "password"     : "1234",
            "re_password"  : "1234"
        }

        response = client.post('/user/signup',json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code,201)

class UserSigninTest(TestCase):
    def setUp(self):
        client = Client()
        User.objects.create(
            email = 'hgggg@gmail.com',
            password = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            name = "hh",
            phone_number = "01012331233"
        )

    def tearDown(self):
            User.objects.all().delete()

    def test_post_user_view(self):
        user = {
            "email"        : "hgggg@gmail.com",
            "password"     : "1234",
        }

        response = client.post('/user/signin',json.dumps(user),content_type='application/json')
        self.assertEqual(response.status_code,201)

class MyPageTest(TestCase):
    def setUp(self):
        client = Client()
        Category.objects.create(
            id = 1,
            name = "크리에이티브"
            )
        SubCategory.objects.create(
            id = 1,
            category_id = 1,
            name = "데이터/개발"
            )
        Creator.objects.create(
            id           = 1,
            image_url    = 'https://images.unsplash.com/photo-1604713964919-601ea4d01c27?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            nickname     = 'qwerty',
            introduction ='asdasdasdasd'
        )
        Level.objects.create(
            id = 1,
            name = "dd"
        )
        Coupon.objects.create(
            id = 1,
            name = "coupon"
        )
        Product.objects.create(
            id              = 1,
            name            = 'content',
            category_id     = 1,
            sub_category_id = 1,
            creator_id      = 1,
            price           = 100000,
            discount        = 0.32,
            chapter         = 1,
            chapter_detail  = 0,
            subtitle_flag   = False,
            is_checked      = True,
            is_open         = False,
            level_id        = 1,
            coupon_id       = 1
         )
        Product.objects.create(
            id              = 2,
            name            = 'content2',
            category_id     = 1,
            sub_category_id = 1,
            creator_id      = 1,
            price           = 100000,
            discount        = 0.32,
            chapter         = 1,
            chapter_detail  = 1,
            subtitle_flag   = False,
            is_checked      = True,
            is_open         = False,
            level_id        = 1,
            coupon_id       = 1
         )
        User.objects.create(
            id           = 1,
            name         = 'qwerty',
            email        = 'qwerty@gmail.com',
            password     = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone_number = '01012221222',
            image_url    = 'https://images.unsplash.com/photo-1604713964919-601ea4d01c27?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            is_active    = False,
            creator_id   = 1,
            cheer_point  = 10
       )
        ProductLike.objects.create(
             product_id = 1,
             user_id    = 1,
         )
        Watched.objects.create(
             product_id = 1,
             user_id    = 1
         )
        Image.objects.create(
            id = 1,
            image_url = 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            product_id = 1
        )
        Image.objects.create(
            id = 2,
            image_url = 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            product_id = 1
        )
        Image.objects.create(
            id = 3,
            image_url = 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            product_id = 1
         )
        Image.objects.create(
            id = 4,
            image_url = 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            product_id = 2
        )
        Image.objects.create(
            id = 5,
            image_url = 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            product_id = 2
        )
        Image.objects.create(
            id = 6,
            image_url = 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            product_id = 2
         )

    def tearDown(self):
        User.objects.all().delete()
        Creator.objects.all().delete()
        Image.objects.all().delete()
        Product.objects.all().delete()
        ProductLike.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()

    def test_mypage_get_success(self):
        self.maxDiff = None
        response = client.get('/user/me?user=1')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
            'message':'Success','mypage':[{
                'my_info':{
                    "coupon_num": 0,
                    "liked_num": 0,
                    "order_count": 2,
                    "point": 10,
                    "profile_image": 'https://images.unsplash.com/photo-1604713964919-601ea4d01c27?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                    "user_email": "qwerty@gmail.com",
                    "user_name": "qwerty"
            },
                'seen_class':[{
                    "category": "데이터/개발",
                    "cheeredRate": 0,
                    "class_image":'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                   "description": "content",
                    "discount": "0.32",
                    "id": 1,
                    "isOpening": False,
                    "likeCount": 1,
                    "mentor": "qwerty",
                    "month": 5,
                    "originPrice": "100000.00",
                    "thumpsup": 0
                }],
                'class_made':[{
                    "category": "데이터/개발",
                    "class_image": 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                   "id": 1,
                    "mentor": "qwerty",
                    "title": "content"
                },{
                    "category": "데이터/개발",
                    "class_image": 'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                    "id": 2,
                    "mentor": "qwerty",
                    "title": "content2"
                }],
                'liked_class':[{
                    "category": "데이터/개발",
                    "cheeredRate": 0,
                    "class_image":'https://images.unsplash.com/photo-1604683946365-c45ee5528486?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                   "description": "content",
                    "discount": "0.32",
                    "id": 1,
                    "isOpening": False,
                    "likeCount": 1,
                    "mentor": "qwerty",
                    "month": 5,
                    "originPrice": "100000.00",
                    "thumpsup": 0
                }]}]
        })

class KakaoSignInTest(TestCase):
    def setUp(self):
        SocialPlatform.objects.create(id=1,platform='kakao')

    def tearDown(self):
        SocialPlatform.objects.get(platform='kakao').delete()

    @patch('user.views.requests')
    def test_kakao_sign_in(self, mocked_requests):

        client = Client()
        class KakaoResponse:
            def json(self):
                return {
                    "Authorization" : 'fake_token.1234',
                    "id"            : "12345",
                    "kakao_account" : {"profile":{"nickname":"hh"}},
                    "social"        : "kakao"
                }

        mocked_requests.get = MagicMock(return_value = KakaoResponse())
        headers  = {'HTTP_Authorization':'fake_token.1234'}
        response = client.get('/user/kakao/login', **headers)
#        token    = jwt.encode({'id': "12345"},SECRET_KEY,algorithm= ALGORITHM).decode('utf-8')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

class BasicInfoTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = "category"
        )
        SubCategory.objects.create(
            id           = 1,
            category_id  = 1,
            name = "sub"
        )
        Creator.objects.create(
            id           = 1,
            nickname     = "phh",
            image_url    = "http://djakj.djka.co",
            introduction = "yeaaaaaaaaaa"
        )
        User.objects.create(
            id   = 1,
            name = "hh",
            creator_id = 1
        )
        Coupon.objects.create(
            id   = 1,
            name = 'coupon'
        )
        Level.objects.create(
            id   = 1,
            name = 'level'
        )
        Product.objects.create(
            id              = 1,
            name            = "product",
            category_id     = 1,
            sub_category_id = 1,
            creator_id      = 1,
            coupon_id       = 1,
            level_id        = 1
        )
        BasicInfo.objects.create(
            id = 1,
            product_id = 1,
            category_id = 1,
            sub_category_id = 1,
            category_detail = 'category_detail',
            level_id = 1
        )

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Creator.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Coupon.objects.all().delete()
        BasicInfo.objects.all().delete()
        Level.objects.all().delete()

    def test_basic_info(self):
        client = Client()
        self.maxDiff = None
        data = {
            'category' : 'category',
            'sub_category' : 'sub',
            'category_detail' : 'category_detail',
            'level' : 'level',
            'nickname' : 'nickname'
        }
        response = client.post('/user/1/basicinfo',data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
                         {
                             'message':'Success',
                             'basic_info':{
                                'category':'category',
                                 'sub_category':'sub',
                                 'category_detail':'category_detail',
                                 'level':'level',
                                 'image_url':'',
                                 'product_id':1
                             }
                         })

class CoverTitleTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = "category"
        )
        SubCategory.objects.create(
            id           = 1,
            category_id  = 1,
            name = "sub"
        )
        Creator.objects.create(
            id           = 1,
            nickname     = "phh",
            image_url    = "http://djakj.djka.co",
            introduction = "yeaaaaaaaaaa"
        )
        User.objects.create(
            id   = 1,
            name = "hh",
            creator_id = 1
        )
        Coupon.objects.create(
            id   = 1,
            name = 'coupon'
        )
        Level.objects.create(
            id   = 1,
            name = 'level'
        )
        Product.objects.create(
            id              = 1,
            name            = "product",
            category_id     = 1,
            sub_category_id = 1,
            creator_id      = 1,
            coupon_id       = 1,
            level_id        = 1
        )
        BasicInfo.objects.create(
            id = 1,
            product_id = 1,
            category_id = 1,
            sub_category_id = 1,
            category_detail = 'category_detail',
            level_id = 1
        )
        Introduction.objects.create(
            product_id = 1,
            theme_image_url = '',
            process_image_url = '',
            work_image_url = '',
            theme_description = 'qwe',
            process_description = 'qwe',
            work_description = 'qwe'
        )

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Creator.objects.all().delete()
        User.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Product.objects.all().delete()
        BasicInfo.objects.all().delete()
        Introduction.objects.all().delete()
        TitleCover.objects.all().delete()

    @patch('user.views.CoverTitleView.s3_client')
    def test_title_cover(self,mocked_client):
        client = Client()
        self.maxDiff = None
        stream = BytesIO() # pillow로 resizing한 이미지 bytes화
        image = img.new("RGB",(100,100))
        image.save(stream, format='jpeg')

        cover_image_file      = SimpleUploadedFile("cover.jpg", stream.getvalue(), content_type = "image/jpg")
        thumbnail_image_file  = SimpleUploadedFile("thumbnail.jpg", stream.getvalue(), content_type = "image/jpg")
        image_files = [cover_image_file, thumbnail_image_file]
        data = {
            'title' : 'title',
            'file'  : image_files
        }
        response = client.post('/user/1/covertitle/1',data,format='multipart')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
                         {
                             'message':'Success'
                         })

class IntroductionView(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = "category"
        )
        SubCategory.objects.create(
            id           = 1,
            category_id  = 1,
            name = "sub"
        )
        Creator.objects.create(
            id           = 1,
            nickname     = "phh",
            image_url    = "http://djakj.djka.co",
            introduction = "yeaaaaaaaaaa"
        )
        User.objects.create(
            id   = 1,
            name = "hh",
            creator_id = 1
        )
        Coupon.objects.create(
            id   = 1,
            name = 'coupon'
        )
        Level.objects.create(
            id   = 1,
            name = 'level'
        )
        Product.objects.create(
            id              = 1,
            name            = "product",
            category_id     = 1,
            sub_category_id = 1,
            creator_id      = 1,
            coupon_id       = 1,
            level_id        = 1
        )
        BasicInfo.objects.create(
            id = 1,
            product_id = 1,
            category_id = 1,
            sub_category_id = 1,
            category_detail = 'category_detail',
            level_id = 1
        )
        Introduction.objects.create(
            product_id = 1,
            theme_image_url = '',
            process_image_url = '',
            work_image_url = '',
            theme_description = 'qwe',
            process_description = 'qwe',
            work_description = 'qwe'
        )
        TitleCover.objects.create(
            product_id = 1,
            title = 'title',
            cover_image_url = '',
            thumbnail_image_url = ''
        )

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Creator.objects.all().delete()
        User.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Product.objects.all().delete()
        BasicInfo.objects.all().delete()
        Introduction.objects.all().delete()
        TitleCover.objects.all().delete()

    def test_title_cover(self):
        client = Client()
        self.maxDiff = None
        data = {
            'theme_desc'   : 'qwe',
            'process_desc' : 'qwe',
            'work_desc'    : 'qwe',
            'file'  : ['','','']
        }

        response = client.post('/user/1/introduction/1',data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
            'message':'Success','introduction':{
                    'theme_image_url'     : '',
                    'process_image_url'   : '',
                    'work_image_url'      : '',
                    'theme_description'   : 'qwe',
                    'process_description' : 'qwe',
                    'work_description'    : 'qwe',
                    "category"            : 'category',
                    "sub_category"        : 'sub',
                    "category_detail"     : 'category_detail',
                    "level"               : 'level',
                    "image_url"           : '',
                    "product_id"          : 1,
                    "title"               : 'title',
                    "cover_image_url"     : '',
                    "thumnail_image_url"  : ''
                }
        })
