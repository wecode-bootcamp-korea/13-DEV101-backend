from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=300)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=45)
    is_active    = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

class Creator(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    image        = models.CharField(max_length=300)
    nickname     = models.CharField(max_length=45)
    introduction = models.TextField()

    class Meta:
        db_table = 'creators'
