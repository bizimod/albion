from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

def index(request):
    data = {
        'title':'Главная страница',
        'menu': menu,
    }
    return render(request, 'res/index.html',data)

def about(request):
    return render(request, 'res/about.html',{'title': 'О сайте'})

def categories_by_slug(request,cat_slug):
    return HttpResponse(f"<h1> Hello, world. You're at the polls slug-categories.</h1><p>slug: {cat_slug}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")