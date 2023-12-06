import os
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination
from recipes.models import Recipe
from django.forms.models import model_to_dict 
from django.http.response import JsonResponse
from django.views.generic import ListView, DetailView
from tag.models import Tag


# Variável constante.
PER_PAGE = os.environ.get('PER_PAGE', 6)

def theory(request, *args, **kwargs):
    
    recipes = Recipe.objects.get_published()


    numbers_of_recipes = recipes.aggregate(numbers=Count('id'))

    context = {
        'recipes': recipes,
        'numbers_of_recipes': numbers_of_recipes,
    }

    return render(request, 'recipes/pages/theory.html', context=context)


class RecipeListviewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update({ 'recipes': page_obj, 'pagination_range': pagination_range })
        return ctx
    

class RecipeViewCategory(RecipeListviewBase):
    template_name = 'recipes/pages/category.html'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )
        return qs

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })

        return ctx

class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


class RecipeViewSearch(RecipeListviewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q','')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        )
        return qs   
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q','')

        ctx.update({
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'additional_url_query': f'&q={search_term}',
        })

        return ctx
    
class RecipeViewTag(RecipeListviewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs   
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        ctx.update({
        'page_title': f'{page_title} - Tag|',
        })

        return ctx
    
    
class RecipeViewRecipe(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, *args,**kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })
        return ctx
    
    

def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):

    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    
    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
