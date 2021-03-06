from django.urls import path
from . import views          
urlpatterns = [
    path('',views.about),
    path('registration', views.registration),
    path('registerdriver', views.registerdriver),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('drivers',views.drivers),
    path('contact',views.contact),
    path('userorder',views.userorder),
    path('driverorder',views.driverorder),
    path('editacc/<user_id>', views.edit_account),
    path('editaccdriver/<driver_id>', views.edit_accountdriver),
    path('update/<user_id>', views.submit),
    path('updatedriver/<driver_id>', views.submitdriver),
    path('remove/<order_id>', views.removeorder) ,
    path('done/<order_id>', views.doneorder) ,
    path('order', views.post_order),
    path('order/<order_id>', views.addorder),
]