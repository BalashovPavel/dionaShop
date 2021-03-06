from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('changefromcart/<int:id>', views.changefromcart, name='changefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
]
