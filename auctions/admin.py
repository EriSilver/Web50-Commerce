from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(items)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(watchlists)
admin.site.register(User)
