from django.urls import path
from user.views  import SignUpView, SignInView, KakaoLoginView, MyPageView

urlpatterns = [
    path('/signup',SignUpView.as_view()),
    path('/signin',SignInView.as_view()),
    path('/kakao/login',KakaoLoginView.as_view()),
    path('/me',MyPageView.as_view())
]
