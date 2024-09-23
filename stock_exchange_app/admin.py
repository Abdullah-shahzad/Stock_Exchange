from django.contrib import admin
from .models import Users, Stocks, Transaction



admin.site.register(Users)
admin.site.register(Stocks)
admin.site.register(Transaction)

