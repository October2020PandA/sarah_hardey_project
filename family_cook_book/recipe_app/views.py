from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from .forms import NewRecipeForm 
from time import gmtime, strftime 
from django.contrib import messages #erro message from validations
import bcrypt #password
from django.core.files.storage import FileSystemStorage #image
from django.views.generic import CreateView #imgae
from django.urls import reverse_lazy #image
from django.template.loader import render_to_string #search
from django.http import JsonResponse #search


# ----------------- LOGIN / REGISTER ------------------------------------------- #

# localhost:8000 (login/registeration page)
def index(request):
    # optional - if the users were to click away from the site and forget to logout they will be "flushed" back to the inedex page. 
    request.session.flush()
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # storing password harshing with salt string 
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # creating new user with password 
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
        # registeration creation 
        request.session['id'] = new_user.id 
    return redirect('/recipe_wall')
    # return redirect('/') #commented this out to make redirect to /recipe_wall work. 

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0: 
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
    return redirect('/recipe_wall')

def logout(request):
    request.session.flush()
    return redirect('/')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['id'])
    context = {
        'user': this_user,
        'recipes': Recipe.objects.all(),
    }
    return render(request, "recipe_wall.html", context)

# ----------------- RECIPE (list of all recipes) ------------------------------- #

#for receipe_wall.html -- pulls ALL recipes to be displayed on html page.
def recipe(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
        'recipes': Recipe.objects.all(),

    }
    return render(request, "recipe_wall", context)

# ---------------- CRUD RECIPIES ------------------------------------------------ #

#create new recipe (not using forms.py)
def new(request):
    if 'id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Recipe.objects.recipe_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_recipe')
        Recipe.objects.create(title=request.POST['title'], ingredents=request.POST['ingredents'], instructions=request.POST['instructions'], image=request.FILES['image'], recipe_creator=User.objects.get(id=request.session['id']))
        return redirect('/recipe_wall')
    else: 
        form = NewRecipeForm()
    return render(request, 'new_recipe.html', {'form': form})

#view recipe (recipe_card)
def view(request, id):
    if 'id' not in request.session:
        return redirect('/')
    recipe = Recipe.objects.get(id=id)
    context = { 
        'recipe': recipe,
        'comment': Comment.objects.all(), 
    }
    return render(request,'recipe_card.html', context)

#edit recipe - only the user that created the recipe can edit it.
def edit(request, id):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'recipe': Recipe.objects.get(id=id)
    }
    return render(request, 'edit_recipe.html', context)

#update recipe -- submit/save edits
def update(request, id):
    if request.method == 'POST': 
        errors = Recipe.objects.recipe_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{id}') 
        update_recipe = Recipe.objects.filter(id=id)
        if len(update_recipe) != 1:
            return redirect('/recipe_wall')
        elif update_recipe[0].recipe_creator.id != request.session['id']:
            return redirect('/recipe_wall') 
        update_recipe[0].title = request.POST['title']
        update_recipe[0].ingredents = request.POST['ingredents']
        update_recipe[0].instructions = request.POST['instructions']
        update_recipe[0].save()
    return redirect('/recipe_wall') 

#delete recipe - only user that created the recipe can delete it. 
def destroy(request, id):
    Recipe.objects.get(id=id).delete()
    return redirect('/recipe_wall')

#delete comment - only user that created the comment can delete it.
def destroy_comment(request, r_id, c_id):
    Comment.objects.get(id=c_id).delete()
    return redirect(f'/recipe/{r_id}') 

# ---------------- IMAGES/FILES ------------------------------------------------- #

#upload images
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage() #create object
        fs.save(uploaded_file.name, uploaded_file) #save file
        # name = fs.save()uploaded_file.name, uploaded_file)
        # context['url'] = fs.url(name)
    return render(request,'new_recipe.html', context) #update html location for this image 
 
# ---------------- POST A COMMENT ------------------------------------------------ #

#create a comment
def post_comment(request, id):
    comment_user = User.objects.get(id=request.session['id'])
    recipe = Recipe.objects.get(id=id)
    Comment.objects.create(comment_text=request.POST['comment_text'], comment_user=comment_user, recipe_comment=recipe)
    return redirect(f'/recipe/{id}')

# ---------------- SEARCH --------------------------------------------------------- #

#search/search for recipe titles
def search(request):
    if 'id' not in request.session:
        return redirect('/')
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        recipes = Recipe.objects.filter(title__icontains=url_parameter)
    else:
        recipes = Recipe.objects.all()

    ctx["recipes"] = recipes
    if request.is_ajax():

        html = render_to_string(
            template_name="search_results.html", context={"recipes": recipes}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "search.html", context=ctx)

