from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:product_slug>/', views.product_info, name='product_info'),
    path('search/<slug:category_slug>/', views.list_category, name='list_category'),

]