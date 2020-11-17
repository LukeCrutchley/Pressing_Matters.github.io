"""Views"""
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User
from .models import auctionList, newItem, watchlist, bids, comments

class createAuction(forms.Form):
    """New Auction form"""
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=64)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    image_link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    startingPrice = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), \
    label="Starting price in £:", max_digits=10, decimal_places=2)
    catagory = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), \
    choices=[('fashion', 'Fashion'), ('toys', 'Toys'), ('electronics', 'Electronics'), \
        ('home', 'Home')])

class make_bid(forms.Form):
    """New Bid"""
    new_bid = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', \
        'decimal_place': '2', 'max_digits':'10'}))

class add_comment(forms.Form):
    new_comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), \
        max_length=500)

def index(request):
    """Home page"""
    return render(request, "auctions/index.html", {
        "listings": auctionList.objects.filter(status="Open")
    })

def catagories(request):
    """Catagories"""
    options = ['Other', 'Fashion', 'Toys', 'Electronics', 'Home']
    return render(request, "auctions/catagories.html", {
        "options": options
    })

def catagory(request, selected_catagory):
    """Selected Catagory"""
    selected_catagory = selected_catagory.lower()
    return render(request, "auctions/index.html", {
        "listings": auctionList.objects.filter(catagory=selected_catagory, status="Open")
    })


@login_required
def my_watchlist(request):
    """My Watchlsit"""
    on_watchlist = watchlist.objects.filter(user=request.user.username).values_list('auction')
    return render(request, "auctions/index.html", {
        "listings": auctionList.objects.filter(id__in=on_watchlist),
        "on_watchlist": on_watchlist
    })

