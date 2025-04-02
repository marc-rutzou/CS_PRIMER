from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
import re


from .models import User, Listing, Bid, Comment, Category, IsCategory, Watchlist


def index(request):
    active_listings = Listing.objects.filter(status=True).order_by('time')
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

def categories(request):
    categories = Category.objects.all()
    active_listings_category = None

    if request.method == "POST": 
        chosen_cat = request.POST.get("category")
        active_listings_category = [x.listing_id for x in IsCategory.objects.filter(category_id=chosen_cat)]

    
    return render(request, "auctions/categories.html", {
            "active_listings_category": active_listings_category, 
            "categories":categories, 
        })
    


@login_required
def create(request):
    categories = Category.objects.all()
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": categories,
        })

    # how do i get the user id from the current user that is logged in

    title = request.POST["title"]
    description = request.POST["description"]
    starting_bid = request.POST["starting_bid"]

    if not title or not description or not starting_bid:
        return render(request, "auctions/create.html", {
            "categories": categories,
            "message": f"The fields: Title, Description and Starting Bid are required."
        })

    if starting_bid := check_bid(starting_bid):
        listing =  Listing(user_id=request.user, title=title, description=description, starting_bid=starting_bid, max_bid=starting_bid, image_url=request.POST["image_url"], status=True)
        listing.save()
        
        if x := request.POST.get("category"):
            IsCategory(category_id=Category.objects.get(pk=int(x)), listing_id=listing).save()
        Watchlist(user_id=request.user, listing_id=listing).save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,))) 
    else:
        return render(request, "auctions/create.html", {
            "categories": categories,
            "message": f"The Starting Bid has to be a number."
        })
    

def listing(request, listing_id):
    user_id = request.user.id
    listing = Listing.objects.get(pk=listing_id)
    watchlist = [x.listing_id for x in Watchlist.objects.filter(user_id=user_id)]
    bids = Bid.objects.filter(listing_id=listing).order_by('-value')

    # the user who posted the listing should not be able to bid or add to watchlist
    logged_in = request.user.is_authenticated

    if request.method == "POST":
        max_bid = float(listing.max_bid)

        if request.POST.get("close_auction"):
            listing.status = False
            listing.winner = bids.first().user_id
            listing.save()
        
        if new_bid := request.POST.get("bid"):
            new_bid = check_bid(new_bid)
            if new_bid and new_bid > max_bid:
                Bid(value=new_bid, user_id=request.user, listing_id=listing).save()
                listing.max_bid = new_bid
                listing.save()
                bids = Bid.objects.filter(listing_id=listing).order_by('-value')

                # add listing to watchlist if you bid on it
                Watchlist(user_id=request.user, listing_id=listing).save()
            else:
                return render(request, "auctions/listing.html", {
                    "user_id": user_id,
                    "listing": listing, 
                    "logged_in": logged_in,
                    "watchlist": watchlist,
                    "bids": bids,   
                    "message": f"Your bid must be greater than all the other bids",
                })
        
        if remove_bid_id := request.POST.get("remove_bid"): 
            Bid.objects.get(pk=remove_bid_id).delete()
            listing.max_bid = Bid.objects.filter(listing_id=listing).order_by('-value').first().value
            listing.save()

        if remove_comment_id := request.POST.get("remove_comment"):
            Comment.objects.get(pk=remove_comment_id).delete()
        
        if content := request.POST.get("content"):
            Comment(content=content, user_id=request.user, listing_id=listing).save()

    comments = Comment.objects.filter(listing_id=listing).order_by('-time')

    return render(request, "auctions/listing.html", {
        "user_id": user_id,
        "listing": listing, 
        "logged_in": logged_in,
        "watchlist": watchlist,
        "bids": bids,
        "winner": listing.winner,
        "comments": comments,
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        if add_id := request.POST.get("add"):
            Watchlist(user_id=request.user, listing_id=Listing.objects.get(pk=int(add_id))).save()
        elif remove_id := request.POST.get("remove"):
            Watchlist.objects.get(user_id=request.user, listing_id=Listing.objects.get(pk=int(remove_id))).delete()

    return render(request, "auctions/watchlist.html", {
            "watchlist": sorted([x.listing_id for x in Watchlist.objects.filter(user_id=request.user.id)], key=lambda x: x.title.lower()) 
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


def check_bid(bid):
    if re.search(r'^\d*(\.\d{0,2})?$', bid):
        return float(bid)
    else:
        return None
    
