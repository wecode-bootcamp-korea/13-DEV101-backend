from django.db import models

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=45)
    
    class Meta:
        db_table = "social_platforms"

class Creator(models.Model):
    image_url    = models.URLField(max_length=2000)
    nickname     = models.CharField(max_length=45)
    introduction = models.TextField()

    class Meta:
        db_table = 'creators'

class User(models.Model):
    name            = models.CharField(max_length=45)
    email           = models.EmailField(max_length=300, unique=True)
    password        = models.CharField(max_length=300, null=True)
    phone_number    = models.CharField(max_length=45, null=True)
    image_url       = models.URLField(max_length=2000, null=True)
    is_active       = models.BooleanField(default=False)
    creator         = models.OneToOneField(Creator, on_delete=models.SET_NULL, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    cheer_point     = models.PositiveIntegerField(default=10)
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, null=True)
    social_login_id = models.CharField(max_length=200, null=True)
    coupon          = models.ManyToManyField('product.Coupon', through='user.UserCoupon', related_name='user')

    class Meta:
        db_table = 'users'

class UserCoupon(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey('product.Coupon', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_coupons'