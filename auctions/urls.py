from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("bid/<int:id>", views.place_bid, name="bid"),
    path("add/<int:id_item>", views.add, name="add"),
    path("close/<int:id>", views.close_auction, name="close_auction"),
    path("create", views.cretelisting, name="createlisting"),
    path("bids", views.bids_visualization, name="bids"),
    path("comment/<int:id>", views.add_comment, name="comment"),
    path("categories/<str:categorie>", views.categorie_page, name="categorie")
]
