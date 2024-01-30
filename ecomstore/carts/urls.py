from django.urls import path, include
from carts.views import show_cart

urlpatterns = [
    path("", view=show_cart, name="show_cart"),
    path("cart/", view=show_cart, name="show_cart"),
]