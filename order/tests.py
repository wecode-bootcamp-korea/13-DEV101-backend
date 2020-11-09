import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.http import HttpResponse

from product.models import Product, Category, SubCategory, Coupon, Level, BasicInfo, Introduction, Image, Post, Comment
from user.models import Creator, User
from .models import OrderStatus, PaymentType, SmsAuth

class OrderTest(TestCase):
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
        Image.objects.create(
            id=1,
            product_id=1,
            image_url='www.url.com'
        )
        User.objects.create(
            id=1,
            name='name',
            email='email@email.com',
            password='12345678',
            phone_number='01012345678',
            image_url='www.url.com'
        )
        OrderStatus.objects.create(
            id=1,
            name='status'
        )
        PaymentType.objects.create(
            id=1,
            name='type1'
        )
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Coupon.objects.all().delete()
        Level.objects.all().delete()
        Creator.objects.all().delete()
        Image.objects.all().delete()
        User.objects.all().delete()
        OrderStatus.objects.all().delete()
        PaymentType.objects.all().delete()

    def test_order_success(self):
        client=Client()
        response=client.get('/order/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'creator':'nickname',
                'class_image':'www.url.com',
                'username':'name',
                'phone_number':'01012345678',
                'price':'300000.00',
                'discount':165000,
                'total':135000
            }
        )

    def test_order_get_fail(self):
        client=Client()
        response=client.get('/order/9999')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'NO_PRODUCT'
            }
        )

    def test_order_not_found(self):
        client=Client()
        response=client.get('order/?id=1')
        self.assertEqual(response.status_code,404)

    def test_order_post_success(self):
        client=Client()
        order={
            'username':'name',
            'phone_number':'01012345678',
            'price':'300000'
        }
        response=client.post('/order/1', json.dumps(order), content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_order_post_not_found(self):
        client=Client()
        order={
            'username':'name',
            'phone_number':'01012345678',
            'price':'300000'
        }
        response=client.post('/order/9999', json.dumps(order), content_type='application/json')
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),
            {
                'message':'NO_PRODUCT'
            }
        )

    def test_order_post_invalid_keys(self):
        client=Client()
        order={
            'user':'name',
            'phone_number':'01012345678',
            'price':'300000'
        }
        response=client.post('/order/1', json.dumps(order), content_type='application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )

class SmsTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            name='name',
            email='email@email.com',
            password='12345678',
            phone_number='01012345678',
            image_url='www.url.com'
        )
        SmsAuth.objects.create(
            id=1,
            user_id=1,
            phone_number='+821072901284',
            auth_number='1111'
        )

    def tearDown(self):
        User.objects.all().delete()
        SmsAuth.objects.all().delete()
    
    @patch('order.views.SmsAuthView.send_sms')
    def test_sms_post_success(self, mock_post):
        mock_post.post=MagicMock(return_value=HttpResponse(status=202))
        client=Client()
        user_info={'phone_number':'+821072901284'}
        user_id=1
        
        response=client.post('/order/smsauth', json.dumps(user_info), content_type='application/json')
        self.assertEqual(response.status_code,200)

    @patch('order.views.SmsAuthView.send_sms')
    def test_sms_post_invalid_keys(self, mock_post):
        mock_post.post=MagicMock(return_value=HttpResponse(status=202))
        client=Client()
        user_info={'phone':'+821072901284'}
        user_id=1
        
        response=client.post('/order/smsauth', json.dumps(user_info), content_type='application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )

class SmsCheckTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            name='name',
            email='email@email.com',
            password='12345678',
            phone_number='01012345678',
            image_url='www.url.com'
        )
        SmsAuth.objects.create(
            id=1,
            user_id=1,
            phone_number='+821012345678',
            auth_number=1111
        )
    
    def tearDown(self):
        User.objects.all().delete()
        SmsAuth.objects.all().delete()
    
    def test_sms_check_success(self):
        client=Client()
        user_input={
            'phone_number':'01012345678',
            'auth_number':'1111'
        }
        response=client.post('/order/smsauthcheck', json.dumps(user_input), content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_sms_check_fail(self):
        client=Client()
        user_input={
            'phone_number':'01012345678',
            'auth_number':'1234'
        }
        response=client.post('/order/smsauthcheck', json.dumps(user_input), content_type='application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'CHECK_VERIFICATION_NUMBER'
            }
        )

    def test_sms_check_invalid_keys(self):
        client=Client()
        user_input={
            'phone':'01012345678',
            'auth':'1234'
        }
        response=client.post('/order/smsauthcheck', json.dumps(user_input), content_type='application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'KEY_ERROR'
            }
        )