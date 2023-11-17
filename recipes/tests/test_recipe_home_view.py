from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeViewsBase
from unittest import skip


class RecipeHomeViewTest(RecipeViewsBase):
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    @skip('WIP')
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 🥲</h1>',
            response.content.decode('utf-8')
        )
        self.fail('Para que eu termine de digita-lo')

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertEquals(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipe_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>Receitas não encontradas ☹️</h1>',
            response.content.decode('utf-8')
        )