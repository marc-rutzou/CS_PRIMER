from django.contrib import admin

from .models import User, Listing, Bid, Comment, Category, IsCategory, Watchlist

# Register your models here.
class BidAdmin(admin.ModelAdmin):
    list_display = ("user_id", "listing_id", "value", )

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(IsCategory)
admin.site.register(Watchlist)