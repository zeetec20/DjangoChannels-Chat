from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model

class Index(View):
    def get(self, request):
        listUser = get_user_model().objects.all()
        
        context = {
            'listUser': listUser 
        }
        return render(request, 'chat/index.html', context)