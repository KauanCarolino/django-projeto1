from django.http import Http404
from django.shortcuts import get_object_or_404, render
from utils.recipes.factory import make_recipe

from .models import Recipe
from recipes.models import Recipe


<<<<<<< HEAD
def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id')

    if not recipes:
        raise Http404('Not Found 😞')

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes.first().category.name} - Category |',
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })

=======

def home(request):
    return render(request, 'home.html')

>>>>>>> 449690cbe3a176ae57378e1ae49d80e21595e3be
