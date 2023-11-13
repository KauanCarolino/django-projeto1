from django.urls import path
from recipes.views import home
<<<<<<< HEAD
from . import views
from django.conf.urls.static import static
from django.conf import settings
=======
>>>>>>> 449690cbe3a176ae57378e1ae49d80e21595e3be

app_name = 'recipes'

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name="home"),
    path('recipe/category/<int:category_id>/', views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
    path('', home),  # /home/
]
>>>>>>> 449690cbe3a176ae57378e1ae49d80e21595e3be
