from django.urls import path
from .views import update_cart,cart_home
urlpatterns = [
    path("update/", update_cart, name="update"),
    path("list/", cart_home, name="list"),
]