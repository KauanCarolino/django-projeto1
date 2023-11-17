from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeViewsBase


class RecipeDetailVIewTest(RecipeViewsBase):
    def tearDown(self) -> None:
        return super().tearDown()
        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_details_template_loads_the_correct_recipes(self):
        needed_title = 'This is a detail page - it load one recipe'

        self.make_recipe(title=needed_title)

        response = self.client.get(

            reverse('recipes:recipe',
                    kwargs={
                        'id': 1,
                    }))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)