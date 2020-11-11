from django.urls import path, include
from .views import DetailView, CommentView, ProductLikeView, ProductsView, SearchView, PackageView, CheerView

urlpatterns = [
    path('product/<int:product_id>', DetailView.as_view()),
    path('product/<int:product_id>/post/<int:post_id>', CommentView.as_view()),
    path('products', ProductsView.as_view()),
    path('search',SearchView.as_view()),
    path('product/<int:product_id>/like', ProductLikeView.as_view()),
    path('product/<int:product_id>/packages', PackageView.as_view()),
    path('product/<int:product_id>/cheer', CheerView.as_view()),
]
