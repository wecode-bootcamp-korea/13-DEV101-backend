from django.db import models

class Creator(models.Model):
    image_url    = models.URLField(max_length=2000)
    nickname     = models.CharField(max_length=45)
    introduction = models.TextField()

    class Meta:
        db_table = 'creators'

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=300, unique=True)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=45)
    image_url    = models.URLField(max_length=2000)
    is_active    = models.BooleanField(default=False)
    creator      = models.OneToOneField(Creator, on_delete=models.SET_NULL, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateField(auto_now=True)

    class Meta:
        db_table = 'users'

