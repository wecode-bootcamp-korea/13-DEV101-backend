from django.urls import path
from .views import OrderView, SmsAuthView, SmsAuthCheckView

urlpatterns = [
    path('/<int:product_id>', OrderView.as_view()),
    path('/smsauth', SmsAuthView.as_view()),
    path('/smsauthcheck', SmsAuthCheckView.as_view()),
]