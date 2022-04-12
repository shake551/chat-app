from django.contrib import admin
import sys

sys.path.append('../')
from accounts.models.user import User

admin.site.register(User)
