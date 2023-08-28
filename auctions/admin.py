from django.contrib import admin

from .models import Comment, ListItem, Bid, User, WatchlistItem

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(ListItem)
admin.site.register(Bid)
admin.site.register(WatchlistItem)