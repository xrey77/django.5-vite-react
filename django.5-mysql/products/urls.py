from django.urls import path
from .views import ProductList
from .views import ProductSearch

urlpatterns = [
    path('products/list/<int:page>', ProductList.as_view(), name="productlist"),
    path('products/search/<int:page>/<str:key>', ProductSearch.as_view(), name="productlist"),
]