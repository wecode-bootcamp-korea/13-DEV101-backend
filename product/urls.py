from django.urls import path, include
from .views import DetailView, CommentView

urlpatterns = [
    path('product/<int:product_id>', DetailView.as_view()),
    path('product/<int:product_id>/post/<int:post_id>', CommentView.as_view()),
]