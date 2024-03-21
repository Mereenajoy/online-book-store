from django.contrib import admin
from django.urls import path,include
from .import views
from . views import *

urlpatterns = [
        path('', views.index, name='index'),
        path('signup', views.signup, name='signup'),
        path('login', views.login, name='login'),
        path('demo', views.demo, name='demo'),
        path('admin_home', views.admin_home, name='admin_home'),
        path('admin_add_product',views.admin_add_product,name='admin_add_product'),
        path('admin_view_products', views.admin_view_products, name='admin_view_products'),
        path('product_details/<int:product_id>/', views.product_details, name='product_details'),
        path('view_product',views.view_product,name='view_product'),
        path('homepage',views.homepage,name='homepage'),
        path('admin_update_pro',views.admin_update_pro, name='admin_update_pro'),
        path('admin_delete_product', admin_delete_product, name='admin_delete_product'),
        path('adminviewusers',views.adminviewusers, name='adminviewusers'),
        # path('wishlist',views.wishlist, name='wishlist'),
        # path('add_to_wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
     
        path('admin_add_category' , views.admin_add_category , name='admin_add_category'),
        path('my-cart',views.mycart, name='my-cart'),
        path('search', views.search, name='search'),
        path('contact', views.contact, name='contact'),
        path('profile', views.profile, name='profile'),
        path('updateprofile', views.updateprofile, name='updateprofile'),
 
   path('managecart/<int:id>',views.managecart,name="managecart"),

   path("empty-cart",views.emptycart),
   path('user_orders', views.user_orders, name='user_orders'),

   path("checkout",views.checkout),
   path('add-to-cart/<int:id>',views.addtocart),
   path('admin_view_orders', views.admin_view_orders, name='admin_view_orders'),
   path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    # path('active_user_count', active_user_count, name='active_user_count'),
    # path('orders_placed_count', orders_placed_count, name='orders_placed_count'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    # path('review/<int:book_id>/', views.review, name='review'),
   
     path('productdetails/<int:product_id>/',views.productdetails, name='productdetails'),
     path('t', views.t, name='t'),
    path('toggle-activation/<int:product_id>/', views.toggle_product_activation, name='toggle_product_activation'),

    # path('admin_counts', views.admin_counts, name='admin_counts'),
   
    # path('checkout_session',views.checkout_session,name='checkout_session'),
        

    # Add other paths as needed

        


]