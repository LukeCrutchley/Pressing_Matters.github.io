from django.contrib import admin
from .models import auctionList, auctionAdmin, watchlist, bids, comments

# Register your models here.
admin.site.register(auctionList, auctionAdmin)
admin.site.register(watchlist)
admin.site.register(bids)
admin.site.register(comments)
