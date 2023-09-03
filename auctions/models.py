from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.db.models import F, Value


def validate_email(value):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError('Invalid email')

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, validators=[validate_email])

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}"


class ListItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    data_post = models.DateField()
    photo_url = models.CharField(max_length=400)
    item_types = (
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Books", "Books"),
        ("Industrial Equipment", "Industrial Equipment"),
        ("Collectibles and Art", "Collectibles and Art"),
        ("Sports", "Sports"),
        ("Health and Beauty", "Health and Beauty"),
        ("Geek", "Geek"),
        ("Home and Garden", "Home and Garden"),
    )
    type_item = models.CharField(max_length=20, choices=item_types)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bids = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    idItem = models.ForeignKey(ListItem, on_delete=models.CASCADE,related_name="Comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="UserComment")
    text = models.CharField(max_length=500, blank=True,null=True)
  

    def __str__(self):
        return f"Comment by: {self.user.username}"

class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="UserBid")
    idItem = models.ForeignKey(ListItem, on_delete=models.CASCADE,related_name="bid")
    bids_amount =  models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    def save(self, *args, **kwargs):  
        if self.user == self.idItem.user:
            raise ValidationError("You cannot bid on your own item.")
        if self.bids_amount > self.idItem.price:
            self.idItem.bids = F('bids') +  Value(1)
            self.idItem.price = self.bids_amount
            self.idItem.save()
        else:
            raise ValidationError("Invalid bid amount, as it is lower than the current bid.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.idItem.bids = F('bids') - 1
        self.idItem.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Bid ID: {self.id}"

class WatchlistItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username}'s Watchlist: {self.item.name}"