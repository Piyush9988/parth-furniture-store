from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),

    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('sofas/', views.sofa_products, name='sofas'),
    path('chairs/', views.chair_products, name='chairs'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # NEW URLS 👇
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),

    path('contact/', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)