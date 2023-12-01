from django.views import View
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from recipes.models import Recipe
from ..forms.recipe_form import AuthorRecipeForm

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()
        return recipe
    
    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )


    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)
    
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id, )))

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'deleted recipe success')
        return redirect(reverse('authors:dashboard'))