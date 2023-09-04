


from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import TutorialCategory,TutorialSeries,Tutorial
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .forms import NewUserForm







def single_slug(request, single_slug):
    print("Received single_slug:", single_slug)
    # Rest of your code
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)

        series_urls = {}
        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            series_urls[m] = part_one.tutorial_slug

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]

    if single_slug in categories:
        return render(request,
                      "main/category.html",
                      {'part_ones' : series_urls })
    elif single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug = single_slug)
        tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        return render(request, "main/tutorial.html",{'tutorial': this_tutorial,'sidebar':tutorials_from_series,'this_tutorial_index':this_tutorial_idx})

        # return HttpResponse(f"{single_slug} is a tutorial in !!")
    else:
        return HttpResponse(f"{single_slug} does not correspond to any category or tutorial")




        # Create your views here.
def homepage(request):

    return render(request ,'main/categories.html',{"categories": TutorialCategory.objects.all})



def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,   f"new account created : {username} " )
            login(request, user)
            messages.info(request,   f"you are now logged in as  : {username} " )

            return redirect("main:homepage")
    else:
        form = NewUserForm()  # Create an empty form for GET requests

    # Move the error handling outside the else block
    errors = []
    for field_name, errors_list in form.errors.items():
        for error in errors_list:
            errors.append(f"{field_name.capitalize()}: {error}")

    return render(request, "main/register.html", {'form': form, 'errors': errors})

def logout_request(request):
    logout(request)
    messages.info(request, "logged out successfully !")
    return redirect('main:homepage')



def login_request(request):
    if request.method == "POST":  # Fix typo ("methord" should be "method")
        form = AuthenticationForm(request, data=request.POST)  # Fix typo ("request.post" should be "request.POST")
        if form.is_valid():
            username = form.cleaned_data['username']  # Use square brackets for dictionary access
            password = form.cleaned_data['password']  # Use square brackets for dictionary access
            user = authenticate(username=username, password=password)  # Use authenticate function

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "main/login.html", {"form": form})

