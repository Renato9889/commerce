from django.contrib import admin

from .models import Comment, ListItem, Bid, User

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(ListItem)
admin.site.register(Bid)