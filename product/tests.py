import json

from datetime  import datetime
from django.test import TestCase, Client, TransactionTestCase

from .models import Product, Category, SubCategory, Coupon, Level, BasicInfo, Introduction, Image, Post, Comment, ProductLike
from user.models import Creator, User

class DetailTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        BasicInfo.objects.create(
            id=1,
            product_id=1,
            category_id=1,
            sub_category_id=1,
            category_detail='hihi',
            level_id=1
        )
        Introduction.objects.create(
            id=1,
            product_id=1,
            theme_image_url='www.url.com',
            process_image_url='www.url.com',
            work_image_url='www.url.com',
            theme_description='haha',
            process_description='haha',
            work_description='haha'
        )
        User.objects.create(
            id=1,
            email='email@emai.com',
            password='password',
            phone_number='01012345678',
            image_url='www.url.com',
            is_active=True,
            creator_id=1,
            cheer_point=10
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        BasicInfo.objects.all().delete()
        Introduction.objects.all().delete()
        User.objects.all().delete()

    def test_product_get_success(self):
        client=Client()
        self.maxDiff = None
        response=client.get('/product/1')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {   "product_id":1,
                "header_images": [],
                "detail_aside": {
                    "category": "sub_category1",
                    "creator_name": "nickname",
                    "title": "class1",
                    "price": "300000.00",
                    "discount": "0.55",
                    "heart": 0
                },
                "detail": {
                    "class_info": {
                        "chapter": 20,
                        "sub_chapter": 33,
                        "is_subtitled": True,
                        "level": "level1",
                        "class_detail": "hihi",
                        "to_learn": [{
                    "description": "haha",
                    "image_url": "www.url.com"
                },
                {
                    "description": "haha",
                    "image_url": "www.url.com"
                },
                {
                    "description": "haha",
                    "image_url": "www.url.com"
                }],
                    }
                },
                "reviews": {
                    "review_length": 0,
                    "satis": 0,
                    "content": [],
                    "comment_list": []
                },
                "notice": [],
                "community": []
            }
            
        )

    def test_product_get_fail(self):
        client=Client()
        response=client.get('/product/9999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'PRODUCT DOES NOT EXIST'
            }
        )

    def test_product_get_not_found(self):
        client=Client()
        response=client.get('/product?id=1')
        
        self.assertEqual(response.status_code,404)

class CommentTest(TransactionTestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        User.objects.create(
            id=1,
            name='name',
            email='email@emai.com',
            password='password',
            phone_number='01012345678',
            image_url='www.url.com',
            is_active=True,
            creator_id=1,
            cheer_point=10
        )
        Post.objects.create(
            id=1,
            product_id=1,
            user_id=1,
            content='haha',
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        User.objects.all().delete()

    def test_comment_post_success(self):
        client=Client()
        self.maxDiff = None
        comment={
            'user_id':'1',
            'content':'hi',
        }
        response=client.post('/product/1/post/1', comment)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                'post_id':1,
                'comment_id':2,
                'user':'name',
                'user_image_url':'www.url.com',
                'created_at':'',
                'content':'hi',
                'comment_image_url':None
            }
        )

    def test_comment_post_fail(self):
        client=Client()
        comment={
            'user_id':'1',
            'content':'hi',
        }
        response=client.post('/product/1/post/9999', comment)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'POST DOES NOT EXIST'
            }
        )

    def test_comment_post_key_error(self):
        client=Client()
        comment={
            'user_id':'1',
            'contents':'hi',
        }
        response=client.post('/product/1/post/1', comment)        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'KEY ERROR'
            }
        )

class ProductLikeTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        User.objects.create(
            id=1,
            name='name',
            email='email@email.com',
            password='password',
            phone_number='01012345678',
            image_url='www.url.com',
            is_active=True,
            creator_id=1,
            cheer_point=10
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        User.objects.all().delete()
        ProductLike.objects.all().delete

    def test_product_like_post_success(self):
        client=Client()
        self.maxDiff = None
        response=client.post('/product/1/like')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {'like_count':1}
        )

    def test_product_like_post_not_found(self):
        client=Client()
        response=client.post('/product/999/like')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {'message': 'NO_PRODUCT'}
        )

class DetailTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        BasicInfo.objects.create(
            id=1,
            product_id=1,
            category_id=1,
            sub_category_id=1,
            category_detail='hihi',
            level_id=1
        )
        Introduction.objects.create(
            id=1,
            product_id=1,
            theme_image_url='www.url.com',
            process_image_url='www.url.com',
            work_image_url='www.url.com',
            theme_description='haha',
            process_description='haha',
            work_description='haha'
        )
        User.objects.create(
            id=1,
            email='email@emai.com',
            password='password',
            phone_number='01012345678',
            image_url='www.url.com',
            is_active=True,
            creator_id=1,
            cheer_point=10
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        BasicInfo.objects.all().delete()
        Introduction.objects.all().delete()
        User.objects.all().delete()

    def test_product_get_success(self):
        client=Client()
        self.maxDiff = None
        response=client.get('/product/1')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {   "product_id":1,
                "header_images": [],
                "detail_aside": {
                    "category": "sub_category1",
                    "creator_name": "nickname",
                    "title": "class1",
                    "price": "300000.00",
                    "discount": "0.55",
                    "heart": 0
                },
                "detail": {
                    "class_info": {
                        "chapter": 20,
                        "sub_chapter": 33,
                        "is_subtitled": True,
                        "level": "level1",
                        "class_detail": "hihi",
                        "to_learn": [{
                    "description": "haha",
                    "image_url": "www.url.com"
                },
                {
                    "description": "haha",
                    "image_url": "www.url.com"
                },
                {
                    "description": "haha",
                    "image_url": "www.url.com"
                }],
                    }
                },
                "reviews": {
                    "review_length": 0,
                    "satis": 0,
                    "content": [],
                    "comment_list": []
                },
                "notice": [],
                "community": []
            }
            
        )

    def test_product_get_fail(self):
        client=Client()
        response=client.get('/product/9999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'PRODUCT DOES NOT EXIST'
            }
        )

    def test_product_get_not_found(self):
        client=Client()
        response=client.get('/product?id=1')
        
        self.assertEqual(response.status_code,404)

