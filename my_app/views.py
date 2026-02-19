from django.shortcuts import render

def home(request):
    context = {
        'title': 'Home',
        'content': 'Welcome to the home page',
        'is_home': True,
    }
    return render(request, 'pages/index.html', context)
def about(request):
    context = {
        'title': 'About',
        'content': 'Its DjangoProject from Roman_Tyshchuk from 21ICT group',
        'is_home': False,
    }
    return render(request, 'pages/index.html', context)
def contact(request):
    context = {
        'title': 'Contact',
        'content': 'This project is hosted on github: https://github.com/romanhhgfggh/Gambler_project.git' ,
        'is_home': False,
    }
    return render(request, 'pages/index.html', context)
# Create your views here.
