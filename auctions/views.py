from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import User, ListItem, WatchlistItem, Comment, Bid


def index(request):
    title = "Active Listings"
    itens = ListItem.objects.filter(status=True)
    return render(request,"auctions/index.html",{
        "texttitle": title,
        "listitem": itens
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
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
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
            user.first_name = first_name
            user.last_name = last_name
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
    if not request.user.is_authenticated:
        return redirect('login') 
    try:  
        item = ListItem.objects.get(pk=id)

        watchlist_items = WatchlistItem.objects.filter(user=request.user)

        product_ids = watchlist_items.values_list('item', flat=True)

        user_watchlist = ListItem.objects.filter(id__in=product_ids)

        comments = Comment.objects.filter(idItem=item)
    except ListItem.DoesNotExist:
        raise Http404("Error 404!!! Not Found")
    
    return render(request,"auctions/listings.html",{
        "item": item,
        'user_watchlist': user_watchlist,
        'comments': comments
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
        raise Http404("Error 404!!! Not Found")
    return render(request,"auctions/categorie.html",{
        "listitem": itens,
        "categorie": categorie
    })


def watchlist(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    try:
        watchlist_items = WatchlistItem.objects.filter(user=request.user)

        product_ids = watchlist_items.values_list('item', flat=True)

        itens = ListItem.objects.filter(id__in=product_ids)
    except WatchlistItem.DoesNotExist:
        raise Http404("Error 404!!! Not Found")
   
    return render(request, "auctions/index.html",{
        "texttitle": "Watchlist",
        "listitem": itens
    })

def add(request, id_item):

    if not request.user.is_authenticated:
        return redirect('login') 

    try:
        item = get_object_or_404(ListItem, id=id_item)
        find_item = WatchlistItem.objects.filter(user=request.user, item=item).first()
        if find_item:
            find_item.delete()
        else:
            WatchlistItem.objects.create(user=request.user, item=item)
    except ListItem.DoesNotExist:
        raise Http404("Error 404!!! Not Found")
   
    return redirect('watchlist')

def place_bid(request, id):

    item = ListItem.objects.get(id=id)

    watchlist_items = WatchlistItem.objects.filter(user=request.user)

    product_ids = watchlist_items.values_list('item', flat=True)

    user_watchlist = ListItem.objects.filter(id__in=product_ids)

    comments = Comment.objects.filter(idItem=item)

    if request.method == "POST":
        
        bid_value = float(request.POST["bid_value"])

        if bid_value >= item.price:
            
            bid = Bid(
                user=request.user,
                idItem = item,
                bids_amount = bid_value)
            bid.save()

            return render(request, 'auctions/listings.html', {
                "item":item,
                'user_watchlist': user_watchlist,
                'comments': comments
                })
        else:
            return render(request, "auctions/listings.html", {
                "item":item,
                "message": "Invalid bid amount, as it is lower than the current bid.",
                'user_watchlist': user_watchlist,
                'comments': comments
            })

def cretelisting(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]
        photo_url = request.POST["photo_url"]
        type_item = request.POST["type_item"]

        
        if not name or not description or not price or not photo_url or not type_item:
            return render(request, "auctions/createlisting.html", {
                "message": "ERROR - All fields are mandatory."
            })
        else:
            listitem = ListItem(
                name=name,
                description=description,
                price=price,
                data_post= timezone.now(),
                photo_url=photo_url,
                type_item=type_item,
                user=request.user
            )
            listitem.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html")

def add_comment(request, id):
    if request.method == "POST":
        text = request.POST["text"]
        if not text:
            return render(request, "auctions/listings.html", {
                "message": "ERROR - Not Comment"
            })
        else:
            item = get_object_or_404(ListItem, pk=id)
            comment = Comment(
                user=request.user,
                text = text,
                idItem = item
            )
            comment.save()
            return redirect('listing', id=id)
    else:
        return redirect('listing', id=id)

def bids_visualization(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    try:
        my_items = ListItem.objects.filter(user=request.user)

        product_ids = my_items.values_list('id', flat=True)

        itens = ListItem.objects.filter(id__in=product_ids)

        bids = Bid.objects.filter(idItem__in=product_ids)

        list_bids = bids.values_list('idItem', flat=True)

    except Bid.DoesNotExist:
        raise Http404("Error 404!!! Not Found")
   
    return render(request, "auctions/bidsvisualization.html",{
        "texttitle": "Bids for my items",
        "listitem": itens,
        "bids": bids,
        "list_bids":list_bids
    })

def close_auction(request, id):

    item = ListItem.objects.get(id=id)

    watchlist_items = WatchlistItem.objects.filter(user=request.user)

    product_ids = watchlist_items.values_list('item', flat=True)

    user_watchlist = ListItem.objects.filter(id__in=product_ids)

    comments = Comment.objects.filter(idItem=item)
    
    if request.method == "POST":
        if(item.status == True):
            item.status = False
            item.save()
        else:
            item.status = True
            item.save()
    
    return render(request, "auctions/listings.html", {
                "item":item,
                'user_watchlist': user_watchlist,
                'comments': comments
            })
    
    