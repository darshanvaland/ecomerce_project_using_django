from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoryView,name='Category'),
    path('signup/', register,name='register'),
    path('login/', login,name='login'),
    path('logout/', logout,name='logout'),
    path('productall/',productall,name='productall'),
    path('productcatview/<int:id>',productcatwise,name='productcatwise'),
    path('profile/', profile,name='profile'),
    path('feedback/', feedback,name='feedback'),
    path('productdetaiils/<int:id>/', productdetaiils , name='productdetaiils'),
    path('cart/',cart,name='cart'),
    path("delete_cartitem/<int:id>",delete_cartitem,name="cdelete"),
    path('delete_cartall/',delete_cartall,name="delete_cartall"),
    path('shiping/',shiping,name="shiping"),
    path('ordersucces/',ordersucces,name='ordersucces'),
    path('myorder',myorder,name='myorder'),
    path('orderdetialsview/',orderdetialsview,name='orderdetialsview'),
    path('search/',search,name='search'),
    path('razorpayView/',razorpayView,name='razorpayView'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
]   
