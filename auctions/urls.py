from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("create", views.create, name="create"),
    path("catagories", views.catagories, name="catagories"),
    path("catagory/<str:selected_catagory>", views.catagory, name="catagory"),
    path("<str:listing_id>", views.listing, name="listing")
]
