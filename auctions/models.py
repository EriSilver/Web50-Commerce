from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class items(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=128, verbose_name="Title")
    category = models.CharField(max_length=64, verbose_name="Category")
    description = models.TextField(verbose_name="Description", blank=True)
    bid = models.ForeignKey("bids", on_delete=models.CASCADE, default=None, blank=True, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Minimum price", validators=[MinValueValidator(0)])
    image = models.URLField(max_length=200, blank=True, verbose_name="Image URL")
    date = models.DateTimeField(verbose_name="Date Created", auto_now_add=True, blank=False, auto_created=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        b = self.min_price if not self.bid else self.bid.bid
        return f"{self.name} of category: {self.category} with a highest bid: ${b}."
    

class bids(models.Model):
    buser = models.ForeignKey(User, on_delete=models.CASCADE)
    bitem = models.ForeignKey(items, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bdate = models.DateTimeField(auto_now_add=True, blank=False, editable=False, auto_created=True)

    def __str__(self):
        return f"Bid of value ${self.bid} Created by: {self.buser.username} on {self.bitem.name} on {self.bdate}."

class comments(models.Model):
    citem = models.ForeignKey(items, on_delete=models.CASCADE)
    comment = models.TextField()
    cuser = models.ForeignKey(User, on_delete=models.CASCADE)
    cdate = models.DateTimeField(auto_now_add=True, blank=False, editable=False, auto_created=True)

    def __str__(self):
        return f"Comment on {self.citem.name} by {self.cuser.username} on {self.cdate}"

class watchlists(models.Model):
    witem = models.ForeignKey("items", on_delete=models.CASCADE)
    wuser = models.ForeignKey("User", on_delete=models.CASCADE)
    wdate = models.DateTimeField(auto_now_add=True, blank=False, editable=False, auto_created=True)

    def __str__(self):
        return f"{self.wuser.username} added {self.witem.name} to their watchlist on {self.wdate}"