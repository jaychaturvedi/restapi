from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import  authenticate, login, get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.urls import reverse_lazy
from user.forms import UserForm
from user.models import Profile
from rest_framework import viewsets
from user.serializers import UserSerializer 
User = get_user_model()

#restAPI -- class viewset
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

def index(request):
    return HttpResponseRedirect(reverse('user_list'))

def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('user_list'))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "auth/login.html", context)
    else:
        return render(request, "auth/login.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required(login_url="/login/")
def user_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'User'
    context['profiles'] = Profile.objects.all()
    return render(request, 'user/index.html', context)

@login_required(login_url="/login/")
def user_details(request, id=None):
    context = {}
    context['user'] = get_object_or_404(User, id=id)
    return render(request, 'user/details.html', context)

@login_required(login_url="/login/")
def user_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            u = user_form.save()    
            return HttpResponseRedirect(reverse('user_list'))
        else:
            return render(request, 'user/add.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'user/add.html', context)

@login_required(login_url="/login/")
def user_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()    
            return HttpResponseRedirect(reverse('user_list'))
        else:
            return render(request, 'user/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'user/edit.html', {"user_form": user_form})

@login_required(login_url="/login/")
def user_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    user.delete()
    return HttpResponseRedirect(reverse('user_list'))



class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.profile