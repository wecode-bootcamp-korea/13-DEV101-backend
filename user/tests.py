import json
import bcrypt

from django.test    import TestCase,Client

from user.models    import User,Creator
from product.models import Product,ProductLike,Image,Category,SubCategory,Level,Coupon,Watched

client = Client()

class MyPageTest(TestCase):
    def setUp(self):
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
        Product.objects.create(
             id              = 2,
             name            = 'content2',
             category_id     = 1,
             sub_category_id = 1,
             price           = 100000,
             discount        = 0.32,
             chapter         = 1,
             chapter_detail   = 1,
             subtitle_flag   = False,
             is_checked      = True,
             is_open         = False,
             level_id        = 1
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
                    "coupon_num": 15,
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
