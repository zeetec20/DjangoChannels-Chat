from django.views import View
from django.views.generic.base import RedirectView
from django.shortcuts import redirect

class Index(RedirectView):
    url = '/chat'