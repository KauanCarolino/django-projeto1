from django.urls import path
from .views import home
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListviewBase.as_view(), name="home"),

    path('recipes/search/', views.RecipeViewSearch.as_view(), name="search"),

    path('recipes/tags/<slug:slug>/', views.RecipeViewTag.as_view(), name="tag"),

    path('recipes/category/<int:category_id>/',
         views.RecipeViewCategory.as_view(), name="category"),

    path('recipes/<int:pk>/', views.RecipeViewRecipe.as_view(), name="recipe"),

    path('recipes/theory/', views.theory, name="theory"),

    path('recipes/api/v1/<int:pk>/', views.RecipeDetailAPI.as_view(), name="recipes_api_v1"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
path('', home),  # /home/
