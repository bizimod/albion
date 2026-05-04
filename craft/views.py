from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def categories(request,cat_id):
    return HttpResponse(f"<h1> Hello, world. You're at the polls categories.</h1><p>id: {cat_id}</p>")

def categories_by_slug(request,cat_slug):
    if request.Post:
        print(request.POST)
    return HttpResponse(f"<h1> Hello, world. You're at the polls slug-categories.</h1><p>slug: {cat_slug}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")