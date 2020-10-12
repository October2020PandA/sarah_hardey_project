from django.contrib import admin
from .models import * # carry modles over (like views.py)
#need to import Recipe model HERE

admin.site.register(User),
admin.site.register(Recipe),
admin.site.register(Comment),
 