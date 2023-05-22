""""Admin site"""
from django.contrib import admin

from data.models.basic_models import RegularExp
from data.models.user_model import Profile

admin.site.register(RegularExp)
admin.site.register(Profile)
