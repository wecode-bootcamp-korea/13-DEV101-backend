from django.db import models

class OrderStatus(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'order_status'

class PaymentType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'payment_types'

class Order(models.Model):
    product      = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user         = models.ForeignKey('user.User', on_delete = models.CASCADE)
    status       = models.ForeignKey(OrderStatus, on_delete = models.CASCADE)
    name         = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20)
    total_price  = models.DecimalField(max_digits=16, decimal_places=2)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class SmsAuth(models.Model):
    user=models.ForeignKey('user.User', on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=20)
    auth_number=models.IntegerField()

    class Meta:
        db_table = 'sms_auths'