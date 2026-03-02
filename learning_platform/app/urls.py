from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name="about") ,
    path('course/',views.courses,name="course"),
    path('contact/',views.contact,name="contact"),
    path('add-to-cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name="cart"),
     path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
]

