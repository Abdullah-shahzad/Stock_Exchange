from django.contrib import admin
from .models import User, Stocks, Transaction



admin.site.register(User)
admin.site.register(Stocks)
admin.site.register(Transaction)

