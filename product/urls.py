from django.urls import path, include
from .views import DetailView, CommentView, ProductsView, SearchView

urlpatterns = [
    path('product/<int:product_id>', DetailView.as_view()),
    path('product/<int:product_id>/post/<int:post_id>', CommentView.as_view()),
    path('products', ProductsView.as_view()),
    path('search',SearchView.as_view()),
]