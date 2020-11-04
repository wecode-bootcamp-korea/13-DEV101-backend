from django.db import models

class OrderStatus(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'order_status'

class Order(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete = models.CASCADE)
    status  = models.ForeignKey(OrderStatus, on_delete = models.CASCADE)

    class Meta:
        db_table = 'orders'

