from django.urls import path
from .views import *

app_name = "members"

urlpatterns = [
    path('login_usuarios', login_usuarios, name='login_usuarios'),
    path('logout', logout_view, name='logout'),
]


