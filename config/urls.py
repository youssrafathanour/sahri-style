from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('catalogue/', views.catalogue, name='catalogue'),

    path(
        'produit/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'panier/ajouter/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'panier/',
        views.cart,
        name='cart'
    ),

    path(
        'panier/plus/<int:product_id>/',
        views.increase_cart,
        name='increase_cart'
    ),

    path(
        'panier/moins/<int:product_id>/',
        views.decrease_cart,
        name='decrease_cart'
    ),

    path(
        'panier/supprimer/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
        path(
        'commande/<int:order_id>/statut/',
        views.update_order_status,
        name='update_order_status'
    ),
]