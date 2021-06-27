from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import *

class NewListing(ModelForm):
    class Meta:
        model = items
        fields = ['name', 'category', 'description', 'min_price', 'image']        

def index(request):
    listings = items.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def inactive(request):
    listings = items.objects.filter(creator__username=request.user.username).filter(active=False)
    print(listings.values())
    return render(request, "auctions/inactive.html", {
        "listings": listings
    })

@login_required
def watchlist(request):
    listings = watchlists.objects.filter(wuser__username=request.user.username)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
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
            theuser = user
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

@login_required
def create(request):
    if request.method == "GET":
        form = NewListing()
        return render(request, "auctions/create.html", {
            "form": form
        })
    else:
        form = NewListing(request.POST)
        if not form.is_valid():
            return render(request, "auctions/create.html", {
                "form": form,
                "msg": "All fields are required."
            })
        data = dict(request.POST)
        titles = items.objects.values_list("name", flat=True)
        if data["name"][0] in titles:
            return render(request, "auctions/create.html", {
                "form" : form,
                "msg": "Title already exists."
            })
        print("############", request.user.username , "#########################")
        if not request.user.username:
            return render(request, "auctions/create.html", {
                "form": form,
                "msg": "Log in required"
            })

        cr = User.objects.get(username=request.user.username)

        ni = items(creator=cr, name=data["name"][0], category=data["category"][0], description=data["description"][0], min_price=data["min_price"][0], image=data["image"][0])
        ni.save()

        print(list(items.objects.values()))

        return HttpResponseRedirect("/")

def pages(request, title):
    cats = items.objects.filter(active=True).values_list("category", flat=True)
    if request.method == "GET" and title[:3] == "cat" and title[3:] in cats:
        listings = items.objects.filter(category=title[3:]).filter(active=True)
        return render(request, "auctions/index.html", {
            "listings": listings
        })

    titles = items.objects.values_list('name', flat=True)
    print(titles)
    if title not in titles:
        return render(request, "auctions/page.html", {
                "msg": "Item Unavailable"
            })
    info = items.objects.get(name=title)
    thecomments = comments.objects.filter(citem__name=info.name)
    user = ""
    if request.user.username:
        user = User.objects.get(username=request.user.username)

    if request.method == "GET":
        return render(request, "auctions/page.html", {
                "info": info,
                "comments": thecomments
            })
    else:
        data = dict(request.POST)
        print("$$$$$$$$$$$$$$$$$$$$\n", data)

        if user:
            # close auction
            if "closeauction" in data:
                info.active = False
                info.save()
                return render(request, "auctions/page.html", {
                    "title": title,
                    "info": info, 
                    "msg": "Auction Closed",
                    "comment": data["comment"][0] if "comment" in data else "",
                    "bid": data["bid"][0] if "bid" in data else "" ,
                    "comments": thecomments
                })

            # Adding comments
            if "addcomment" in data:
                c = data["comment"][0].strip()
                if not c:
                    return render(request, "auctions/page.html", {
                        "title": title,
                        "info": info, 
                        "msg": "Comments are supposed to contain numbers and letters, YOU DWEEP!",
                        "comment": data["comment"][0] if "comment" in data else "",
                        "bid": data["bid"][0] if "bid" in data else "" ,
                        "comments": thecomments
                    })

                co = comments(comment=c, citem=info, cuser=user )
                co.save()
                info = items.objects.get(name=title)
                thecomments = comments.objects.filter(citem__name=info.name)
                return render(request, "auctions/page.html", {
                    "title": title,
                    "info": info, 
                    "bid": data["bid"][0] if "bid" in data else "",
                    "comments": thecomments
                })

            if "watchlist" in data:
                item = watchlists.objects.filter(witem__name=info.name).filter(wuser__username=user.username)
                print(item.values())
                if not item:
                    wi = watchlists(wuser=user, witem=info)
                    wi.save()
                    msg = "Item added to your watchlist"

                else:
                    item.delete()
                    msg = "Item removed from your watchlist"
                
                return render(request, "auctions/page.html", {
                    "title": title,
                    "msg": msg,
                    "info": info,
                    "comment": data["comment"][0] if "comment" in data else "",
                    "bid": data["bid"][0] if "bid" in data else "" ,
                    "comments": thecomments
                })
            
            if "addbid" in data:
                thebid = data["bid"][0]
                # no bid entry error
                if not thebid:
                    return render(request, "auctions/page.html", {
                        "title": title,
                        "msg": "No bids submitted",
                        "info": info,
                        "comment": data["comment"][0] if "comment" in data else "",
                        "comments": thecomments
                    })
                # invalid bid
                for e in thebid:
                    if e not in ".0123456789":
                        return render(request, "auctions/page.html", {
                            "title": title,
                            "msg": "Invalid bid\nOnly decimals accepted",
                            "info": info,
                            "comment": data["comment"][0] if "comment" in data else "",
                            "bid": data["bid"][0] if "bid" in data else "" ,
                            "comments": thecomments
                        })

                if info.bid:
                    oldbid = info.bid.bid
                else:
                    oldbid = info.min_price
                
                thebid = float(thebid)
                oldbid = float(oldbid)

                if thebid <= oldbid:
                    return render(request, "auctions/page.html", {
                        "title": title,
                        "msg": "Invalid bid <br> Your bid must be higher than the existing price/bid.",
                        "info": info,
                        "comment": data["comment"][0] if "comment" in data else "",
                        "comments": thecomments
                    })

                bb = bids(buser=user, bitem=info, bid=thebid)
                bb.save()
                bc = bids.objects.filter(bid=thebid).filter(buser__username=user.username).filter(bitem__name=info.name)
                print(bc.values())
                info.bid = bc[0]
                info.save()
                info = items.objects.get(name=title)

                return render(request, "auctions/page.html", {
                    "title": title,
                    "msg": "Congrates, Bid Submitted!",
                    "info": info,
                    "comment": data["comment"][0] if "comment" in data else "",
                    "comments": thecomments
                })

        return render(request, "auctions/page.html", {
            "title": title,
            "info": info,
            "comments": thecomments
        })

def category(request):
    cats = items.objects.filter(active=True).values_list("category", flat=True).distinct()
    print("*******************",cats)
    return render(request, "auctions/category.html", {
        "cats": cats
    })