class CommentTest(TransactionTestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        User.objects.create(
            id=1,
            name='name',
            email='email@emai.com',
            password='password',
            phone_number='01012345678',
            image_url='www.url.com',
            is_active=True,
            creator_id=1,
            cheer_point=10
        )
        Post.objects.create(
            id=1,
            product_id=1,
            user_id=1,
            content='haha',
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        User.objects.all().delete()

    def test_comment_post_success(self):
        client=Client()
        self.maxDiff = None
        comment={
            'user_id':'1',
            'content':'hi',
        }
        response=client.post('/product/1/post/1', comment)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                'post_id':1,
                'comment_id':2,
                'user':'name',
                'user_image_url':'www.url.com',
                'created_at':'',
                'content':'hi',
                'comment_image_url':None
            }
        )

    def test_comment_post_fail(self):
        client=Client()
        comment={
            'user_id':'1',
            'content':'hi',
        }
        response=client.post('/product/1/post/9999', comment)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'POST DOES NOT EXIST'
            }
        )

    def test_comment_post_key_error(self):
        client=Client()
        comment={
            'user_id':'1',
            'contents':'hi',
        }
        response=client.post('/product/1/post/1', comment)        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'KEY ERROR'
            }
        )

class ProductListTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        BasicInfo.objects.create(
            id=1,
            product_id=1,
            category_id=1,
            sub_category_id=1,
            category_detail='hihi',
            level_id=1
        )
        Introduction.objects.create(
            id=1,
            product_id=1,
            theme_image_url='www.url.com',
            process_image_url='www.url.com',
            work_image_url='www.url.com',
            theme_description='haha',
            process_description='haha',
            work_description='haha'
        )
        Image.objects.create(
            id=1,
            product_id=1,
            image_url='www.url.com'
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        BasicInfo.objects.all().delete()
        Introduction.objects.all().delete()

    def test_product_list_get_success(self):
        client=Client()
        self.maxDiff = None
        response=client.get('/products')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                "top_10_data": [
                    {
                        "product_id": 1,
                        "image_url": "www.url.com",
                        "sub_category": "sub_category1",
                        "mentor": "nickname",
                        "title": "class1",
                        "like_count": 0,
                        "thumbs_up": 0,
                        "price": "300000.00",
                        "discount": "0.55",
                        "coupon": "coupon1"
                    }
                ],
                "planned_data": [],
                "updated_data": [
                    {
                        "product_id": 1,
                        "image_url": "www.url.com",
                        "sub_category": "sub_category1",
                        "mentor": "nickname",
                        "title": "class1",
                        "like_count": 0,
                        "thumbs_up": 0,
                        "coupon": "coupon1",
                        "updated_at": str(datetime.now())
                    }
                ]
            }
            
        )

    def test_product_list_get_not_found(self):
        client=Client()
        response=client.get('/product')
        self.assertEqual(response.status_code,404)

class ProductSearchTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id=1,
            name='category1'
        )
        SubCategory.objects.create(
            id=1,
            category_id=1,
            name='sub_category1'
        )
        Coupon.objects.create(
            id=1,
            name='coupon1'
        )
        Level.objects.create(
            id=1,
            name='level1'
        )
        Creator.objects.create(
            id=1,
            image_url='www.url.com',
            nickname='nickname',
            introduction='hihihi'
        )
        Product.objects.create(
            id=1,
            name='class1',
            category_id=1,
            sub_category_id=1,
            creator_id=1,
            level_id=1,
            coupon_id=1,
            price=300000,
            discount=0.55,
            chapter=20,
            chapter_detail=33,
            subtitle_flag=True,
            is_checked=True,
            is_open=True
        )
        BasicInfo.objects.create(
            id=1,
            product_id=1,
            category_id=1,
            sub_category_id=1,
            category_detail='hihi',
            level_id=1
        )
        Introduction.objects.create(
            id=1,
            product_id=1,
            theme_image_url='www.url.com',
            process_image_url='www.url.com',
            work_image_url='www.url.com',
            theme_description='haha',
            process_description='haha',
            work_description='haha'
        )
        Image.objects.create(
            id=1,
            product_id=1,
            image_url='www.url.com'
        )
    
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        BasicInfo.objects.all().delete()
        Introduction.objects.all().delete()

    def test_product_search_get_success(self):
        client=Client()
        self.maxDiff = None
        response=client.get('/search?query=class1')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
            "data": [
                {
                    "product_id": 1,
                    "image_url": "www.url.com",
                    "sub_category": "sub_category1",
                    "mentor": "nickname",
                    "title": "class1",
                    "like_count": 0,
                    "thumbs_up": 0,
                    "price": "300000.00",
                    "discount": "0.55",
                    "coupon": "coupon1"
                }
            ]
        }
            
        )
    def test_product_search_get_fail(self):
        client=Client()
        response=client.get('/search?sort=4')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'WRONG SORTING'
            }
        )

    def test_product_search_get_not_found(self):
        client=Client()
        response=client.get('/search/class1')
        self.assertEqual(response.status_code,404)