def login_view(request):
    """Login"""
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
    """Logged out"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    """ Register account """
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
    return render(request, "auctions/register.html")


@login_required
def create(request):
    """Create new page"""
    if request.method == "POST":
        Item = newItem()
        Item.title = request.POST.get('title')
        Item.description = request.POST.get('description')
        Item.startingPrice = request.POST.get('startingPrice')
        Item.catagory = request.POST.get('catagory')
        Item.image_link = request.POST.get('image_link')
        n_item = auctionList(title=Item.title, startingPrice=Item.startingPrice, \
        image=Item.image_link, description=Item.description, catagory=Item.catagory, user=request.user.username)
        n_item.save()
        n_bids = bids(current_bid=n_item.startingPrice, auction_item=n_item.id)
        n_bids.save()
        n_comments = comments(auction_item=n_item.id)
        account = request.user.username
        newID = auctionList.objects.latest('id').id
        listing_info = auctionList.objects.get(id=newID)
        bid_info = bids.objects.get(auction_item=newID)
        auction_comments =  comments.objects.filter(auction_item=newID)
        watchlist_message = "Not on Watchlist"
        watchlistedit = "Add to Watchlist"

        return render(request, "auctions/listing.html", {
            "current_bid": bid_info.current_bid,
            "image": listing_info.image,
            "title": listing_info.title,
            "description": listing_info.description,
            "listing_id": newID,
            "watchlist_message": watchlist_message,
            "watchlist_edit": watchlistedit,
            "make_bid": make_bid,
            "status": listing_info.status,
            "owner": True,
            "winner": False,
            "new_comment": add_comment,
            "comments": auction_comments
            })
    return render(request, "auctions/create.html", {
        "listings": auctionList.objects.all(),
        "title": auctionList.title,
        "create": createAuction
    })

@login_required
def listing(request, listing_id):
    """Shows listing"""
    account = request.user.username
    listing_info = auctionList.objects.get(id=listing_id)
    bid_info = bids.objects.get(auction_item=listing_id)
    auction_comments =  comments.objects.filter(auction_item=listing_id)
    if listing_info.status == 'Closed':
        if account == bid_info.user:
            winner = True
    else:        
        winner = False
    if account == listing_info.user:
        owner = True
    else:
        owner = False
    try:
        if watchlist.objects.get(user=request.user.username, auction=listing_id):
            watchlist_message = "On Watchlist"
            watchlistedit = "Remove from Watchlist"
    except:
        watchlist_message = "Not on Watchlist"
        watchlistedit = "Add to Watchlist"
    if request.method == "GET":
        context = {
            "current_bid": bid_info.current_bid,
            "image": listing_info.image,
            "title": listing_info.title,
            "description": listing_info.description,
            "listing_id": listing_id,
            "watchlist_message": watchlist_message,
            "watchlist_edit": watchlistedit,
            "make_bid": make_bid,
            "status": listing_info.status,
            "owner": owner,
            "winner": winner,
            "new_comment": add_comment,
            "comments": auction_comments
        }        
        return render(request, "auctions/listing.html", context)
    elif request.method == "POST" and 'Watchlist' in request.POST:
        try:
            if watchlist.objects.get(user=request.user.username, auction=listing_id):
                watchlist.objects.get(user=request.user.username, auction=listing_id).delete()
                watchlist_message = "Not on Watchlist"
                watchlistedit = "Add to Watchlist"
        except:
            new_watchlist = watchlist(user=request.user.username, auction=listing_id)
            new_watchlist.save()
            watchlist_message = "On Watchlist"
            watchlistedit = "Remove from Watchlist"
        context = {
            "current_bid": bid_info.current_bid,
            "image": listing_info.image,
            "title": listing_info.title,
            "description": listing_info.description,
            "listing_id": listing_id,
            "watchlist_message": watchlist_message,
            "watchlist_edit": watchlistedit,
            "make_bid": make_bid,
            "status": listing_info.status,
            "owner": owner,
            "winner": winner,
            "new_comment": add_comment,
            "comments": auction_comments
        }
        return render(request, "auctions/listing.html", context)
    elif request.method == "POST" and 'bid' in request.POST:
        n_bid = bids()
        n_bid.current_bid = Decimal(request.POST.get('new_bid'))
        if n_bid.current_bid > bid_info.current_bid:
            bid = bids(user=request.user.username, current_bid=n_bid.current_bid,\
                 auction_item=listing_id, pk=listing_id)
            bid.save(force_update=True)
            context = {
                "current_bid": n_bid.current_bid,
                "image": listing_info.image,
                "title": listing_info.title,
                "description": listing_info.description,
                "listing_id": listing_id,
                "watchlist_message": watchlist_message,
                "watchlist_edit": watchlistedit,
                "make_bid": make_bid,
                "status": listing_info.status,
                "owner": owner,
                "winner": winner,
                "new_comment": add_comment,
                "comments": auction_comments
            }
            return render(request, "auctions/listing.html", context)
        return render(request, "auctions/error.html")
    elif request.method == "POST" and 'endauction' in request.POST:
        auctionList.objects.filter(id=listing_id).update(status='Closed', winner=bid_info.user)
        if listing_info.status == 'Closed':
            if account == bid_info.user:
                winner = True
        else:
            winner = False
        if account == listing_info.user:
            owner = True
        else:
            owner = False
        context = {
            "current_bid": bid_info.current_bid,
            "image": listing_info.image,
            "title": listing_info.title,
            "description": listing_info.description,
            "listing_id": listing_id,
            "watchlist_message": watchlist_message,
            "watchlist_edit": watchlistedit,
            "make_bid": make_bid,
            "status": listing_info.status,
            "owner": owner,
            "winner": winner,
            "new_comment": add_comment,
            "comments":  auction_comments
        }
        return render(request, "auctions/listing.html", context)
    elif request.method == "POST" and 'comment' in request.POST:
        newComment = request.POST.get('new_comment')
        n_comment = comments(user=request.user.username, comment=newComment, auction_item=listing_id)
        n_comment.save()
        context = {
            "current_bid": bid_info.current_bid,
            "image": listing_info.image,
            "title": listing_info.title,
            "description": listing_info.description,
            "listing_id": listing_id,
            "watchlist_message": watchlist_message,
            "watchlist_edit": watchlistedit,
            "make_bid": make_bid,
            "status": listing_info.status,
            "owner": owner,
            "winner": winner,
            "new_comment": add_comment,
            "comments":  auction_comments
        }
        return render(request, "auctions/listing.html", context)

    return render(request, "auctions/index.html", {
        "listings": auctionList.objects.all(),
        "title": auctionList.title
    })
