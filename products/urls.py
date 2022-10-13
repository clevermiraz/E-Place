from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<str:pk>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("create/", views.create_product, name="create_product"),
    path('update/<str:pk>/<slug:slug>/', views.update_product, name='update_product'),
    path('delete/<str:pk>/<slug:slug>/', views.delete_product, name='delete_product'),
]
