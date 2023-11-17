from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeViewsBase
from unittest import skip


class RecipeVIewTest(RecipeViewsBase):
    def tearDown(self) -> None:
        return super().tearDown()
