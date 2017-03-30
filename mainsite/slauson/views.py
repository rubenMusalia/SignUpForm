from __future__ import absolute_import
from django.views import generic
from . models import *
from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse_lazy
from .forms import RegistrationForm, LoginForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from braces import views
# Create your views here.


class BasePageView(generic.TemplateView):
    template_name = 'base.html'


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


# For registration
class RegisterPageView(
    views.AnonymousRequiredMixin,
    views.FormValidMessageMixin,
    generic.CreateView
):
    form_class = RegistrationForm
    form_valid_message = "Thanks for signing up, go ahead ang login"
    model = User
    success_url = reverse_lazy('slauson:login')
    template_name = 'accounts/signup.html'


# For Logging Users in
class LoginView(
    views.FormValidMessageMixin,
    generic.FormView,
):
    form_class = LoginForm
    form_valid_message = "You're logged in"
    success_url = reverse_lazy('slauson:homepage')
    template_name = 'accounts/login.html'

# The form validates the data from the login form for authentication

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class ProfileUpdateView(generic.UpdateView):
    form_class = ProfileForm
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self,):
        return reverse('slauson:detail', kwargs={'slug': self.request.user})


class ProfileDetailView(generic.DetailView):
    slug_field = "username"
    model = get_user_model()
    template_name = 'accounts/detail.html'

    def get_object(self, queryset=None):
        user = super(ProfileDetailView, self).get_object(queryset)
        Profile.objects.get_or_create(user=user)
        return user


class ProfilesListView(
    generic.ListView,
):
    model = get_user_model()
    queryset = Profile.objects.all()
    template_name = 'accounts/list.html'


# For Logging Users out
class LogoutView(
    generic.RedirectView,
):
    url = reverse_lazy('slauson:basepage')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)



