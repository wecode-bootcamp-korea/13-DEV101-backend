from django.urls import path
from user.views  import SignUpView, SignInView, KakaoLoginView, MyPageView, BasicInfoView, CoverTitleView, IntroductionView

urlpatterns = [
    path('/signup',SignUpView.as_view()),
    path('/signin',SignInView.as_view()),
    path('/kakao/login',KakaoLoginView.as_view()),
    path('/me',MyPageView.as_view()),
    path('/basicinfo',BasicInfoView.as_view()),
    path('/covertitle/<int:product_id>',CoverTitleView.as_view()),
    path('/introduction/<int:product_id>',IntroductionView.as_view())
    ]
