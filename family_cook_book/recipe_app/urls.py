from django.urls import path 
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout), 
    path('recipe_wall', views.success), #need to update #login takes you to /recipe_wall.html
    path('add_recipe', views.new), #takes you to add_recipe.html
    path('edit/<int:id>', views.edit), #takes you to edit_recipe.html
    path('update/<int:id>', views.update), #update after editing a recipe. Redirect to recipe/<int:id> (?)
    path('delete/<int:id>', views.destroy), #delet a recipe
    path('recipe/<int:id>', views.view), #view a recipe card, redirect to recipe/<int:id> (?)
    path('search', views.search), #search
    path('post_comment/<int:id>', views.post_comment), #post a comment on a recipe.
    path('recipe/<int:r_id>/destroy_comment/<int:c_id>', views.destroy_comment), #delete comment on a recipe

]

## urlpatterns used for image/files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)