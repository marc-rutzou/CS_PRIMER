from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    def __str__(self):
        return f"username: {self.username} email: {self.email}"


class Listing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
    max_bid =  models.DecimalField(max_digits=12, decimal_places=2, default=0)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    image_url = models.URLField()
    status = models.BooleanField()      # True is active
    time = models.TimeField(auto_now_add=True)


class Bid(models.Model):
    value = models.DecimalField(max_digits=12, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_by_user")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_on_listing")


class Comment(models.Model):
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_by_user")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_on_listing")
    time = models.TimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=64)

class IsCategory(models.Model): 
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistings")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"user: {self.user_id.username} listing: {self.listing_id.title} user_id: {self.user_id.id} listing_id: {self.listing_id.id}"