import json
import boto3
import datetime

from django.views import View
from django.http import JsonResponse
from django.core.cache import cache
from django.db         import IntegrityError

from .models import Product, Post, Comment
from user.models import User
from my_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

POST_LIMIT   = 8
REVIEW_LIMIT = 2

class DetailView(View):
    def get(self,request, product_id):
        try:
            product      = cache.get_or_set('product', Product.objects.select_related(
                'category', 
                'sub_category', 
                'creator', 
                'level', 
                'coupon'
                ).prefetch_related(
                    'image_set',
                    'tags', 
                    'review_set', 
                    'post_set',
                    'productlike_set', 
                    'introduction_set', 
                    'basicinfo_set'
                    ).get(id=product_id)
            )
            
            data={
                'product_id'   : product.id,
                'header_images':[
                    {
                        "src": image.image_url
                    } for image in product.image_set.all()],

                'detail_aside':{
                    'category'    : product.sub_category.name,
                    'creator_name': product.creator.nickname,
                    'title'       : product.name,
                    'price'       : product.price,
                    'discount'    : product.discount,
                    'heart'       : product.productlike_set.count()
                },

                'detail':{
                    'class_info':{
                        'chapter'     : product.chapter,
                        'sub_chapter' : product.chapter_detail,
                        'is_subtitled': product.subtitle_flag,
                        'level'       : product.level.name,
                        'class_detail': product.basicinfo_set.first().category_detail,
                        'to_learn'    : [
                            {'description': product.introduction_set.first().theme_description,
                            'image_url'  : product.introduction_set.first().theme_image_url},
                            {'description': product.introduction_set.first().process_description,
                            'image_url'  : product.introduction_set.first().process_image_url},
                            {'description': product.introduction_set.first().work_description,
                            'image_url'  : product.introduction_set.first().work_image_url}
                            ]
                        }
                    },
                
                'reviews':{
                    'review_length': product.review_set.all().count(),
                    'satis'        : product.review_set.filter(good_bad=True).count()/product.review_set.all().count()*100 if product.review_set.all().count()!=0 else 0,
                    'content':[
                        {
                            'description':post.content
                        } for post in product.post_set.all()[:POST_LIMIT]],
                    'comment_list':[{
                        'profile_image': review.user.image_url,
                        'nickname'     : review.user.name,
                        'date'         : review.created_at,
                        'description'  : review.content
                    } for review in product.review_set.all()[:REVIEW_LIMIT]]
                },

                'notice':[
                    {
                        'profile_image': product.creator.image_url,
                        'nickname'     : product.creator.nickname,
                        'date'         : post.created_at,
                        'description'  : post.content
                    }
                for post in product.post_set.filter(user_id=User.objects.get(creator_id=product.creator_id))],

                'community':[
                    {   
                        'post_id'      : post.id,
                        'profile_image': post.user.image_url,
                        'nickname'     : post.user.name,
                        'date'         : post.created_at,
                        'description'  : post.content,
                        'comments': [{
                            'comment_id'   : comment.id,
                            'profile_image': comment.user.image_url,
                            'nickname'     : comment.user.name,
                            'date'         : comment.created_at,
                            'description'  : comment.content,
                            'image_url'    : comment.image_url
                        } for comment in post.comment_set.all()]
                    }
                for post in product.post_set.all() if post.user_id!=User.objects.get(creator_id=product.creator_id).id]
            }
            
            return JsonResponse(data, status=200)
            return JsonResponse({'message': 'PAGE DOES NOT EXIST'}, status=404)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT DOES NOT EXIST'}, status=400)

class CommentView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    def post(self, request, product_id, post_id):
        try:
            user_id=request.POST['user_id']
            content=request.POST['content']
            file=request.FILES.getlist('file')
            if file:
                filename=str(datetime.datetime.now())+User.objects.get(id=user_id).name+file.name
                
                self.s3_client.upload_fileobj(
                    file,
                    "class-dev101",
                    filename,
                    ExtraArgs={
                        "ContentType": file.content_type
                    }
                )
                file_url=f"https://s3.ap-northeast-2.amazonaws.com/class-dev101/{filename}"
            else:
                file_url=None

            new_comment=Comment.objects.create(
                post_id=post_id,
                user_id=user_id,
                content=content,
                image_url=file_url
            )
            cache.delete('product')
            data={
                'post_id':new_comment.post.id,
                'comment_id':new_comment.id,
                'user':new_comment.user.name,
                'user_image_url':new_comment.user.image_url,
                'created_at':new_comment.created_at,
                'content':new_comment.content,
                'comment_image_url':new_comment.image_url
            }
            
            return JsonResponse(data, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message':'POST DOES NOT EXIST'}, status=400)

        

