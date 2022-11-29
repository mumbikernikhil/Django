from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact', contact, name='contact'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
    path('blog', handle_blog, name='blog'),
    path('search', search, name='search'),
    path('subscription', subscription, name='subscription'),
    path('success', success, name='success'),
]