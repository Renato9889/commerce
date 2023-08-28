from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, ListItem, WatchlistItem


def index(request):
    title = "Active Listings"
    return render(request,"auctions/index.html",{
        "texttitle": title,
        "listitem":ListItem.objects.all()
    })


def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, id):
    item = ListItem.objects.get(pk=id)
    return render(request,"auctions/listings.html",{
        "item": item
    })


def categories(request):
    categories = ["Electronics","Fashion","Books", "Industrial Equipment","Collectibles and Art","Sports","Health and Beauty", "Geek", "Home and Garden"]
    imgs = ["../../static/auctions/eletronics.jpeg","../../static/auctions/fashion.jpeg","../../static/auctions/books.jpeg",
            "../../static/auctions/industrialequipment.jpeg","../../static/auctions/Collectibles.jpeg","../../static/auctions/sports.jpeg",
            "../../static/auctions/Health.jpeg","../../static/auctions/geek.jpg","../../static/auctions/home.jpeg"]
    combined_data = list(zip(categories, imgs))
    return render(request,"auctions/listingcategories.html",{
        'combined_data':combined_data
    })

def categorie_page(request, categorie):
    try:
        itens = ListItem.objects.filter(type_item=categorie)
    except ListItem.DoesNotExist:
        raise Http404("Item não encontrado")
    return render(request,"auctions/categorie.html",{
        "listitem": itens,
        "categorie": categorie
    })


def watchlist(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    watchlist_items = WatchlistItem.objects.filter(user=request.user)


    title = "Watchlist"
    return render(request, "auctions/index.html",{
        "texttitle": title,
        "listitem" : watchlist_items 
    })